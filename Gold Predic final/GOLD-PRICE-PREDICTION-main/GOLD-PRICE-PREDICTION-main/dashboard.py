"""
Real-Time Gold Price Prediction Dashboard
========================================

A web dashboard to monitor real-time gold price predictions
using Dash and Plotly for interactive visualizations.
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import time

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Real-Time Gold Price Predictor"

# Define the layout
app.layout = html.Div([
    html.Div([
        html.H1("🌟 Real-Time Gold Price Prediction Dashboard", 
                style={'textAlign': 'center', 'color': '#2E86AB', 'marginBottom': '30px'}),
        
        # Current prediction display
        html.Div([
            html.Div([
                html.H3("Current Prediction", style={'color': '#A23B72'}),
                html.Div(id='current-prediction', style={'fontSize': '24px', 'fontWeight': 'bold'})
            ], className='six columns'),
            
            html.Div([
                html.H3("Last Update", style={'color': '#A23B72'}),
                html.Div(id='last-update', style={'fontSize': '18px'})
            ], className='six columns')
        ], className='row', style={'marginBottom': '30px'}),
        
        # Market data display
        html.Div([
            html.H3("Live Market Data", style={'color': '#A23B72', 'textAlign': 'center'}),
            html.Div(id='market-data', style={'textAlign': 'center'})
        ], style={'marginBottom': '30px'}),
        
        # Prediction history chart
        html.Div([
            dcc.Graph(id='prediction-chart')
        ], style={'marginBottom': '30px'}),
        
        # Market data comparison chart
        html.Div([
            dcc.Graph(id='market-chart')
        ], style={'marginBottom': '30px'}),
        
        # Alerts section
        html.Div([
            html.H3("Recent Alerts", style={'color': '#A23B72'}),
            html.Div(id='alerts-display')
        ], style={'marginBottom': '30px'}),
        
        # Auto-refresh component
        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # Update every 30 seconds
            n_intervals=0
        )
    ], style={'padding': '20px'})
])

@callback(
    [Output('current-prediction', 'children'),
     Output('last-update', 'children'),
     Output('market-data', 'children'),
     Output('prediction-chart', 'figure'),
     Output('market-chart', 'figure'),
     Output('alerts-display', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    """Update the dashboard with latest data"""
    
    # Try to load prediction data
    try:
        if os.path.exists('realtime_predictions.json'):
            with open('realtime_predictions.json', 'r') as f:
                data = json.load(f)
        else:
            # Return empty data if file doesn't exist
            return "No data available", "Never", "No data available", {}, {}, "No alerts"
    except Exception as e:
        return f"Error loading data: {e}", "Error", "Error", {}, {}, "Error"
    
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
                    ], style={'margin': '0 10px'})
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
                line=dict(color='#FF6B35', width=3)
            ))
            
            fig_prediction.update_layout(
                title='Gold Price Prediction History',
                xaxis_title='Time',
                yaxis_title='Price ($)',
                template='plotly_white',
                height=400
            )
        else:
            fig_prediction = {}
        
        # Market data chart
        if market_data:
            market_names = []
            market_prices = []
            market_changes = []
            
            for name, data_item in market_data.items():
                if data_item:
                    market_names.append(name)
                    market_prices.append(data_item['price'])
                    market_changes.append(data_item.get('change', 0))
            
            fig_market = go.Figure()
            fig_market.add_trace(go.Bar(
                x=market_names,
                y=market_prices,
                marker_color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
            ))
            
            fig_market.update_layout(
                title='Current Market Data',
                xaxis_title='Market Indicators',
                yaxis_title='Price',
                template='plotly_white',
                height=400
            )
        else:
            fig_market = {}
        
        # Alerts
        alerts = data.get('alerts', [])
        if alerts:
            alerts_display = []
            for alert in alerts[-5:]:  # Show last 5 alerts
                alerts_display.append(
                    html.Div(alert, style={
                        'padding': '10px',
                        'margin': '5px 0',
                        'backgroundColor': '#FFF3CD',
                        'border': '1px solid #FFEAA7',
                        'borderRadius': '5px'
                    })
                )
        else:
            alerts_display = [html.Div("No recent alerts", style={'color': '#666'})]
        
        return current_price, last_update, market_display, fig_prediction, fig_market, alerts_display
    
    else:
        return "No prediction available", "Never", "No data available", {}, {}, "No alerts"

# Add some CSS styling
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
                background-color: #f8f9fa;
            }
            .row {
                display: flex;
                flex-wrap: wrap;
                margin: 0 -15px;
            }
            .six.columns {
                flex: 0 0 50%;
                padding: 0 15px;
            }
            .dash-graph {
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    print("🚀 Starting Real-Time Gold Price Prediction Dashboard...")
    print("📊 Dashboard will be available at: http://127.0.0.1:8050")
    print("🔄 Auto-refreshes every 30 seconds")
    print("=" * 60)
    
    app.run(debug=True, host='127.0.0.1', port=8050)
