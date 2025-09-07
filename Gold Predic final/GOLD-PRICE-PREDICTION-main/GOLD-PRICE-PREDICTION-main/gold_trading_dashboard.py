"""
Gold Trading Dashboard with Sentiment Analysis
============================================

A comprehensive dashboard showing:
- Current gold price
- Today's opening and closing prices
- Upper and lower circuit limits
- Sentiment-based buy/hold/sell recommendations
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import numpy as np
import yfinance as yf

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Gold Trading Dashboard"

# Custom CSS for professional trading interface
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .main-container {
                background: rgba(255, 255, 255, 0.95);
                margin: 20px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                backdrop-filter: blur(10px);
                padding: 30px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 25px;
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
                border-radius: 15px;
                color: #1e3c72;
                box-shadow: 0 10px 20px rgba(255, 215, 0, 0.3);
            }
            .header h1 {
                margin: 0;
                font-size: 2.8em;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }
            .header p {
                margin: 10px 0 0 0;
                font-size: 1.3em;
                opacity: 0.8;
            }
            .price-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .price-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                text-align: center;
                border-top: 5px solid #FFD700;
                transition: transform 0.3s ease;
            }
            .price-card:hover {
                transform: translateY(-5px);
            }
            .price-value {
                font-size: 2.2em;
                font-weight: bold;
                color: #1e3c72;
                margin: 10px 0;
            }
            .price-label {
                color: #666;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }
            .current-price {
                border-top-color: #4CAF50;
                background: linear-gradient(135deg, #E8F5E8 0%, #F1F8E9 100%);
            }
            .current-price .price-value {
                color: #2E7D32;
                font-size: 3em;
            }
            .circuit-limit {
                border-top-color: #FF5722;
            }
            .circuit-limit .price-value {
                color: #D32F2F;
            }
            .sentiment-section {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                margin-bottom: 30px;
                text-align: center;
            }
            .sentiment-title {
                font-size: 2em;
                font-weight: 600;
                color: #1e3c72;
                margin-bottom: 20px;
            }
            .recommendation {
                font-size: 2.5em;
                font-weight: bold;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
            }
            .recommendation.buy {
                background: linear-gradient(135deg, #4CAF50 0%, #8BC34A 100%);
                color: white;
            }
            .recommendation.hold {
                background: linear-gradient(135deg, #FF9800 0%, #FFC107 100%);
                color: white;
            }
            .recommendation.sell {
                background: linear-gradient(135deg, #F44336 0%, #E91E63 100%);
                color: white;
            }
            .sentiment-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .sentiment-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                border-left: 4px solid #FFD700;
            }
            .sentiment-label {
                font-weight: 600;
                color: #666;
                margin-bottom: 5px;
            }
            .sentiment-value {
                font-size: 1.3em;
                font-weight: bold;
                color: #1e3c72;
            }
            .chart-container {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .chart-title {
                font-size: 1.5em;
                font-weight: 600;
                color: #1e3c72;
                margin-bottom: 20px;
                text-align: center;
            }
            .market-info {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
            }
            .market-info h3 {
                margin-top: 0;
                text-align: center;
            }
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            .info-item {
                text-align: center;
                padding: 10px;
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
            }
            .info-label {
                font-size: 0.9em;
                opacity: 0.8;
                margin-bottom: 5px;
            }
            .info-value {
                font-size: 1.2em;
                font-weight: bold;
            }
            .last-update {
                text-align: center;
                color: #666;
                font-style: italic;
                margin-top: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
            }
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .status-online { background-color: #4CAF50; }
            .status-offline { background-color: #F44336; }
        </style>
    </head>
    <body>
        <div class="main-container">
            {%app_entry%}
        </div>
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

def get_gold_data():
    """Fetch real-time gold data from Yahoo Finance"""
    try:
        # Fetch GLD (Gold ETF) data
        gld = yf.Ticker("GLD")
        hist = gld.history(period="2d", interval="1d")
        
        if not hist.empty:
            latest = hist.iloc[-1]
            previous = hist.iloc[-2] if len(hist) > 1 else latest
            
            # Calculate circuit limits (typically 5% for gold)
            current_price = float(latest['Close'])
            upper_circuit = current_price * 1.05  # 5% upper limit
            lower_circuit = current_price * 0.95  # 5% lower limit
            
            return {
                'current_price': current_price,
                'open_price': float(latest['Open']),
                'close_price': float(latest['Close']),
                'previous_close': float(previous['Close']),
                'high': float(latest['High']),
                'low': float(latest['Low']),
                'volume': int(latest['Volume']),
                'upper_circuit': upper_circuit,
                'lower_circuit': lower_circuit,
                'change': float(latest['Close'] - previous['Close']),
                'change_percent': float((latest['Close'] - previous['Close']) / previous['Close'] * 100),
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        print(f"Error fetching gold data: {e}")
        return None

def analyze_sentiment_and_recommendation(gold_data, prediction_data=None):
    """Analyze sentiment and provide buy/hold/sell recommendation"""
    if not gold_data:
        return "HOLD", 0, "Insufficient data"
    
    # Base sentiment factors
    sentiment_score = 0
    factors = []
    
    # Price momentum
    if gold_data['change_percent'] > 2:
        sentiment_score += 0.3
        factors.append("Strong upward momentum")
    elif gold_data['change_percent'] > 0:
        sentiment_score += 0.1
        factors.append("Positive momentum")
    elif gold_data['change_percent'] < -2:
        sentiment_score -= 0.3
        factors.append("Strong downward momentum")
    elif gold_data['change_percent'] < 0:
        sentiment_score -= 0.1
        factors.append("Negative momentum")
    
    # Volume analysis
    if gold_data['volume'] > 50000000:  # High volume
        sentiment_score += 0.2
        factors.append("High trading volume")
    elif gold_data['volume'] < 20000000:  # Low volume
        sentiment_score -= 0.1
        factors.append("Low trading volume")
    
    # Price position relative to day's range
    day_range = gold_data['high'] - gold_data['low']
    if day_range > 0:
        price_position = (gold_data['current_price'] - gold_data['low']) / day_range
        if price_position > 0.8:
            sentiment_score += 0.2
            factors.append("Trading near day's high")
        elif price_position < 0.2:
            sentiment_score -= 0.2
            factors.append("Trading near day's low")
    
    # Circuit limit proximity
    if gold_data['current_price'] > gold_data['upper_circuit'] * 0.98:
        sentiment_score -= 0.3
        factors.append("Near upper circuit limit")
    elif gold_data['current_price'] < gold_data['lower_circuit'] * 1.02:
        sentiment_score += 0.3
        factors.append("Near lower circuit limit")
    
    # Add prediction data if available
    if prediction_data and 'news_sentiment' in prediction_data:
        news_sentiment = prediction_data['news_sentiment']
        sentiment_score += news_sentiment * 0.5
        if news_sentiment > 0.3:
            factors.append("Positive news sentiment")
        elif news_sentiment < -0.3:
            factors.append("Negative news sentiment")
    
    # Determine recommendation
    if sentiment_score > 0.3:
        recommendation = "BUY"
        recommendation_class = "buy"
    elif sentiment_score < -0.3:
        recommendation = "SELL"
        recommendation_class = "sell"
    else:
        recommendation = "HOLD"
        recommendation_class = "hold"
    
    return recommendation, sentiment_score, factors

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🥇 Gold Trading Dashboard", className="header"),
        html.P("Real-Time Gold Price Analysis & Trading Recommendations", className="header")
    ]),
    
    # Status indicator
    html.Div([
        html.Span(className="status-indicator status-online", id="status-indicator"),
        html.Span("Live Market Data", id="status-text", style={'fontWeight': 'bold', 'color': '#4CAF50'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Price information grid
    html.Div([
        html.Div([
            html.Div("Current Price", className="price-label"),
            html.Div(id="current-price", className="price-value")
        ], className="price-card current-price"),
        
        html.Div([
            html.Div("Today's Open", className="price-label"),
            html.Div(id="open-price", className="price-value")
        ], className="price-card"),
        
        html.Div([
            html.Div("Previous Close", className="price-label"),
            html.Div(id="close-price", className="price-value")
        ], className="price-card"),
        
        html.Div([
            html.Div("Upper Circuit", className="price-label"),
            html.Div(id="upper-circuit", className="price-value")
        ], className="price-card circuit-limit"),
        
        html.Div([
            html.Div("Lower Circuit", className="price-label"),
            html.Div(id="lower-circuit", className="price-value")
        ], className="price-card circuit-limit")
    ], className="price-grid"),
    
    # Sentiment analysis and recommendation
    html.Div([
        html.H2("📊 Trading Recommendation", className="sentiment-title"),
        html.Div(id="recommendation", className="recommendation"),
        html.Div([
            html.Div([
                html.Div("Sentiment Score", className="sentiment-label"),
                html.Div(id="sentiment-score", className="sentiment-value")
            ], className="sentiment-item"),
            html.Div([
                html.Div("Price Change", className="sentiment-label"),
                html.Div(id="price-change", className="sentiment-value")
            ], className="sentiment-item"),
            html.Div([
                html.Div("Volume", className="sentiment-label"),
                html.Div(id="volume", className="sentiment-value")
            ], className="sentiment-item"),
            html.Div([
                html.Div("Day's Range", className="sentiment-label"),
                html.Div(id="day-range", className="sentiment-value")
            ], className="sentiment-item")
        ], className="sentiment-details"),
        html.Div(id="sentiment-factors", style={'marginTop': '20px', 'textAlign': 'left'})
    ], className="sentiment-section"),
    
    # Market information
    html.Div([
        html.H3("📈 Market Information"),
        html.Div(id="market-info", className="info-grid")
    ], className="market-info"),
    
    # Price chart
    html.Div([
        html.H3("📊 Gold Price Chart", className="chart-title"),
        dcc.Graph(id="price-chart", style={'height': '400px'})
    ], className="chart-container"),
    
    # Last update
    html.Div([
        html.Div(id="last-update", className="last-update")
    ]),
    
    # Auto-refresh component
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    )
])

@callback(
    [Output('current-price', 'children'),
     Output('open-price', 'children'),
     Output('close-price', 'children'),
     Output('upper-circuit', 'children'),
     Output('lower-circuit', 'children'),
     Output('recommendation', 'children'),
     Output('recommendation', 'className'),
     Output('sentiment-score', 'children'),
     Output('price-change', 'children'),
     Output('volume', 'children'),
     Output('day-range', 'children'),
     Output('sentiment-factors', 'children'),
     Output('market-info', 'children'),
     Output('price-chart', 'figure'),
     Output('last-update', 'children'),
     Output('status-indicator', 'className'),
     Output('status-text', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    """Update the dashboard with latest data"""
    
    # Get gold data
    gold_data = get_gold_data()
    
    if not gold_data:
        return (
            "Error", "Error", "Error", "Error", "Error",
            "ERROR", "recommendation", "Error", "Error", "Error", "Error",
            html.Div("Unable to fetch data", style={'color': '#F44336'}),
            [], {}, "Error", "status-indicator status-offline", "Data Error"
        )
    
    # Get prediction data if available
    prediction_data = None
    try:
        if os.path.exists('realtime_predictions.json'):
            with open('realtime_predictions.json', 'r') as f:
                prediction_data = json.load(f)
    except:
        pass
    
    # Analyze sentiment and get recommendation
    recommendation, sentiment_score, factors = analyze_sentiment_and_recommendation(gold_data, prediction_data)
    
    # Format recommendation class
    rec_class = f"recommendation {recommendation.lower()}"
    
    # Format price change
    change_str = f"{gold_data['change']:+.2f} ({gold_data['change_percent']:+.2f}%)"
    change_color = "#4CAF50" if gold_data['change'] > 0 else "#F44336" if gold_data['change'] < 0 else "#666"
    
    # Format volume
    volume_str = f"{gold_data['volume']:,}"
    
    # Format day's range
    day_range = gold_data['high'] - gold_data['low']
    range_str = f"${gold_data['low']:.2f} - ${gold_data['high']:.2f}"
    
    # Sentiment factors
    factors_html = html.Div([
        html.H4("Analysis Factors:", style={'marginBottom': '10px', 'color': '#1e3c72'}),
        html.Ul([html.Li(factor) for factor in factors], style={'textAlign': 'left', 'color': '#666'})
    ])
    
    # Market info
    market_info = [
        html.Div([
            html.Div("High", className="info-label"),
            html.Div(f"${gold_data['high']:.2f}", className="info-value")
        ], className="info-item"),
        html.Div([
            html.Div("Low", className="info-label"),
            html.Div(f"${gold_data['low']:.2f}", className="info-value")
        ], className="info-item"),
        html.Div([
            html.Div("Change", className="info-label"),
            html.Div(change_str, className="info-value", style={'color': change_color})
        ], className="info-item"),
        html.Div([
            html.Div("Volume", className="info-label"),
            html.Div(volume_str, className="info-value")
        ], className="info-item")
    ]
    
    # Create price chart
    try:
        gld = yf.Ticker("GLD")
        hist = gld.history(period="5d", interval="1h")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist['Close'],
            mode='lines',
            name='Gold Price',
            line=dict(color='#FFD700', width=3)
        ))
        
        # Add circuit limits
        fig.add_hline(y=gold_data['upper_circuit'], line_dash="dash", line_color="red", 
                     annotation_text="Upper Circuit", annotation_position="top right")
        fig.add_hline(y=gold_data['lower_circuit'], line_dash="dash", line_color="green", 
                     annotation_text="Lower Circuit", annotation_position="bottom right")
        
        fig.update_layout(
            title='Gold Price (GLD) - 5 Day Chart',
            xaxis_title='Time',
            yaxis_title='Price ($)',
            template='plotly_white',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1e3c72')
        )
    except:
        fig = {}
    
    return (
        f"${gold_data['current_price']:.2f}",
        f"${gold_data['open_price']:.2f}",
        f"${gold_data['close_price']:.2f}",
        f"${gold_data['upper_circuit']:.2f}",
        f"${gold_data['lower_circuit']:.2f}",
        recommendation,
        rec_class,
        f"{sentiment_score:.2f}",
        change_str,
        volume_str,
        range_str,
        factors_html,
        market_info,
        fig,
        f"Last updated: {gold_data['timestamp']}",
        "status-indicator status-online",
        "Live Market Data"
    )

if __name__ == '__main__':
    print("🚀 Starting Gold Trading Dashboard...")
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
    print("🥇 Features: Current price, circuit limits, sentiment analysis, buy/hold/sell recommendations")
    print("=" * 70)
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8050)
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        print("Trying alternative port...")
        try:
            app.run(debug=True, host='127.0.0.1', port=8051)
            print("📊 Dashboard available at: http://127.0.0.1:8051")
        except Exception as e2:
            print(f"❌ Error on alternative port: {e2}")
