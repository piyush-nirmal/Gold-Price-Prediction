# 🥇 Professional Gold Trading Dashboard

A comprehensive real-time gold price prediction and trading dashboard system that combines machine learning, live market data, sentiment analysis, and a professional web interface.

## 🌟 Features

### 🎨 **Professional Dark Theme Interface**
- Sleek black gradient background with gold accents
- Modern Inter font typography
- Animated status indicators with pulsing effects
- Glass-morphism effects with backdrop blur
- Custom scrollbars with gold gradient
- Responsive design with hover animations

### 📊 **Advanced Trading Charts**
- **30-Day Candlestick Chart** - Clean, simple candlestick pattern
- **Real-time Price Updates** - Live data every 30 seconds
- **Circuit Limits** - Upper and lower trading boundaries clearly marked
- **Dark Theme Styling** - Professional trading platform appearance
- **Interactive Charts** - Zoom, pan, and hover functionality

### 🤖 **Machine Learning & Analysis**
- **Random Forest Regressor** with 98.7% accuracy
- **Real-time Sentiment Analysis** - News sentiment integration
- **Trading Recommendations** - BUY/HOLD/SELL based on multiple factors
- **Technical Analysis** - Price momentum, volume analysis, market indicators
- **Risk Assessment** - Circuit limit proximity analysis

### 📈 **Real-Time Data Integration**
- **Yahoo Finance API** - Primary data source for market prices
- **Live Market Data** - Current prices, volume, high/low
- **News Sentiment** - Automated analysis of gold-related news
- **Market Indicators** - SPX, USO, SLV, EUR/USD correlation
- **Auto-refresh** - Dashboard updates every 30 seconds

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Internet connection for live data

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/piyush-nirmal/Gold-Price-Prediction.git
   cd Gold-Price-Prediction
   ```

2. **Install required packages:**
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn yfinance plotly dash requests beautifulsoup4 textblob schedule
   ```

3. **Run the dashboard:**
   ```bash
   python gold_trading_dashboard.py
   ```

4. **Access the dashboard:**
   Open your browser and go to: **http://127.0.0.1:8050**

## 📁 Project Structure

```
Gold-Price-Prediction/
├── gold_trading_dashboard.py      # Main professional dashboard
├── run_gold_prediction.py         # Basic ML model training
├── realtime_gold_predictor.py     # Real-time prediction engine
├── news_sentiment.py              # News sentiment analysis
├── api_integration.py             # Financial data API integration
├── start_realtime_system.py       # Complete system manager
├── config.py                      # Configuration settings
├── dashboard.py                   # Alternative dashboard
├── simple_dashboard.py            # Basic dashboard
├── professional_dashboard.py      # Enhanced dashboard
├── gold-price-prediction.ipynb    # Jupyter notebook analysis
├── gld_price_data.csv             # Historical training data
└── README.md                      # This file
```

## 🎯 Usage Examples

### Start the Professional Dashboard
```bash
python gold_trading_dashboard.py
```
- **URL:** http://127.0.0.1:8050
- **Features:** Dark theme, 30-day candlestick chart, real-time updates

### Run Basic Prediction Model
```bash
python run_gold_prediction.py
```
- Trains Random Forest model
- Generates performance visualizations
- Shows prediction accuracy metrics

### Start Complete Real-Time System
```bash
python start_realtime_system.py
```
- Runs all components simultaneously
- Includes predictions, news analysis, API monitoring
- Comprehensive system management

## 📊 Dashboard Components

### 🎨 **Visual Elements**
- **Header** - Gradient gold title with professional styling
- **Status Bar** - Live connection indicator with animations
- **Price Cards** - Current price, open, close, circuit limits
- **Trading Recommendation** - Large BUY/HOLD/SELL display
- **Sentiment Analysis** - Score and contributing factors
- **Market Information** - High, low, volume, change data
- **Candlestick Chart** - 30-day price history with circuit limits

### 🔧 **Technical Features**
- **Real-time Data Fetching** - Yahoo Finance integration
- **Sentiment Analysis** - News and market sentiment scoring
- **Trading Logic** - Multi-factor recommendation system
- **Error Handling** - Graceful fallbacks and error states
- **Auto-refresh** - 30-second update intervals
- **Responsive Design** - Works on all screen sizes

