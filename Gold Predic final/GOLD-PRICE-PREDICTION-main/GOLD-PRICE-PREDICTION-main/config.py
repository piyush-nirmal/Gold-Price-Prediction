"""
Configuration File for Real-Time Gold Price Prediction System
============================================================

This file contains all configuration settings, API keys, and parameters
for the real-time gold price prediction system.
"""

import os
from datetime import datetime

class Config:
    """Configuration class for the real-time prediction system"""
    
    # API Keys (Add your actual API keys here)
    API_KEYS = {
        'alpha_vantage': os.getenv('ALPHA_VANTAGE_API_KEY', None),
        'quandl': os.getenv('QUANDL_API_KEY', None),
        'finnhub': os.getenv('FINNHUB_API_KEY', None),
        'news_api': os.getenv('NEWS_API_KEY', None),
        'polygon': os.getenv('POLYGON_API_KEY', None)
    }
    
    # Yahoo Finance Symbols
    SYMBOLS = {
        'SPX': '^GSPC',           # S&P 500
        'GLD': 'GLD',             # Gold ETF
        'USO': 'USO',             # Oil ETF
        'SLV': 'SLV',             # Silver ETF
        'EUR_USD': 'EURUSD=X',    # EUR/USD
        'VIX': '^VIX',            # Volatility Index
        'DXY': 'DX-Y.NYB',        # Dollar Index
        'TLT': 'TLT',             # Treasury Bond ETF
        'QQQ': 'QQQ',             # NASDAQ ETF
        'IWM': 'IWM'              # Russell 2000 ETF
    }
    
    # Prediction Settings
    PREDICTION_SETTINGS = {
        'model_retrain_interval': 24,  # hours
        'prediction_interval': 5,      # minutes
        'data_fetch_interval': 2,      # minutes
        'news_analysis_interval': 10,  # minutes
        'sentiment_weight': 0.1,       # Weight of sentiment in prediction
        'volatility_threshold': 5.0,   # High volatility threshold
        'price_change_threshold': 2.0  # Significant price change threshold
    }
    
    # News Sources
    NEWS_SOURCES = [
        {
            'name': 'Reuters Gold News',
            'url': 'https://www.reuters.com/business/energy/',
            'selector': '.story-title',
            'weight': 0.3
        },
        {
            'name': 'MarketWatch Gold',
            'url': 'https://www.marketwatch.com/investing/future/gc00',
            'selector': '.headline',
            'weight': 0.2
        },
        {
            'name': 'Bloomberg Gold',
            'url': 'https://www.bloomberg.com/markets/commodities',
            'selector': '.headline',
            'weight': 0.2
        },
        {
            'name': 'CNBC Gold',
            'url': 'https://www.cnbc.com/gold/',
            'selector': '.headline',
            'weight': 0.15
        },
        {
            'name': 'Yahoo Finance Gold',
            'url': 'https://finance.yahoo.com/quote/GC=F/',
            'selector': '.headline',
            'weight': 0.15
        }
    ]
    
    # Sentiment Analysis Keywords
    SENTIMENT_KEYWORDS = {
        'gold_related': [
            'gold', 'precious metals', 'bullion', 'GLD', 'gold ETF',
            'inflation', 'fed', 'federal reserve', 'interest rates',
            'dollar', 'USD', 'safe haven', 'economic uncertainty',
            'geopolitical', 'crisis', 'recession', 'market volatility'
        ],
        'positive': [
            'rise', 'increase', 'up', 'gain', 'surge', 'rally',
            'strong', 'positive', 'bullish', 'optimistic', 'growth',
            'demand', 'investment', 'safe haven', 'inflation hedge',
            'breakthrough', 'momentum', 'support', 'resistance'
        ],
        'negative': [
            'fall', 'drop', 'decline', 'down', 'loss', 'crash',
            'weak', 'negative', 'bearish', 'pessimistic', 'recession',
            'crisis', 'uncertainty', 'volatility', 'risk', 'pressure',
            'selloff', 'correction', 'bear market'
        ]
    }
    
    # Technical Indicators Settings
    TECHNICAL_INDICATORS = {
        'sma_periods': [20, 50, 200],
        'ema_periods': [12, 26],
        'rsi_period': 14,
        'macd_fast': 12,
        'macd_slow': 26,
        'macd_signal': 9,
        'bollinger_period': 20,
        'bollinger_std': 2
    }
    
    # Alert Settings
    ALERT_SETTINGS = {
        'price_alerts': {
            'high_threshold': 200.0,
            'low_threshold': 100.0,
            'change_threshold': 5.0
        },
        'volatility_alerts': {
            'high_volatility': 5.0,
            'extreme_volatility': 10.0
        },
        'sentiment_alerts': {
            'strong_positive': 0.5,
            'strong_negative': -0.5
        }
    }
    
    # Dashboard Settings
    DASHBOARD_SETTINGS = {
        'host': '127.0.0.1',
        'port': 8050,
        'debug': True,
        'auto_refresh_interval': 30,  # seconds
        'max_history_points': 100,
        'chart_height': 400
    }
    
    # Data Storage Settings
    DATA_STORAGE = {
        'prediction_history_file': 'realtime_predictions.json',
        'news_sentiment_file': 'news_sentiment.json',
        'market_data_file': 'live_market_data.json',
        'system_status_file': 'system_status.json',
        'model_file': 'gold_prediction_model.pkl',
        'max_file_size_mb': 10,
        'backup_interval_hours': 24
    }
    
    # Logging Settings
    LOGGING = {
        'log_level': 'INFO',
        'log_file': 'gold_predictor.log',
        'max_log_size_mb': 5,
        'backup_count': 5,
        'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
    
    # Rate Limiting Settings
    RATE_LIMITING = {
        'yahoo_finance_delay': 1,      # seconds
        'alpha_vantage_delay': 12,     # seconds (5 calls per minute)
        'quandl_delay': 1,             # seconds
        'finnhub_delay': 1,            # seconds
        'news_delay': 2                # seconds
    }
    
    # Model Settings
    MODEL_SETTINGS = {
        'algorithm': 'RandomForestRegressor',
        'n_estimators': 100,
        'random_state': 0,
        'test_size': 0.2,
        'features': ['SPX', 'USO', 'SLV', 'EUR/USD'],
        'target': 'GLD',
        'outlier_threshold': 0.98
    }
    
    # Market Hours (UTC)
    MARKET_HOURS = {
        'gold_futures': {
            'open': '00:00',
            'close': '23:59',
            'timezone': 'UTC'
        },
        'stock_market': {
            'open': '14:30',  # 9:30 AM EST
            'close': '21:00',  # 4:00 PM EST
            'timezone': 'UTC'
        }
    }
    
    @classmethod
    def get_api_key(cls, service):
        """Get API key for a service"""
        return cls.API_KEYS.get(service)
    
    @classmethod
    def is_market_open(cls):
        """Check if markets are open"""
        now = datetime.utcnow()
        current_time = now.strftime('%H:%M')
        
        # Simple check - in production, you'd use proper timezone handling
        return True  # For now, assume markets are always open
    
    @classmethod
    def get_symbol(cls, name):
        """Get symbol for a market indicator"""
        return cls.SYMBOLS.get(name)
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        errors = []
        
        # Check required settings
        if not cls.SYMBOLS:
            errors.append("No symbols configured")
        
        if not cls.PREDICTION_SETTINGS:
            errors.append("No prediction settings configured")
        
        # Check API keys (optional)
        missing_apis = [k for k, v in cls.API_KEYS.items() if v is None]
        if missing_apis:
            print(f"⚠️ Missing API keys: {', '.join(missing_apis)}")
            print("   Some features may not work without these keys")
        
        return errors

# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development configuration"""
    DASHBOARD_SETTINGS = Config.DASHBOARD_SETTINGS.copy()
    DASHBOARD_SETTINGS['debug'] = True
    
    LOGGING = Config.LOGGING.copy()
    LOGGING['log_level'] = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DASHBOARD_SETTINGS = Config.DASHBOARD_SETTINGS.copy()
    DASHBOARD_SETTINGS['debug'] = False
    
    LOGGING = Config.LOGGING.copy()
    LOGGING['log_level'] = 'WARNING'

# Configuration factory
def get_config(environment='development'):
    """Get configuration based on environment"""
    if environment == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()

# Example usage and setup instructions
def setup_instructions():
    """Print setup instructions"""
    print("🔧 REAL-TIME GOLD PRICE PREDICTION SYSTEM SETUP")
    print("=" * 60)
    print("\n📋 SETUP INSTRUCTIONS:")
    print("1. Install required packages:")
    print("   pip install yfinance schedule requests beautifulsoup4 textblob flask plotly dash")
    print("\n2. Configure API keys (optional but recommended):")
    print("   - Set environment variables:")
    print("     export ALPHA_VANTAGE_API_KEY='your_key_here'")
    print("     export QUANDL_API_KEY='your_key_here'")
    print("     export FINNHUB_API_KEY='your_key_here'")
    print("\n3. Run the system:")
    print("   python start_realtime_system.py")
    print("\n4. Access the dashboard:")
    print("   http://127.0.0.1:8050")
    print("\n📊 FEATURES:")
    print("✅ Real-time market data fetching")
    print("✅ News sentiment analysis")
    print("✅ Technical indicators")
    print("✅ Price predictions")
    print("✅ Web dashboard")
    print("✅ Alert system")
    print("✅ Data logging")
    print("\n🔑 API KEY SOURCES:")
    print("• Alpha Vantage: https://www.alphavantage.co/support/#api-key")
    print("• Quandl: https://www.quandl.com/account/api")
    print("• Finnhub: https://finnhub.io/register")

if __name__ == "__main__":
    # Validate configuration
    config = get_config()
    errors = config.validate_config()
    
    if errors:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"   - {error}")
    else:
        print("✅ Configuration is valid!")
    
    # Show setup instructions
    setup_instructions()
