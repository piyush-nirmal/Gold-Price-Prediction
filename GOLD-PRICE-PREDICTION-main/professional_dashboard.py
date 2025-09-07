"""
Professional Gold Price Prediction Dashboard
==========================================

A modern, professional-looking dashboard with beautiful styling,
interactive charts, and real-time updates.
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

# Initialize Dash app with external stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Gold Price Predictor Pro"

# Custom CSS
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
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                margin: 0;
                padding: 0;
                min-height: 100vh;
            }
            .main-container {
                background: rgba(255, 255, 255, 0.95);
                margin: 20px;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
                padding: 30px;
            }
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
                border-radius: 15px;
                color: white;
                box-shadow: 0 10px 20px rgba(255, 107, 53, 0.3);
            }
            .header h1 {
                margin: 0;
                font-size: 2.5em;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .header p {
                margin: 10px 0 0 0;
                font-size: 1.2em;
                opacity: 0.9;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0,0,0,0.1);
                text-align: center;
                border-left: 5px solid #FF6B35;
                transition: transform 0.3s ease;
            }
            .stat-card:hover {
                transform: translateY(-5px);
            }
            .stat-value {
                font-size: 2.5em;
                font-weight: bold;
                color: #2E86AB;
                margin: 10px 0;
            }
            .stat-label {
                color: #666;
                font-size: 1.1em;
                text-transform: uppercase;
                letter-spacing: 1px;
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
                color: #2E86AB;
                margin-bottom: 20px;
                text-align: center;
            }
            .market-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin: 20px 0;
            }
            .market-item {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .market-symbol {
                font-weight: bold;
                font-size: 1.1em;
                margin-bottom: 5px;
            }
            .market-price {
                font-size: 1.3em;
                font-weight: bold;
            }
            .market-change {
                font-size: 0.9em;
                margin-top: 5px;
            }
            .positive { color: #4CAF50; }
            .negative { color: #F44336; }
            .neutral { color: #FFC107; }
            .alert-box {
                background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 5px 15px rgba(255, 107, 53, 0.3);
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
            .last-update {
                text-align: center;
                color: #666;
                font-style: italic;
                margin-top: 20px;
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

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🌟 Gold Price Prediction Pro", className="header"),
        html.P("Real-Time Market Analysis & AI-Powered Predictions", className="header")
    ]),
    
    # Status indicator
    html.Div([
        html.Span(className="status-indicator status-online", id="status-indicator"),
        html.Span("System Online", id="status-text", style={'fontWeight': 'bold', 'color': '#4CAF50'})
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Main stats grid
    html.Div([
        html.Div([
            html.Div("Current Prediction", className="stat-label"),
            html.Div(id="current-prediction", className="stat-value")
        ], className="stat-card"),
        
        html.Div([
            html.Div("Base Prediction", className="stat-label"),
            html.Div(id="base-prediction", className="stat-value")
        ], className="stat-card"),
        
        html.Div([
            html.Div("Sentiment Score", className="stat-label"),
            html.Div(id="sentiment-score", className="stat-value")
        ], className="stat-card"),
        
        html.Div([
            html.Div("Market Status", className="stat-label"),
            html.Div("🟢 Active", className="stat-value", style={'fontSize': '1.5em'})
        ], className="stat-card")
    ], className="stats-grid"),
    
    # Market data section
    html.Div([
        html.H3("📊 Live Market Data", className="chart-title"),
        html.Div(id="market-data", className="market-grid")
    ], className="chart-container"),
    
    # Charts section
    html.Div([
        html.H3("📈 Prediction History", className="chart-title"),
        dcc.Graph(id="prediction-chart", style={'height': '400px'})
    ], className="chart-container"),
    
    html.Div([
        html.H3("📊 Market Indicators", className="chart-title"),
        dcc.Graph(id="market-chart", style={'height': '400px'})
    ], className="chart-container"),
    
    # Alerts section
    html.Div([
        html.H3("🔔 Recent Alerts", className="chart-title"),
        html.Div(id="alerts-display")
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
    [Output('current-prediction', 'children'),
     Output('base-prediction', 'children'),
     Output('sentiment-score', 'children'),
     Output('market-data', 'children'),
     Output('prediction-chart', 'figure'),
     Output('market-chart', 'figure'),
     Output('alerts-display', 'children'),
     Output('last-update', 'children'),
     Output('status-indicator', 'className'),
     Output('status-text', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    """Update the dashboard with latest data"""
    
    # Try to load prediction data
    try:
        if os.path.exists('realtime_predictions.json'):
            with open('realtime_predictions.json', 'r') as f:
                data = json.load(f)
            status_class = "status-indicator status-online"
            status_text = "System Online"
        else:
            # Return default values if no data
            return (
                "Loading...", "Loading...", "Loading...", 
                [html.Div("No data available", style={'textAlign': 'center', 'color': '#666'})],
                {}, {}, 
                [html.Div("No alerts", style={'textAlign': 'center', 'color': '#666'})],
                "Never", "status-indicator status-offline", "System Offline"
            )
    except Exception as e:
        return (
            f"Error: {e}", "Error", "Error",
            [html.Div("Error loading data", style={'textAlign': 'center', 'color': '#F44336'})],
            {}, {},
            [html.Div("System error", style={'textAlign': 'center', 'color': '#F44336'})],
            "Error", "status-indicator status-offline", "System Error"
        )
    
    # Current prediction data
    if data.get('last_prediction'):
        prediction = data['last_prediction']
        current_price = f"${prediction['predicted_price']:.2f}"
        base_price = f"${prediction['base_prediction']:.2f}"
        sentiment = f"{prediction['news_sentiment']:.3f}"
        last_update = prediction['timestamp']
        
        # Market data display
        market_data = prediction.get('market_data', {})
        market_items = []
        for name, data_item in market_data.items():
            if data_item:
                change = data_item.get('change', 0)
                change_class = "positive" if change > 0 else "negative" if change < 0 else "neutral"
                change_str = f"{change:+.2f}" if change != 0 else "0.00"
                
                market_items.append(
                    html.Div([
                        html.Div(name, className="market-symbol"),
                        html.Div(f"${data_item['price']:.2f}", className="market-price"),
                        html.Div(f"({change_str})", className=f"market-change {change_class}")
                    ], className="market-item")
                )
        
        # Prediction history chart
        if data.get('prediction_history'):
            history_df = pd.DataFrame(data['prediction_history'])
            history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
            
            fig_prediction = go.Figure()
            fig_prediction.add_trace(go.Scatter(
                x=history_df['timestamp'],
                y=history_df['predicted_price'],
                mode='lines+markers',
                name='Predicted Price',
                line=dict(color='#FF6B35', width=3),
                marker=dict(size=6, color='#FF6B35')
            ))
            
            fig_prediction.update_layout(
                title='Gold Price Prediction Trend',
                xaxis_title='Time',
                yaxis_title='Price ($)',
                template='plotly_white',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2E86AB'),
                title_font_size=16
            )
        else:
            fig_prediction = {}
        
        # Market data chart
        if market_data:
            market_names = []
            market_prices = []
            colors = ['#FF6B35', '#2E86AB', '#A23B72', '#F7931E', '#4CAF50']
            
            for i, (name, data_item) in enumerate(market_data.items()):
                if data_item:
                    market_names.append(name)
                    market_prices.append(data_item['price'])
            
            fig_market = go.Figure(data=[
                go.Bar(
                    x=market_names,
                    y=market_prices,
                    marker_color=colors[:len(market_names)],
                    text=[f"${price:.2f}" for price in market_prices],
                    textposition='auto'
                )
            ])
            
            fig_market.update_layout(
                title='Current Market Data',
                xaxis_title='Market Indicators',
                yaxis_title='Price',
                template='plotly_white',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2E86AB'),
                title_font_size=16
            )
        else:
            fig_market = {}
        
        # Alerts
        alerts = data.get('alerts', [])
        if alerts:
            alerts_display = []
            for alert in alerts[-5:]:  # Show last 5 alerts
                alerts_display.append(
                    html.Div([
                        html.I(className="fas fa-bell", style={'marginRight': '10px'}),
                        alert
                    ], className="alert-box")
                )
        else:
            alerts_display = [html.Div("No recent alerts", style={'textAlign': 'center', 'color': '#666'})]
        
        return (
            current_price, base_price, sentiment, market_items,
            fig_prediction, fig_market, alerts_display,
            f"Last updated: {last_update}", status_class, status_text
        )
    
    else:
        return (
            "No data", "No data", "No data",
            [html.Div("No data available", style={'textAlign': 'center', 'color': '#666'})],
            {}, {},
            [html.Div("No alerts", style={'textAlign': 'center', 'color': '#666'})],
            "Never", "status-indicator status-offline", "No Data"
        )

if __name__ == '__main__':
    print("🚀 Starting Professional Gold Price Prediction Dashboard...")
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
    print("🎨 Professional styling with modern design")
    print("=" * 60)
    
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
