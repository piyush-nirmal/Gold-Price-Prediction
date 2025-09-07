
"""
API Integration Module for Real-Time Gold Price Prediction
========================================================

This module provides integration with various financial APIs
for real-time data fetching and market analysis.
"""

import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
import warnings
warnings.filterwarnings('ignore')

class FinancialDataAPI:
    def __init__(self):
        """Initialize the financial data API integration"""
        self.api_keys = {
            'alpha_vantage': None,  # Add your API key here
            'quandl': None,         # Add your API key here
            'finnhub': None         # Add your API key here
        }
        
        # Rate limiting
        self.last_request_time = {}
        self.request_delay = 1  # seconds between requests
        
        print("🔌 Financial Data API Integration Initialized!")
    
    def rate_limit(self, api_name):
        """Implement rate limiting for API requests"""
        current_time = time.time()
        if api_name in self.last_request_time:
            time_since_last = current_time - self.last_request_time[api_name]
            if time_since_last < self.request_delay:
                time.sleep(self.request_delay - time_since_last)
        
        self.last_request_time[api_name] = time.time()
    
    def fetch_yahoo_finance_data(self, symbols, period="1d", interval="1m"):
        """Fetch data from Yahoo Finance"""
        try:
            self.rate_limit('yahoo_finance')
            print(f"📈 Fetching Yahoo Finance data for {symbols}...")
            
            data = {}
            for symbol in symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period=period, interval=interval)
                    
                    if not hist.empty:
                        latest = hist.iloc[-1]
                        data[symbol] = {
                            'price': float(latest['Close']),
                            'open': float(latest['Open']),
                            'high': float(latest['High']),
                            'low': float(latest['Low']),
                            'volume': int(latest['Volume']),
                            'change': float(latest['Close'] - latest['Open']),
                            'change_percent': float((latest['Close'] - latest['Open']) / latest['Open'] * 100),
                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        print(f"  ✅ {symbol}: ${latest['Close']:.2f}")
                    else:
                        print(f"  ⚠️ No data for {symbol}")
                        data[symbol] = None
                        
                except Exception as e:
                    print(f"  ❌ Error fetching {symbol}: {e}")
                    data[symbol] = None
            
            return data
            
        except Exception as e:
            print(f"❌ Error fetching Yahoo Finance data: {e}")
            return {}
    
    def fetch_alpha_vantage_data(self, symbol, function="GLOBAL_QUOTE"):
        """Fetch data from Alpha Vantage API"""
        if not self.api_keys['alpha_vantage']:
            print("⚠️ Alpha Vantage API key not configured")
            return None
        
        try:
            self.rate_limit('alpha_vantage')
            print(f"📊 Fetching Alpha Vantage data for {symbol}...")
            
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': function,
                'symbol': symbol,
                'apikey': self.api_keys['alpha_vantage']
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'price': float(quote['05. price']),
                    'change': float(quote['09. change']),
                    'change_percent': float(quote['10. change percent'].rstrip('%')),
                    'volume': int(quote['06. volume']),
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                print(f"  ⚠️ No data returned for {symbol}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching Alpha Vantage data: {e}")
            return None
    
    def fetch_quandl_data(self, dataset, symbol):
        """Fetch data from Quandl API"""
        if not self.api_keys['quandl']:
            print("⚠️ Quandl API key not configured")
            return None
        
        try:
            self.rate_limit('quandl')
            print(f"📊 Fetching Quandl data for {symbol}...")
            
            url = f"https://www.quandl.com/api/v3/datasets/{dataset}/{symbol}.json"
            params = {
                'api_key': self.api_keys['quandl'],
                'limit': 1
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'dataset' in data and 'data' in data['dataset']:
                latest_data = data['dataset']['data'][0]
                return {
                    'price': float(latest_data[1]),  # Assuming price is in second column
                    'timestamp': latest_data[0],  # Date in first column
                    'source': 'Quandl'
                }
            else:
                print(f"  ⚠️ No data returned for {symbol}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching Quandl data: {e}")
            return None
    
    def fetch_finnhub_data(self, symbol):
        """Fetch data from Finnhub API"""
        if not self.api_keys['finnhub']:
            print("⚠️ Finnhub API key not configured")
            return None
        
        try:
            self.rate_limit('finnhub')
            print(f"📊 Fetching Finnhub data for {symbol}...")
            
            url = f"https://finnhub.io/api/v1/quote"
            params = {
                'symbol': symbol,
                'token': self.api_keys['finnhub']
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'c' in data:  # Current price
                return {
                    'price': float(data['c']),
                    'change': float(data['d']),  # Change
                    'change_percent': float(data['dp']),  # Change percent
                    'high': float(data['h']),  # High
                    'low': float(data['l']),  # Low
                    'open': float(data['o']),  # Open
                    'previous_close': float(data['pc']),  # Previous close
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                print(f"  ⚠️ No data returned for {symbol}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching Finnhub data: {e}")
            return None
    
    def get_comprehensive_market_data(self):
        """Get comprehensive market data from multiple sources"""
        print("🌐 Fetching comprehensive market data...")
        
        # Define symbols to fetch
        symbols = {
            'yahoo': ['^GSPC', 'GLD', 'USO', 'SLV', 'EURUSD=X'],
            'alpha_vantage': ['GLD', 'SPY', 'USO'],
            'finnhub': ['GLD', 'SPY', 'USO']
        }
        
        comprehensive_data = {
            'yahoo_finance': {},
            'alpha_vantage': {},
            'finnhub': {},
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Fetch from Yahoo Finance (primary source)
        yahoo_data = self.fetch_yahoo_finance_data(symbols['yahoo'])
        comprehensive_data['yahoo_finance'] = yahoo_data
        
        # Fetch from Alpha Vantage (if API key available)
        if self.api_keys['alpha_vantage']:
            for symbol in symbols['alpha_vantage']:
                av_data = self.fetch_alpha_vantage_data(symbol)
                if av_data:
                    comprehensive_data['alpha_vantage'][symbol] = av_data
        
        # Fetch from Finnhub (if API key available)
        if self.api_keys['finnhub']:
            for symbol in symbols['finnhub']:
                fh_data = self.fetch_finnhub_data(symbol)
                if fh_data:
                    comprehensive_data['finnhub'][symbol] = fh_data
        
        return comprehensive_data
    
    def get_historical_data(self, symbol, period="1mo", interval="1d"):
        """Get historical data for analysis"""
        try:
            print(f"📊 Fetching historical data for {symbol}...")
            
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            
            if not hist.empty:
                return {
                    'data': hist,
                    'symbol': symbol,
                    'period': period,
                    'interval': interval,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                print(f"  ⚠️ No historical data for {symbol}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching historical data: {e}")
            return None
    
    def calculate_technical_indicators(self, data):
        """Calculate technical indicators from price data"""
        try:
            if data is None or data['data'].empty:
                return None
            
            df = data['data'].copy()
            
            # Simple Moving Averages
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()
            
            # Exponential Moving Averages
            df['EMA_12'] = df['Close'].ewm(span=12).mean()
            df['EMA_26'] = df['Close'].ewm(span=26).mean()
            
            # MACD
            df['MACD'] = df['EMA_12'] - df['EMA_26']
            df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
            
            # RSI
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            df['BB_Middle'] = df['Close'].rolling(window=20).mean()
            bb_std = df['Close'].rolling(window=20).std()
            df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            
            return {
                'data': df,
                'symbol': data['symbol'],
                'indicators': {
                    'SMA_20': df['SMA_20'].iloc[-1] if not pd.isna(df['SMA_20'].iloc[-1]) else None,
                    'SMA_50': df['SMA_50'].iloc[-1] if not pd.isna(df['SMA_50'].iloc[-1]) else None,
                    'RSI': df['RSI'].iloc[-1] if not pd.isna(df['RSI'].iloc[-1]) else None,
                    'MACD': df['MACD'].iloc[-1] if not pd.isna(df['MACD'].iloc[-1]) else None
                },
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            print(f"❌ Error calculating technical indicators: {e}")
            return None
    
    def save_api_data(self, data, filename="api_data.json"):
        """Save API data to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            print(f"💾 API data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving API data: {e}")

def main():
    """Test the API integration"""
    print("🌟 Testing Financial Data API Integration")
    print("=" * 60)
    
    api = FinancialDataAPI()
    
    # Test Yahoo Finance data
    print("\n1. Testing Yahoo Finance API...")
    yahoo_data = api.fetch_yahoo_finance_data(['GLD', '^GSPC', 'USO'])
    
    # Test comprehensive data
    print("\n2. Testing Comprehensive Data Fetching...")
    comprehensive_data = api.get_comprehensive_market_data()
    
    # Test historical data
    print("\n3. Testing Historical Data...")
    hist_data = api.get_historical_data('GLD', period="1mo")
    
    # Test technical indicators
    if hist_data:
        print("\n4. Testing Technical Indicators...")
        tech_data = api.calculate_technical_indicators(hist_data)
        if tech_data:
            print("  📊 Technical Indicators:")
            for indicator, value in tech_data['indicators'].items():
                if value is not None:
                    print(f"    {indicator}: {value:.2f}")
    
    # Save data
    api.save_api_data(comprehensive_data)
    
    print("\n✅ API Integration Test Complete!")

if __name__ == "__main__":
    main()
