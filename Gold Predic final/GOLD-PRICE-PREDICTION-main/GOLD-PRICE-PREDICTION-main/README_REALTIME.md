# 🌟 Real-Time Gold Price Prediction System

A comprehensive real-time gold price prediction system that combines machine learning, live market data, news sentiment analysis, and interactive dashboards.

## 🚀 Features

### Core Functionality
- **Real-Time Data Fetching**: Live market data from multiple sources
- **Machine Learning Predictions**: Trained Random Forest model for gold price prediction
- **News Sentiment Analysis**: Automated analysis of gold-related news sentiment
- **Technical Indicators**: RSI, MACD, Moving Averages, Bollinger Bands
- **Interactive Dashboard**: Real-time web dashboard with charts and alerts
- **Alert System**: Price, volatility, and sentiment-based alerts
- **Scheduled Updates**: Configurable intervals for data updates

### Data Sources
- **Yahoo Finance**: Primary data source for market prices
- **Alpha Vantage**: Alternative data source (API key required)
- **Quandl**: Economic and financial data (API key required)
- **Finnhub**: Real-time market data (API key required)
- **News Sources**: Reuters, MarketWatch, Bloomberg, CNBC

## 📋 Prerequisites

### Required Packages
```bash
pip install yfinance schedule requests beautifulsoup4 textblob flask plotly dash pandas numpy scikit-learn matplotlib seaborn
```

### Optional API Keys
For enhanced functionality, obtain API keys from:
- [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- [Quandl](https://www.quandl.com/account/api)
- [Finnhub](https://finnhub.io/register)

Set environment variables:
```bash
export ALPHA_VANTAGE_API_KEY='your_key_here'
export QUANDL_API_KEY='your_key_here'
export FINNHUB_API_KEY='your_key_here'
```

## 🏃‍♂️ Quick Start

### 1. Start the Complete System
```bash
python start_realtime_system.py
```
Choose option 1 to start all components.

### 2. Access the Dashboard
Open your browser and go to: `http://127.0.0.1:8050`

### 3. Monitor Predictions
The system will automatically:
- Fetch live market data every 2 minutes
- Make predictions every 5 minutes
- Analyze news sentiment every 10 minutes
- Update the dashboard every 30 seconds

## 📁 File Structure

```
GOLD-PRICE-PREDICTION-main/
├── realtime_gold_predictor.py      # Main prediction engine
├── dashboard.py                     # Web dashboard
├── news_sentiment.py               # News sentiment analysis
├── api_integration.py              # API data fetching
├── start_realtime_system.py        # System startup script
├── config.py                       # Configuration settings
├── run_gold_prediction.py          # Original static prediction
├── gld_price_data.csv              # Historical training data
└── README_REALTIME.md              # This file
```

## 🔧 Configuration

### Prediction Settings
Edit `config.py` to customize:
- Update intervals
- Alert thresholds
- Model parameters
- API settings

### Dashboard Settings
- Host: `127.0.0.1`
- Port: `8050`
- Auto-refresh: 30 seconds

## 📊 System Components

### 1. Prediction Engine (`realtime_gold_predictor.py`)
- Fetches live market data
- Makes ML-based predictions
- Adjusts predictions based on sentiment
- Generates alerts
- Saves prediction history

### 2. Web Dashboard (`dashboard.py`)
- Real-time price charts
- Market data display
- Alert notifications
- Prediction history
- Auto-refreshing interface

### 3. News Sentiment Analyzer (`news_sentiment.py`)
- Fetches gold-related news
- Analyzes sentiment using TextBlob
- Keyword-based sentiment scoring
- Market indicator analysis

### 4. API Integration (`api_integration.py`)
- Multiple data source integration
- Rate limiting
- Technical indicator calculation
- Data validation and storage

### 5. System Manager (`start_realtime_system.py`)
- Component orchestration
- Process management
- System monitoring
- Status reporting

## 📈 Usage Examples

### Single Prediction
```python
from realtime_gold_predictor import RealTimeGoldPredictor

predictor = RealTimeGoldPredictor()
result = predictor.run_prediction_cycle()
print(f"Predicted Gold Price: ${result['predicted_price']:.2f}")
```

### News Sentiment Analysis
```python
from news_sentiment import NewsSentimentAnalyzer

analyzer = NewsSentimentAnalyzer()
sentiment = analyzer.analyze_news_sentiment()
print(f"News Sentiment: {sentiment['overall_sentiment']:.3f}")
```

### API Data Fetching
```python
from api_integration import FinancialDataAPI

api = FinancialDataAPI()
data = api.fetch_yahoo_finance_data(['GLD', '^GSPC', 'USO'])
print(data)
```

## 🔔 Alert System

The system generates alerts for:
- **Price Alerts**: High (>$200) or Low (<$100) predictions
- **Volatility Alerts**: High market volatility detected
- **Sentiment Alerts**: Strong positive/negative sentiment
- **Data Quality Alerts**: Missing or invalid data

## 📊 Data Files

The system creates several data files:
- `realtime_predictions.json`: Latest predictions and history
- `news_sentiment.json`: Sentiment analysis results
- `live_market_data.json`: Current market data
- `system_status.json`: System status and health

## 🛠️ Troubleshooting

### Common Issues

1. **No Data Available**
   - Check internet connection
   - Verify API keys (if using premium sources)
   - Check market hours

2. **Dashboard Not Loading**
   - Ensure port 8050 is available
   - Check firewall settings
   - Verify all packages are installed

3. **Prediction Errors**
   - Ensure training data is available
   - Check model file integrity
   - Verify feature data quality

### Debug Mode
Run individual components for testing:
```bash
python start_realtime_system.py
# Choose option 6 for component testing
```

## 📚 API Documentation

### RealTimeGoldPredictor Class
```python
class RealTimeGoldPredictor:
    def __init__(self)
    def fetch_live_market_data(self)
    def predict_gold_price(self)
    def run_prediction_cycle(self)
    def start_scheduled_predictions(self, interval_minutes)
```

### NewsSentimentAnalyzer Class
```python
class NewsSentimentAnalyzer:
    def __init__(self)
    def analyze_news_sentiment(self)
    def get_market_sentiment_indicators(self)
```

### FinancialDataAPI Class
```python
class FinancialDataAPI:
    def __init__(self)
    def fetch_yahoo_finance_data(self, symbols)
    def get_comprehensive_market_data(self)
    def calculate_technical_indicators(self, data)
```

## 🔒 Security Considerations

- API keys are stored as environment variables
- Rate limiting prevents API abuse
- Input validation for all data sources
- Error handling for network issues

## 📈 Performance Optimization

- Caching for frequently accessed data
- Asynchronous data fetching
- Efficient data structures
- Memory management for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational and research purposes. Please ensure compliance with API terms of service when using external data sources.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the configuration settings
3. Test individual components
4. Check system logs

## 🔮 Future Enhancements

- [ ] Additional ML algorithms (LSTM, XGBoost)
- [ ] More news sources and sentiment analysis
- [ ] Mobile app interface
- [ ] Email/SMS alerts
- [ ] Portfolio integration
- [ ] Backtesting framework
- [ ] Cloud deployment
- [ ] Real-time streaming data

---

**⚠️ Disclaimer**: This system is for educational and research purposes only. Do not use for actual trading decisions without proper risk management and professional advice.