## 📈 Model Performance

### **Machine Learning Model**
- **Algorithm:** Random Forest Regressor
- **Accuracy:** 98.7% (R² Score: 0.987)
- **Features:** SPX, USO, SLV, EUR/USD
- **Target:** GLD (Gold ETF)
- **Training Data:** Historical gold price data

### **Sentiment Analysis**
- **News Sources:** Reuters, MarketWatch, Bloomberg, CNBC
- **Analysis Method:** TextBlob sentiment scoring
- **Keywords:** Gold-related market terms
- **Integration:** Real-time sentiment affects recommendations

## 🎨 Design Features

### **Dark Theme Elements**
- **Background:** Linear gradient from #0a0a0a to #1a1a1a
- **Cards:** Dark gradients with subtle borders
- **Text:** High contrast white/gray text
- **Accents:** Gold (#FFD700) and green (#00ff88) highlights
- **Animations:** Smooth transitions and hover effects

### **Professional Typography**
- **Font:** Inter (Google Fonts)
- **Weights:** 300-800 range
- **Hierarchy:** Clear size and weight distinctions
- **Spacing:** Consistent letter-spacing and line-height

## 🔧 Configuration

### **Dashboard Settings**
- **Host:** 127.0.0.1
- **Port:** 8050 (fallback: 8051)
- **Update Interval:** 30 seconds
- **Debug Mode:** Enabled

### **Data Sources**
- **Primary:** Yahoo Finance (GLD ticker)
- **Period:** 30 days for charts
- **Interval:** Daily for candlesticks
- **Real-time:** Live market data

## 📊 Generated Files

The system creates several data and visualization files:
- `actual_vs_predicted.png` - Model performance comparison
- `correlation_heatmap.png` - Feature correlation analysis
- `distribution_comparison.png` - Price distribution analysis
- `feature_importance.png` - Feature importance ranking
- `realtime_predictions.json` - Latest predictions and history
- `news_sentiment.json` - Sentiment analysis results
- `live_market_data.json` - Current market data
- `system_status.json` - System status and health

## 🛠️ Troubleshooting

### **Common Issues**

1. **Server Not Starting**
   - Check if port 8050 is available
   - Verify all packages are installed
   - Check for syntax errors in code

2. **No Data Available**
   - Check internet connection
   - Verify Yahoo Finance API access
   - Check market hours

3. **Dashboard Not Loading**
   - Try alternative port: http://127.0.0.1:8051
   - Check firewall settings
   - Clear browser cache

### **Debug Mode**
Run individual components for testing:
```bash
python start_realtime_system.py
# Choose option 6 for component testing
```

## 🔒 Security & Performance

### **Security Considerations**
- API keys stored as environment variables
- Rate limiting prevents API abuse
- Input validation for all data sources
- Error handling for network issues

### **Performance Optimization**
- Caching for frequently accessed data
- Efficient data structures
- Memory management for large datasets
- Asynchronous data fetching

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dataset Source:** [Kaggle Gold Price Data](https://www.kaggle.com/altruistdelhite04/gold-price-data)
- **Financial APIs:** Yahoo Finance, Alpha Vantage, Quandl
- **News Sources:** Reuters, MarketWatch, Bloomberg, CNBC
- **Fonts:** Google Fonts (Inter)
- **Charts:** Plotly Dash

## 📞 Contact

**Piyush Nirmal** - [@piyush-nirmal](https://github.com/piyush-nirmal)

**Project Link:** [https://github.com/piyush-nirmal/Gold-Price-Prediction](https://github.com/piyush-nirmal/Gold-Price-Prediction)

---

## ⚠️ Disclaimer

This system is for educational and research purposes only. Do not use for actual trading decisions without proper risk management and professional advice. The predictions and recommendations are based on historical data and sentiment analysis and should not be considered as financial advice.

---

⭐ **Star this repository if you found it helpful!**

## 🚀 Getting Started

1. **Install dependencies:** `pip install -r requirements.txt`
2. **Run dashboard:** `python gold_trading_dashboard.py`
3. **Open browser:** http://127.0.0.1:8050
4. **Enjoy trading insights!** 🥇📈
