"""
Simple Test Dashboard for Gold Price Prediction
=============================================
"""

import dash
from dash import dcc, html
import plotly.graph_objs as go
import json
import os
from datetime import datetime

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Gold Price Predictor - Test"

# Simple layout
app.layout = html.Div([
    html.H1("🌟 Gold Price Prediction Dashboard", 
            style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': '30px'}),
    
    html.Div([
        html.H2("Current Prediction", style={'color': '#A23B72'}),
        html.Div(id='current-prediction', 
                style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#FF6B35'})
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    
    html.Div([
        html.H3("Market Data", style={'color': '#A23B72'}),
        html.Div(id='market-data', style={'textAlign': 'center'})
    ], style={'marginBottom': '30px'}),
    
    html.Div([
        html.H3("Last Update", style={'color': '#A23B72'}),
        html.Div(id='last-update', style={'textAlign': 'center'})
    ], style={'marginBottom': '30px'}),
    
    # Auto-refresh component
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    )
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

@app.callback(
    [dash.dependencies.Output('current-prediction', 'children'),
     dash.dependencies.Output('market-data', 'children'),
     dash.dependencies.Output('last-update', 'children')],
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    """Update the dashboard with latest data"""
    
    # Try to load prediction data
    try:
        if os.path.exists('realtime_predictions.json'):
            with open('realtime_predictions.json', 'r') as f:
                data = json.load(f)
        else:
            return "No data available", "No data available", "Never"
    except Exception as e:
        return f"Error: {e}", "Error", "Error"
    
    # Current prediction
    if data.get('last_prediction'):
        prediction = data['last_prediction']
        current_price = f"${prediction['predicted_price']:.2f}"
        last_update = prediction['timestamp']
        
        # Market data
        market_data = prediction.get('market_data', {})
        market_display = []
        for name, data_item in market_data.items():
            if data_item:
                change = data_item.get('change', 0)
                change_str = f"({change:+.2f})" if change != 0 else "(0.00)"
                market_display.append(
                    html.Span([
                        html.Strong(f"{name}: "),
                        f"${data_item['price']:.2f} {change_str}"
                    ], style={'margin': '0 15px', 'display': 'inline-block'})
                )
        
        return current_price, market_display, last_update
    
    else:
        return "No prediction available", "No data available", "Never"

if __name__ == '__main__':
    print("🚀 Starting Simple Gold Price Prediction Dashboard...")
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
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
