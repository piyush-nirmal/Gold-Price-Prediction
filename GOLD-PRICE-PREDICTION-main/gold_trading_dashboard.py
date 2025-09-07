
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

# Custom CSS for professional dark trading interface
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #0f0f0f 100%);
                color: #e0e0e0;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .main-container {
                background: rgba(20, 20, 20, 0.95);
                margin: 0;
                padding: 20px;
                min-height: 100vh;
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding: 30px;
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                border-radius: 20px;
                border: 1px solid rgba(255, 215, 0, 0.3);
                box-shadow: 0 20px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.1);
                position: relative;
                overflow: hidden;
            }
            
            .header::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #FFD700, #FFA500, #FF6B35);
            }
            
            .header h1 {
                margin: 0;
                font-size: 3.2em;
                font-weight: 800;
                background: linear-gradient(135deg, #FFD700 0%, #FFA500 50%, #FF6B35 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                text-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
                letter-spacing: -1px;
            }
            
            .header p {
                margin: 15px 0 0 0;
                font-size: 1.4em;
                color: #b0b0b0;
                font-weight: 400;
            }
            
            .status-bar {
                display: flex;
                justify-content: center;
                align-items: center;
                margin-bottom: 25px;
                padding: 15px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 10px;
                animation: pulse 2s infinite;
            }
            
            .status-online { 
                background: linear-gradient(135deg, #00ff88, #00cc6a);
                box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
            }
            
            .status-offline { 
                background: linear-gradient(135deg, #ff4444, #cc0000);
                box-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
            }
            
            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.5; }
                100% { opacity: 1; }
            }
            
            .price-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            
            .price-card {
                background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
                padding: 25px;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .price-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, #FFD700, #FFA500);
            }
            
            .price-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                border-color: rgba(255, 215, 0, 0.3);
            }
            
            .price-value {
                font-size: 2.4em;
                font-weight: 700;
                color: #ffffff;
                margin: 15px 0;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .price-label {
                color: #a0a0a0;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1.5px;
                font-weight: 600;
            }
            
            .current-price {
                background: linear-gradient(135deg, #1a2e1a 0%, #2d4a2d 100%);
                border-color: rgba(0, 255, 136, 0.3);
            }
            
            .current-price::before {
                background: linear-gradient(90deg, #00ff88, #00cc6a);
            }
            
            .current-price .price-value {
                color: #00ff88;
                font-size: 3.2em;
                text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
            }
            
            .circuit-limit {
                background: linear-gradient(135deg, #2e1a1a 0%, #4a2d2d 100%);
                border-color: rgba(255, 68, 68, 0.3);
            }
            
            .circuit-limit::before {
                background: linear-gradient(90deg, #ff4444, #cc0000);
            }
            
            .circuit-limit .price-value {
                color: #ff4444;
            }
            
            .sentiment-section {
                background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
                padding: 35px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 30px;
                text-align: center;
                box-shadow: 0 15px 30px rgba(0,0,0,0.3);
            }
            
            .sentiment-title {
                font-size: 2.2em;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 25px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .recommendation {
                font-size: 2.8em;
                font-weight: 800;
                padding: 25px;
                border-radius: 20px;
                margin: 25px 0;
                text-shadow: 0 4px 8px rgba(0,0,0,0.4);
                letter-spacing: 2px;
                border: 2px solid rgba(255,255,255,0.2);
            }
            
            .recommendation.buy {
                background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
                color: #000000;
                box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
            }
            
            .recommendation.hold {
                background: linear-gradient(135deg, #ffa500 0%, #ff8c00 100%);
                color: #000000;
                box-shadow: 0 10px 30px rgba(255, 165, 0, 0.3);
            }
            
            .recommendation.sell {
                background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
                color: #ffffff;
                box-shadow: 0 10px 30px rgba(255, 68, 68, 0.3);
            }
            
            .sentiment-details {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-top: 25px;
            }
            
            .sentiment-item {
                background: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 12px;
                border-left: 4px solid #FFD700;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .sentiment-label {
                font-weight: 600;
                color: #a0a0a0;
                margin-bottom: 8px;
                font-size: 0.9em;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .sentiment-value {
                font-size: 1.4em;
                font-weight: 700;
                color: #ffffff;
            }
            
            .chart-container {
                background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
                padding: 30px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 25px;
                box-shadow: 0 15px 30px rgba(0,0,0,0.3);
            }
            
            .chart-title {
                font-size: 1.8em;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 25px;
                text-align: center;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .market-info {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #ffffff;
                padding: 25px;
                border-radius: 20px;
                margin: 25px 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 15px 30px rgba(0,0,0,0.3);
            }
            
            .market-info h3 {
                margin-top: 0;
                text-align: center;
                font-size: 1.6em;
                font-weight: 700;
                margin-bottom: 20px;
            }
            
            .info-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .info-item {
                text-align: center;
                padding: 15px;
                background: rgba(255,255,255,0.05);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);
                transition: all 0.3s ease;
            }
            
            .info-item:hover {
                background: rgba(255,255,255,0.1);
                transform: translateY(-2px);
            }
            
            .info-label {
                font-size: 0.9em;
                opacity: 0.8;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 500;
            }
            
            .info-value {
                font-size: 1.3em;
                font-weight: 700;
            }
            
            .last-update {
                text-align: center;
                color: #a0a0a0;
                font-style: italic;
                margin-top: 25px;
                padding: 20px;
                background: rgba(0, 0, 0, 0.3);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .technical-indicators {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 25px 0;
            }
            
            .indicator-card {
                background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
                padding: 20px;
                border-radius: 16px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                text-align: center;
            }
            
            .indicator-title {
                font-size: 1.1em;
                font-weight: 600;
                color: #a0a0a0;
                margin-bottom: 10px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .indicator-value {
                font-size: 1.8em;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 5px;
            }
            
            .indicator-status {
                font-size: 0.9em;
                font-weight: 500;
                padding: 4px 12px;
                border-radius: 20px;
                display: inline-block;
            }
            
            .status-bullish { background: rgba(0, 255, 136, 0.2); color: #00ff88; }
            .status-bearish { background: rgba(255, 68, 68, 0.2); color: #ff4444; }
            .status-neutral { background: rgba(255, 165, 0, 0.2); color: #ffa500; }
            
            /* Scrollbar styling */
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #1a1a1a;
            }
            
            ::-webkit-scrollbar-thumb {
                background: linear-gradient(135deg, #FFD700, #FFA500);
                border-radius: 4px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: linear-gradient(135deg, #FFA500, #FF6B35);
            }
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
    
    # Status bar
    html.Div([
        html.Span(className="status-indicator status-online", id="status-indicator"),
        html.Span("Live Market Data", id="status-text", style={'fontWeight': '600', 'color': '#00ff88', 'fontSize': '1.1em'})
    ], className="status-bar"),
    
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
        dcc.Graph(id="price-chart", style={'height': '500px'})
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
            html.Div("Unable to fetch data", style={'color': '#ff4444'}),
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
        html.H4("Analysis Factors:", style={'marginBottom': '10px', 'color': '#ffffff'}),
        html.Ul([html.Li(factor) for factor in factors], style={'textAlign': 'left', 'color': '#a0a0a0'})
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
    
    # Create simple candlestick chart for 30 days
    try:
        gld = yf.Ticker("GLD")
        hist = gld.history(period="30d", interval="1d")
        
        fig = go.Figure()
        
        # Add simple candlestick chart
        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist['Open'],
            high=hist['High'],
            low=hist['Low'],
            close=hist['Close'],
            name='Gold Price',
            increasing_line_color='#00ff88',
            decreasing_line_color='#ff4444',
            increasing_fillcolor='rgba(0, 255, 136, 0.3)',
            decreasing_fillcolor='rgba(255, 68, 68, 0.3)'
        ))
        
        # Add circuit limits
        fig.add_hline(y=gold_data['upper_circuit'], line_dash="dash", line_color="#ff4444", 
                     annotation_text="Upper Circuit", annotation_position="top right")
        fig.add_hline(y=gold_data['lower_circuit'], line_dash="dash", line_color="#00ff88", 
                     annotation_text="Lower Circuit", annotation_position="bottom right")
        
        fig.update_layout(
            title=dict(
                text='Gold Price (GLD) - 30 Day Candlestick Chart',
                font=dict(size=18, color='#ffffff')
            ),
            xaxis_title='Date',
            yaxis_title='Price ($)',
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0'),
            xaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            showlegend=False
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
    print("🚀 Starting Professional Gold Trading Dashboard...")
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
    print("🥇 Features: Dark theme, simple 30-day candlestick chart")
    print("📈 Real-time data, sentiment analysis, trading recommendations, circuit limits")
    print("🎨 Professional UI with Inter font, animations, and responsive design")
    print("=" * 80)
    
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
