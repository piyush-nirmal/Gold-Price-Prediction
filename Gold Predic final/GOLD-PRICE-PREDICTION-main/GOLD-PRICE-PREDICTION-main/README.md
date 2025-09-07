# Gold Price Prediction System

A comprehensive real-time gold price prediction system using machine learning, sentiment analysis, and web dashboard.

## 🚀 Features

- **Machine Learning Model**: Random Forest Regressor with 98.7% accuracy
- **Real-time Data**: Live market data from multiple sources
- **Sentiment Analysis**: News sentiment analysis for better predictions
- **Interactive Dashboard**: Web-based dashboard with real-time updates
- **Technical Indicators**: Comprehensive technical analysis
- **Alert System**: Price and volatility alerts
- **Multiple APIs**: Integration with Yahoo Finance, Alpha Vantage, and more

## 📊 Model Performance

- **R² Score**: 0.987 (98.7% accuracy)
- **Algorithm**: Random Forest Regressor
- **Features**: SPX, USO, SLV, EUR/USD
- **Target**: GLD (Gold ETF)

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Git

### Setup
1. Clone the repository:
```bash
git clone https://github.com/piyush-nirmal/Gold-Price-Prediction.git
cd Gold-Price-Prediction
```

2. Install required packages:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn yfinance plotly dash requests beautifulsoup4 textblob schedule
```

3. (Optional) Set up API keys for enhanced features:
```bash
export ALPHA_VANTAGE_API_KEY='your_key_here'
export QUANDL_API_KEY='your_key_here'
export FINNHUB_API_KEY='your_key_here'
```

## 🎯 Usage

### Basic Prediction
Run the basic gold price prediction model:
```bash
python run_gold_prediction.py
```

### Real-time Dashboard
Start the comprehensive trading dashboard:
```bash
python gold_trading_dashboard.py
```
Access the dashboard at: http://127.0.0.1:8050

### Complete Real-time System
Start all components (predictions, news analysis, API monitoring):
```bash
python start_realtime_system.py
```

## 📁 Project Structure

```
Gold-Price-Prediction/
├── run_gold_prediction.py          # Basic ML model training and prediction
├── dashboard.py                    # Real-time prediction dashboard
├── start_realtime_system.py        # Complete real-time system manager
├── realtime_gold_predictor.py      # Real-time prediction engine
├── api_integration.py              # Financial data API integration
├── news_sentiment.py               # News sentiment analysis
├── config.py                       # Configuration settings
├── gld_price_data.csv              # Historical gold price data
├── gold-price-prediction.ipynb     # Jupyter notebook analysis
└── README.md                       # This file
```

## 📈 Generated Visualizations

The system generates several visualization files:
- `actual_vs_predicted.png` - Model performance comparison
- `correlation_heatmap.png` - Feature correlation analysis
- `distribution_comparison.png` - Price distribution analysis
- `feature_importance.png` - Feature importance ranking

## 🔧 Configuration

Edit `config.py` to customize:
- API keys and endpoints
- Prediction intervals
- Alert thresholds
- Dashboard settings
- Model parameters

## 📊 Dashboard Features

- **Real-time Price**: Current gold price with live updates
- **Circuit Limits**: Upper and lower trading limits
- **Sentiment Analysis**: Buy/Hold/Sell recommendations
- **Technical Indicators**: RSI, MACD, Bollinger Bands
- **Price Charts**: Interactive price history
- **Market Data**: Related market indicators

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Dataset source: [Kaggle Gold Price Data](https://www.kaggle.com/altruistdelhite04/gold-price-data)
- Financial data APIs: Yahoo Finance, Alpha Vantage, Quandl
- News sources: Reuters, MarketWatch, Bloomberg, CNBC

## 📞 Contact

Piyush Nirmal - [@piyush-nirmal](https://github.com/piyush-nirmal)

Project Link: [https://github.com/piyush-nirmal/Gold-Price-Prediction](https://github.com/piyush-nirmal/Gold-Price-Prediction)

---

⭐ Star this repository if you found it helpful!