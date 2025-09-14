from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import requests
import plotly.graph_objs as go
import plotly.utils
import google.generativeai as genai
from src.data_preprocessing import DataPreprocessor
from src.gold_predictor import GoldPricePredictor
from src.recommendation_engine import InvestmentRecommendationEngine
from src.real_time_sentiment import RealTimeSentimentAnalyzer
from bs4 import BeautifulSoup

app = Flask(__name__)

# Global variables to store data and models
processed_data = None
predictor = None
recommendation_engine = InvestmentRecommendationEngine()
sentiment_analyzer = None

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyBe0Dnwwu96kGgLlq-v3oU1eiQ2kuuqoF4"
genai.configure(api_key=GEMINI_API_KEY)

def get_live_gold_price():
    """Get live gold price from multiple free APIs"""
    try:
        # Try Coinbase API first (most reliable)
        response = requests.get('https://api.coinbase.com/v2/exchange-rates?currency=XAU', timeout=10)
        if response.status_code == 200:
            data = response.json()
            rates = data.get('data', {}).get('rates', {})
            usd_rate = rates.get('USD')
            if usd_rate:
                try:
                    return float(usd_rate)
                except:
                    pass
        
        # Try Alpha Vantage (free tier) as fallback
        response = requests.get('https://www.alphavantage.co/query?function=COMMODITY_EXCHANGE_RATE&from_symbol=XAU&to_symbol=USD&apikey=demo', timeout=10)
        if response.status_code == 200:
            data = response.json()
            price = data.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate')
            if price:
                try:
                    return float(price)
                except:
                    pass
                
        return 1800  # Default fallback
    except:
        return 1800  # Default fallback

def get_usd_to_inr_rate():
    """Get current USD to INR exchange rate"""
    try:
        # Using a free currency API
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['rates'].get('INR', 83.0)  # Default fallback
        else:
            return 83.0  # Default fallback
    except:
        return 83.0  # Default fallback

# --- MetalpriceAPI.com integration (optional) ---
def get_live_gold_price_metalpriceapi():
    """Get live gold price using MetalpriceAPI if configured.

    Returns tuple (usd_per_oz, inr_per_oz) where each may be None.
    """
    api_key = os.environ.get('METALPRICE_API_KEY')
    if not api_key:
        return None, None
    try:
        usd = None
        inr = None
        # Query USD price per XAU
        url_usd = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=XAU&currencies=USD"
        r1 = requests.get(url_usd, timeout=10)
        if r1.status_code == 200:
            d1 = r1.json()
            v = d1.get('rates', {}).get('USD')
            if isinstance(v, (int, float)) and v > 0:
                usd = float(v)
        # Query INR price per XAU
        url_inr = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=XAU&currencies=INR"
        r2 = requests.get(url_inr, timeout=10)
        if r2.status_code == 200:
            d2 = r2.json()
            v = d2.get('rates', {}).get('INR')
            if isinstance(v, (int, float)) and v > 0:
                inr = float(v)
        return usd, inr
    except Exception:
        return None, None

def get_usd_to_inr_rate_metalpriceapi():
    """Get USD→INR rate using MetalpriceAPI if configured. Returns None on failure."""
    api_key = os.environ.get('METALPRICE_API_KEY')
    if not api_key:
        return None
    try:
        url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=INR"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            rate = data.get('rates', {}).get('INR')
            if isinstance(rate, (int, float)) and rate > 0:
                return float(rate)
        return None
    except Exception:
        return None

def convert_usd_to_inr(usd_price, exchange_rate=None):
    """Convert USD price to INR"""
    if exchange_rate is None:
        exchange_rate = get_usd_to_inr_rate()
    return usd_price * exchange_rate

