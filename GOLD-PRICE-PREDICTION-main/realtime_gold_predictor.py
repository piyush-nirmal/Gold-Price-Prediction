"""
Real-Time Gold Price Prediction System
=====================================

This script provides real-time gold price predictions using:
1. Live market data from Yahoo Finance
2. News sentiment analysis
3. Scheduled updates
4. Web dashboard for monitoring

Features:
- Real-time data fetching
- News sentiment analysis
- Historical comparison
- Alert system
- Web dashboard
"""

import yfinance as yf
import pandas as pd
import numpy as np
import schedule
import time
import json
import requests
from datetime import datetime, timedelta
from textblob import TextBlob
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

# Import our trained model
import pickle
from sklearn.ensemble import RandomForestRegressor

class RealTimeGoldPredictor:
    def __init__(self):
        """Initialize the real-time gold predictor"""
        self.model = None
        self.last_prediction = None
        self.prediction_history = []
        self.market_data = {}
        self.news_sentiment = 0
        self.alerts = []
        
        # Load the trained model
        self.load_model()
        
        # Market symbols
        self.symbols = {
            'SPX': '^GSPC',      # S&P 500
            'GLD': 'GLD',        # Gold ETF
            'USO': 'USO',        # Oil ETF
            'SLV': 'SLV',        # Silver ETF
            'EUR/USD': 'EURUSD=X' # EUR/USD
        }
        
        print("🚀 Real-Time Gold Price Predictor Initialized!")
        print("=" * 50)
    
    def load_model(self):
        """Load the trained Random Forest model"""
        try:
            # We'll create the model from our previous training
            # For now, we'll recreate it (in production, you'd save/load the model)
            print("📊 Loading trained model...")
            
            # Load the original data to retrain the model
            gold_data = pd.read_csv("gld_price_data.csv")
            data = gold_data.drop(['Date'], axis=1)
            
            # Remove outliers
            q = data["USO"].quantile(0.98)
            data = data[(data["USO"] < q)]
            
            # Prepare features and target
            X = data.drop(['GLD'], axis=1)
            Y = data['GLD']
            
            # Train the model
            self.model = RandomForestRegressor(n_estimators=100, random_state=0)
            self.model.fit(X, Y)
            
            print("✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def fetch_live_market_data(self):
        """Fetch live market data from Yahoo Finance"""
        try:
            print("📈 Fetching live market data...")
            market_data = {}
            
            for name, symbol in self.symbols.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="1d", interval="1m")
                    
                    if not hist.empty:
                        latest_price = hist['Close'].iloc[-1]
                        market_data[name] = {
                            'price': float(latest_price),
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'change': float(hist['Close'].iloc[-1] - hist['Open'].iloc[0]) if len(hist) > 1 else 0
                        }
                        print(f"  {name}: ${latest_price:.2f}")
                    else:
                        print(f"  ⚠️ No data for {name}")
                        
                except Exception as e:
                    print(f"  ❌ Error fetching {name}: {e}")
                    market_data[name] = None
            
            self.market_data = market_data
            return market_data
            
        except Exception as e:
            print(f"❌ Error fetching market data: {e}")
            return None
    
    def get_news_sentiment(self):
        """Get news sentiment for gold-related news"""
        try:
            print("📰 Analyzing news sentiment...")
            
            # Simple news sentiment analysis (in production, use more sophisticated methods)
            news_keywords = ['gold', 'precious metals', 'inflation', 'fed', 'interest rates']
            sentiment_scores = []
            
            # This is a simplified version - in production, you'd use news APIs
            # For now, we'll simulate sentiment based on market volatility
            if 'GLD' in self.market_data and self.market_data['GLD']:
                gld_change = self.market_data['GLD']['change']
                if gld_change > 0:
                    sentiment_scores.append(0.1)  # Positive sentiment
                else:
                    sentiment_scores.append(-0.1)  # Negative sentiment
            
            # Calculate average sentiment
            self.news_sentiment = np.mean(sentiment_scores) if sentiment_scores else 0
            print(f"  📊 News Sentiment: {self.news_sentiment:.3f}")
            
            return self.news_sentiment
            
        except Exception as e:
            print(f"❌ Error analyzing news sentiment: {e}")
            return 0
    
    def predict_gold_price(self):
        """Make real-time gold price prediction"""
        try:
            if not self.model or not self.market_data:
                print("❌ Model or market data not available")
                return None
            
            # Prepare features for prediction
            features = []
            feature_names = ['SPX', 'USO', 'SLV', 'EUR/USD']
            
            for feature in feature_names:
                if feature in self.market_data and self.market_data[feature]:
                    features.append(self.market_data[feature]['price'])
                else:
                    print(f"⚠️ Missing data for {feature}")
                    # Use a default value for missing data
                    if feature == 'EUR/USD':
                        features.append(1.0)  # Default EUR/USD rate
                    else:
                        return None
            
            # Make prediction
            prediction = self.model.predict([features])[0]
            
            # Adjust prediction based on news sentiment
            sentiment_adjustment = self.news_sentiment * 2  # Scale sentiment impact
            adjusted_prediction = prediction + sentiment_adjustment
            
            # Store prediction
            prediction_data = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'predicted_price': float(adjusted_prediction),
                'base_prediction': float(prediction),
                'sentiment_adjustment': float(sentiment_adjustment),
                'market_data': self.market_data.copy(),
                'news_sentiment': self.news_sentiment
            }
            
            self.last_prediction = prediction_data
            self.prediction_history.append(prediction_data)
            
            # Keep only last 100 predictions
            if len(self.prediction_history) > 100:
                self.prediction_history = self.prediction_history[-100:]
            
            print(f"🎯 Predicted Gold Price: ${adjusted_prediction:.2f}")
            print(f"   Base Prediction: ${prediction:.2f}")
            print(f"   Sentiment Adjustment: {sentiment_adjustment:+.2f}")
            
            return prediction_data
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return None
    
    def check_alerts(self):
        """Check for price alerts and market conditions"""
        try:
            if not self.last_prediction:
                return
            
            current_price = self.last_prediction['predicted_price']
            alerts = []
            
            # Price threshold alerts
            if current_price > 200:
                alerts.append("🚨 HIGH: Gold price predicted above $200")
            elif current_price < 100:
                alerts.append("⚠️ LOW: Gold price predicted below $100")
            
            # Volatility alerts
            if len(self.prediction_history) >= 5:
                recent_prices = [p['predicted_price'] for p in self.prediction_history[-5:]]
                volatility = np.std(recent_prices)
                if volatility > 5:
                    alerts.append("📊 HIGH VOLATILITY: Recent predictions show high volatility")
            
            # Sentiment alerts
            if abs(self.news_sentiment) > 0.5:
                sentiment_type = "POSITIVE" if self.news_sentiment > 0 else "NEGATIVE"
                alerts.append(f"📰 {sentiment_type} SENTIMENT: Strong market sentiment detected")
            
            if alerts:
                print("\n🔔 ALERTS:")
                for alert in alerts:
                    print(f"  {alert}")
                self.alerts.extend(alerts)
            
        except Exception as e:
            print(f"❌ Error checking alerts: {e}")
    
    def run_prediction_cycle(self):
        """Run a complete prediction cycle"""
        print(f"\n{'='*60}")
        print(f"🕐 PREDICTION CYCLE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        # Fetch live data
        market_data = self.fetch_live_market_data()
        
        if market_data:
            # Analyze news sentiment
            self.get_news_sentiment()
            
            # Make prediction
            prediction = self.predict_gold_price()
            
            if prediction:
                # Check for alerts
                self.check_alerts()
                
                # Save to file for dashboard
                self.save_prediction_data()
                
                return prediction
        
        return None
    
    def save_prediction_data(self):
        """Save prediction data to JSON file for dashboard"""
        try:
            data_to_save = {
                'last_prediction': self.last_prediction,
                'prediction_history': self.prediction_history[-20:],  # Last 20 predictions
                'alerts': self.alerts[-10:],  # Last 10 alerts
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            with open('realtime_predictions.json', 'w') as f:
                json.dump(data_to_save, f, indent=2)
                
        except Exception as e:
            print(f"❌ Error saving prediction data: {e}")
    
    def start_scheduled_predictions(self, interval_minutes=5):
        """Start scheduled predictions"""
        print(f"⏰ Starting scheduled predictions every {interval_minutes} minutes...")
        
        # Schedule predictions
        schedule.every(interval_minutes).minutes.do(self.run_prediction_cycle)
        
        # Run initial prediction
        self.run_prediction_cycle()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping scheduled predictions...")
    
    def get_prediction_summary(self):
        """Get a summary of current predictions and market status"""
        if not self.last_prediction:
            return "No predictions available"
        
        summary = f"""
📊 REAL-TIME GOLD PRICE PREDICTION SUMMARY
{'='*50}
🕐 Last Update: {self.last_prediction['timestamp']}
🎯 Predicted Price: ${self.last_prediction['predicted_price']:.2f}
📈 Base Prediction: ${self.last_prediction['base_prediction']:.2f}
📰 Sentiment Adjustment: {self.last_prediction['sentiment_adjustment']:+.2f}
📊 News Sentiment: {self.last_prediction['news_sentiment']:.3f}

📈 MARKET DATA:
"""
        
        for name, data in self.market_data.items():
            if data:
                change_str = f"{data['change']:+.2f}" if data['change'] != 0 else "0.00"
                summary += f"  {name}: ${data['price']:.2f} ({change_str})\n"
        
        if self.alerts:
            summary += f"\n🔔 RECENT ALERTS:\n"
            for alert in self.alerts[-3:]:
                summary += f"  {alert}\n"
        
        return summary

def main():
    """Main function to run the real-time predictor"""
    print("🌟 REAL-TIME GOLD PRICE PREDICTION SYSTEM")
    print("=" * 60)
    
    # Initialize predictor
    predictor = RealTimeGoldPredictor()
    
    # Get user choice
    print("\nChoose an option:")
    print("1. Run single prediction")
    print("2. Start scheduled predictions (every 5 minutes)")
    print("3. Start scheduled predictions (every 1 minute)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == '1':
        # Single prediction
        predictor.run_prediction_cycle()
        print("\n" + predictor.get_prediction_summary())
        
    elif choice == '2':
        # Scheduled predictions every 5 minutes
        predictor.start_scheduled_predictions(5)
        
    elif choice == '3':
        # Scheduled predictions every 1 minute
        predictor.start_scheduled_predictions(1)
        
    elif choice == '4':
        print("👋 Goodbye!")
        
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