def get_indian_gold_prices_gemini():
    """Get real-time Indian gold prices using Gemini AI"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = """
        Get me the current gold prices in India for today. Please provide:
        1. Gold price per 10 grams in major Indian cities (Mumbai, Delhi, Chennai, Kolkata, Bangalore)
        2. Gold price per gram
        3. Gold price per troy ounce
        4. Current market trends and analysis
        5. Any significant news affecting gold prices in India
        6. Gold purity levels (22K, 24K) and their prices
        
        Please format the response as JSON with the following structure:
        {
            "prices_per_10gm": {
                "mumbai": price,
                "delhi": price,
                "chennai": price,
                "kolkata": price,
                "bangalore": price
            },
            "price_per_gram": price,
            "price_per_troy_ounce": price,
            "market_trend": "up/down/stable",
            "market_analysis": "brief analysis",
            "news_impact": "relevant news",
            "purity_prices": {
                "22k": price_per_10gm,
                "24k": price_per_10gm
            }
        }
        """
        
        response = model.generate_content(prompt)
        
        # Try to parse JSON from response
        try:
            # Extract JSON from the response text
            response_text = response.text
            # Find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback: create structured data from text
                return parse_gemini_response(response_text)
                
        except json.JSONDecodeError:
            # Fallback: parse the text response
            return parse_gemini_response(response.text)
            
    except Exception as e:
        print(f"Error getting Gemini data: {e}")
        return get_fallback_indian_prices()

def parse_gemini_response(text):
    """Parse Gemini response text to extract price information"""
    try:
        # Extract prices using regex patterns
        import re
        
        # Look for price patterns like "₹45,000" or "45000"
        price_pattern = r'₹?([\d,]+)'
        prices = re.findall(price_pattern, text)
        
        # Convert to numbers
        numeric_prices = []
        for price in prices:
            try:
                numeric_prices.append(float(price.replace(',', '')))
            except:
                continue
        
        # Use average of found prices as base
        avg_price = sum(numeric_prices) / len(numeric_prices) if numeric_prices else 55000
        
        return {
            "prices_per_10gm": {
                "mumbai": avg_price,
                "delhi": avg_price + 100,
                "chennai": avg_price - 50,
                "kolkata": avg_price + 50,
                "bangalore": avg_price + 75
            },
            "price_per_gram": avg_price / 10,
            "price_per_troy_ounce": avg_price * 3.11,  # 10gm to troy oz
            "market_trend": "stable",
            "market_analysis": "Gold prices showing stability with minor fluctuations",
            "news_impact": "Market sentiment influenced by global economic factors",
            "purity_prices": {
                "22k": avg_price * 0.916,  # 22K is 91.6% pure
                "24k": avg_price
            },
            "raw_response": text[:500]  # First 500 chars for debugging
        }
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        return get_fallback_indian_prices()

def get_fallback_indian_prices():
    """Fallback Indian gold prices when API fails"""
    base_price = 55000  # Approximate 10gm price
    
    return {
        "prices_per_10gm": {
            "mumbai": base_price,
            "delhi": base_price + 100,
            "chennai": base_price - 50,
            "kolkata": base_price + 50,
            "bangalore": base_price + 75
        },
        "price_per_gram": base_price / 10,
        "price_per_troy_ounce": base_price * 3.11,
        "market_trend": "stable",
        "market_analysis": "Gold prices showing stability with minor fluctuations",
        "news_impact": "Market sentiment influenced by global economic factors",
        "purity_prices": {
            "22k": base_price * 0.916,
            "24k": base_price
        }
    }

# --- Goodreturns scraper for city-wise Indian gold prices ---
GOODRETURNS_CITY_URLS = {
    'mumbai': 'https://www.goodreturns.in/gold-rates/mumbai.html',
    'delhi': 'https://www.goodreturns.in/gold-rates/delhi.html',
    'chennai': 'https://www.goodreturns.in/gold-rates/chennai.html',
    'kolkata': 'https://www.goodreturns.in/gold-rates/kolkata.html',
    'bangalore': 'https://www.goodreturns.in/gold-rates/bangalore.html',
}

def parse_goodreturns_10g_prices(html_text):
    """Parse Goodreturns HTML to get per-10g prices for 24K and 22K.
    Returns dict { '24k': float, '22k': float } in INR.
    """
    soup = BeautifulSoup(html_text, 'lxml')
    result = {}
    try:
        # Prefer structured table parsing if available
        import re
        rows = soup.find_all('tr')
        for tr in rows:
            row_text = ' '.join(tr.stripped_strings)
            if not row_text:
                continue
            # Look for lines like: "24 Carat Gold (10 grams) Rs 1,12,650"
            m24 = re.search(r'(24\s*(?:carat|k)\b).*?(10\s*grams).*?([₹\s]*[\d,]{4,})', row_text, re.IGNORECASE)
            m22 = re.search(r'(22\s*(?:carat|k)\b).*?(10\s*grams).*?([₹\s]*[\d,]{4,})', row_text, re.IGNORECASE)
            if m24:
                num = re.sub(r'[^\d,]', '', m24.group(3)).replace(',', '')
                try:
                    result['24k'] = float(num)
                except:
                    pass
            # Another common layout: a row with first cell '10 grams' and next cells are 24k and 22k
            cells = [c.get_text(strip=True) for c in tr.find_all(['td','th'])]
            if cells and re.search(r'^10\s*grams?$', cells[0], re.IGNORECASE) and len(cells) >= 3:
                # Try to parse 24k and 22k from the remaining cells
                def parse_num(s):
                    s = re.sub(r'[^\d,]', '', s)
                    return float(s.replace(',', '')) if s else None
                n24 = parse_num(cells[1])
                n22 = parse_num(cells[2])
                if n24 and '24k' not in result:
                    result['24k'] = n24
                if n22 and '22k' not in result:
                    result['22k'] = n22
            if m22:
                num = re.sub(r'[^\d,]', '', m22.group(3)).replace(',', '')
                try:
                    result['22k'] = float(num)
                except:
                    pass
        # Fallback to full-text regex if table parsing failed
        if '24k' not in result or '22k' not in result:
            text = soup.get_text(' ', strip=True)
            def find_price(patterns):
                for p in patterns:
                    m = re.search(p, text, re.IGNORECASE)
                    if m:
                        num = re.sub(r'[^\d,]', '', m.group(1)).replace(',', '')
                        try:
                            return float(num)
                        except:
                            continue
                return None
            price_24 = find_price([
                r'24\s*(?:carat|k)[^\d]{0,40}([₹\s]*[\d,]{4,})\b.*?10\s*grams',
                r'10\s*grams[^\d]{0,40}([₹\s]*[\d,]{4,})\b.*?24\s*(?:carat|k)'
            ])
            price_22 = find_price([
                r'22\s*(?:carat|k)[^\d]{0,40}([₹\s]*[\d,]{4,})\b.*?10\s*grams',
                r'10\s*grams[^\d]{0,40}([₹\s]*[\d,]{4,})\b.*?22\s*(?:carat|k)'
            ])
            if price_24 and '24k' not in result:
                result['24k'] = price_24
            if price_22 and '22k' not in result:
                result['22k'] = price_22
    except Exception:
        pass
    return result

def get_city_prices_goodreturns():
    """Fetch per-10g prices from Goodreturns for configured cities.
    Returns structure compatible with frontend indian_prices.
    """
    prices_per_10gm = {}
    purity_prices = {'22k': None, '24k': None}
    for city, url in GOODRETURNS_CITY_URLS.items():
        try:
            r = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            if r.status_code == 200:
                parsed = parse_goodreturns_10g_prices(r.text)
                if '24k' in parsed:
                    prices_per_10gm[city] = float(parsed['24k'])
                    purity_prices['24k'] = float(parsed['24k'])
                if '22k' in parsed:
                    purity_prices['22k'] = float(parsed['22k'])
        except Exception:
            continue
    # Fallback: if any missing, keep previous computed values or defaults
    if not prices_per_10gm:
        return get_fallback_indian_prices()
    # If purity missing, infer 22k from 24k
    if purity_prices['24k'] and not purity_prices['22k']:
        purity_prices['22k'] = purity_prices['24k'] * 0.916
    return {
        'prices_per_10gm': prices_per_10gm,
        'price_per_gram': list(prices_per_10gm.values())[0] / 10,
        'price_per_troy_ounce': list(prices_per_10gm.values())[0] * 3.11,
        'market_trend': 'stable',
        'market_analysis': 'City prices sourced from Goodreturns.in',
        'news_impact': '-',
        'purity_prices': purity_prices
    }

def initialize_models():
    """Initialize and train models if not already done"""
    global processed_data, predictor, sentiment_analyzer
    
    try:
        # Try to load existing processed data
        if os.path.exists('data/processed_gold_data.csv'):
            processed_data = pd.read_csv('data/processed_gold_data.csv')
            processed_data['Date'] = pd.to_datetime(processed_data['Date'])
            print("Loaded existing processed data")
        else:
            # Process data from scratch
            preprocessor = DataPreprocessor()
            processed_data = preprocessor.preprocess_all()
            processed_data.to_csv('data/processed_gold_data.csv', index=False)
            print("Processed and saved data")
        
        # Initialize predictor
        predictor = GoldPricePredictor()
        
        # Try to load existing model
        if os.path.exists('models/gold_predictor_model.pkl') and os.path.exists('models/scalers.pkl'):
            predictor.load_model()
            print("Loaded existing trained model")
        else:
            # Train new model
            print("Training new model...")
            predictor.train_model(processed_data)
            predictor.save_model()
            print("Model trained and saved")
        
        # Initialize sentiment analyzer
        sentiment_analyzer = RealTimeSentimentAnalyzer()
        print("Initialized real-time sentiment analyzer")
            
    except Exception as e:
        print(f"Error initializing models: {e}")
        # Create dummy data for demo
        dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
        processed_data = pd.DataFrame({
            'Date': dates,
            'SF_Price': np.random.normal(1800, 100, len(dates)),
            'Sentiment_score': np.random.normal(0, 0.3, len(dates)),
            'News': ['Sample news'] * len(dates)
        })

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/current_price')
def api_current_price():
    """API endpoint to get current gold price"""
    try:
        # Prefer MetalpriceAPI if configured, else fallback
        mp_usd, mp_inr = get_live_gold_price_metalpriceapi()
        if mp_usd is not None:
            live_price_usd = mp_usd
        else:
            live_price_usd = get_live_gold_price()

        if mp_inr is not None:
            live_price_inr = mp_inr
            exchange_rate = live_price_inr / live_price_usd if live_price_usd else (get_usd_to_inr_rate_metalpriceapi() or get_usd_to_inr_rate())
        else:
            exchange_rate = get_usd_to_inr_rate_metalpriceapi() or get_usd_to_inr_rate()
            live_price_inr = convert_usd_to_inr(live_price_usd, exchange_rate)
        
        # Calculate Indian prices from live API data
        try:
            inr_per_oz = live_price_inr
            price_per_10gm_24k = (inr_per_oz * (10 / 31.1035))
            # Apply retail premium to match Indian market prices
            RETAIL_PREMIUM_PCT = float(os.environ.get('RETAIL_PREMIUM_PCT', '0.12'))
            price_per_10gm_24k *= (1 + RETAIL_PREMIUM_PCT)
            
            prices_per_10gm = {city: price_per_10gm_24k for city in ['mumbai','delhi','chennai','kolkata','bangalore']}
            indian_prices = {
                'prices_per_10gm': {k: float(v) for k, v in prices_per_10gm.items()},
                'price_per_gram': float(price_per_10gm_24k / 10),
                'price_per_troy_ounce': float(price_per_10gm_24k * 3.11035),
                'market_trend': 'stable',
                'market_analysis': 'Live API data with Indian retail premium',
                'news_impact': '-',
                'purity_prices': {
                    '22k': float(price_per_10gm_24k * 0.916),
                    '24k': float(price_per_10gm_24k)
                }
            }
        except Exception:
            indian_prices = get_fallback_indian_prices()
        
        # Calculate spot price (without retail premium) for consistency
        spot_price_10gm = (live_price_inr * (10 / 31.1035))
        
        return jsonify({
            'price_usd': live_price_usd,
            'price_inr': live_price_inr,
            'exchange_rate': exchange_rate,
            'spot_price_10gm': float(spot_price_10gm),  # Spot price for consistency
            'retail_price_10gm': float(indian_prices['prices_per_10gm']['mumbai']),  # Retail price with premium
            'indian_prices': indian_prices,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'price_usd': 1800,
            'price_inr': 149400,  # 1800 * 83
            'exchange_rate': 83.0,
            'indian_prices': get_fallback_indian_prices(),
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/indian_gold_prices')
def api_indian_gold_prices():
    """API endpoint to get Indian gold prices per 10gm"""
    try:
        indian_prices = get_city_prices_goodreturns()
        
        return jsonify({
            'indian_prices': indian_prices,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({
            'indian_prices': get_fallback_indian_prices(),
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/prediction')
def api_prediction():
    """API endpoint to get price predictions"""
    try:
        if predictor and predictor.is_trained and processed_data is not None:
            # Get historical last price (model baseline)
            historical_last_price_usd = processed_data['SF_Price'].iloc[-1]
            
            # Get live international price (USD/oz) and align predictions to real-time
            # Use the same price source as current_price API
            current_price = get_live_gold_price()
            
            # Get real-time sentiment analysis
            if sentiment_analyzer:
                current_sentiment, sentiment_strength, latest_news = sentiment_analyzer.get_current_sentiment()
            else:
                # Fallback to historical sentiment
                current_sentiment = processed_data['Sentiment_score'].iloc[-1]
                latest_news = str(processed_data['News'].iloc[-1]) if pd.notna(processed_data['News'].iloc[-1]) else ""
            
            # Make predictions
            next_day_price = predictor.predict_next_day(processed_data)
            next_week_prices = predictor.predict_next_week(processed_data)

            # Align model outputs to live market by shifting with the difference to last known
            price_shift = float(current_price) - float(historical_last_price_usd)
            next_day_price = float(next_day_price) + price_shift
            next_week_prices = [float(p) + price_shift for p in next_week_prices]
            
            # Get exchange rate for INR conversion (same as current_price API)
            exchange_rate = get_usd_to_inr_rate()
            
            # Convert prices to INR
            current_price_inr = convert_usd_to_inr(current_price, exchange_rate)
            next_day_price_inr = convert_usd_to_inr(next_day_price, exchange_rate)
            next_week_prices_inr = [convert_usd_to_inr(p, exchange_rate) for p in next_week_prices]
            
            # Convert troy ounce prices to per 10 grams (1 troy oz = 31.1035 grams)
            troy_oz_to_10gm = 10 / 31.1035
            current_price_10gm = current_price_inr * troy_oz_to_10gm
            next_day_price_10gm = next_day_price_inr * troy_oz_to_10gm
            next_week_prices_10gm = [p * troy_oz_to_10gm for p in next_week_prices_inr]
            
            # Generate recommendation
            recommendation = recommendation_engine.generate_recommendation(
                float(current_price), float(next_day_price), current_sentiment, latest_news
            )
            
            return jsonify({
                'current_price_usd': float(current_price),
                'current_price_inr': float(current_price_inr),
                'current_price_10gm': float(current_price_10gm),
                'next_day_price_usd': float(next_day_price),
                'next_day_price_inr': float(next_day_price_inr),
                'next_day_price_10gm': float(next_day_price_10gm),
                'next_week_prices_usd': [float(p) for p in next_week_prices],
                'next_week_prices_inr': [float(p) for p in next_week_prices_inr],
                'next_week_prices_10gm': [float(p) for p in next_week_prices_10gm],
                'exchange_rate': float(exchange_rate),
                'recommendation': {
                    'recommendation': recommendation['recommendation'],
                    'confidence': float(recommendation['confidence']),
                    'reasoning': recommendation['reasoning'],
                    'current_price_usd': float(recommendation['current_price']),
                    'current_price_inr': float(current_price_inr),
                    'current_price_10gm': float(current_price_10gm),
                    'predicted_price_usd': float(recommendation['predicted_price']),
                    'predicted_price_inr': float(next_day_price_inr),
                    'predicted_price_10gm': float(next_day_price_10gm),
                    'price_change_pct': float(recommendation['price_change_pct']),
                    'sentiment_score': float(recommendation['sentiment_score']),
                    'price_trend': recommendation['price_trend'],
                    'sentiment_strength': recommendation['sentiment_strength']
                },
                'status': 'success'
            })
        else:
            return jsonify({
                'status': 'error',
                'error': 'Model not trained or data not available'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/historical_data')
def api_historical_data():
    """API endpoint to get historical data for charts"""
    try:
        if processed_data is not None:
            # Get last 30 days of data for charts
            recent_data = processed_data.tail(30)
            
            return jsonify({
                'dates': [d.strftime('%Y-%m-%d') for d in recent_data['Date']],
                'prices': [float(p) for p in recent_data['SF_Price']],
                'sentiment': [float(s) for s in recent_data['Sentiment_score']],
                'status': 'success'
            })
        else:
            return jsonify({
                'status': 'error',
                'error': 'No data available'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

@app.route('/api/chart_data')
def api_chart_data():
    """API endpoint to get chart data with Plotly"""
    try:
        if processed_data is not None:
            # Get last 30 days of data
            recent_data = processed_data.tail(30)
            
            # Create price chart
            price_chart = go.Figure()
            price_chart.add_trace(go.Scatter(
                x=recent_data['Date'],
                y=recent_data['SF_Price'],
                mode='lines',
                name='Gold Price',
                line=dict(color='gold', width=2)
            ))
            price_chart.update_layout(
                title='Gold Price Trend (Last 30 Days) - Per Troy Ounce',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                template='plotly_white'
            )
            
            # Create sentiment chart
            sentiment_chart = go.Figure()
            sentiment_chart.add_trace(go.Scatter(
                x=recent_data['Date'],
                y=recent_data['Sentiment_score'],
                mode='lines+markers',
                name='Sentiment Score',
                line=dict(color='blue', width=2),
                marker=dict(size=6)
            ))
            sentiment_chart.add_hline(y=0, line_dash="dash", line_color="gray")
            sentiment_chart.update_layout(
                title='Market Sentiment Trend (Last 30 Days)',
                xaxis_title='Date',
                yaxis_title='Sentiment Score',
                template='plotly_white'
            )
            
            return jsonify({
                'price_chart': json.dumps(price_chart, cls=plotly.utils.PlotlyJSONEncoder),
                'sentiment_chart': json.dumps(sentiment_chart, cls=plotly.utils.PlotlyJSONEncoder),
                'status': 'success'
            })
        else:
            return jsonify({
                'status': 'error',
                'error': 'No data available'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': str(e)
        })

 

@app.route('/dashboard')
def dashboard():
    """Dashboard page with charts and recommendations"""
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('models', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    # Initialize models
    initialize_models()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)
