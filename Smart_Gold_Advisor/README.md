# Smart Gold Investment Advisor

An AI-powered web application that combines machine learning price forecasting with news sentiment analysis to provide intelligent gold investment recommendations.

## 🌟 Features

- **Real-time Gold Price Tracking**: Live gold price updates from public APIs
- **LSTM Price Prediction**: Advanced time series forecasting using Long Short-Term Memory networks
- **Sentiment Analysis**: News sentiment analysis to gauge market mood
- **Investment Recommendations**: AI-powered Buy/Sell/Hold recommendations with confidence scores
- **Interactive Charts**: Beautiful visualizations of price trends and sentiment analysis
- **Custom Data Upload**: Upload your own datasets to retrain the model
- **Responsive Web Interface**: Modern, mobile-friendly design

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   # If you have the files locally, navigate to the project directory
   cd Smart_Gold_Advisor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the models**
   ```bash
   python train_models.py
   ```

4. **Start the web application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
Smart_Gold_Advisor/
├── app.py                          # Flask web application
├── data_preprocessing.py           # Data cleaning and preprocessing
├── models/
│   └── gold_predictor.py          # LSTM model for price prediction
├── recommendation_engine.py        # Investment recommendation logic
├── train_models.py                # Model training script
├── requirements.txt               # Python dependencies
├── templates/
│   ├── index.html                 # Main dashboard
│   └── dashboard.html             # Advanced analytics
├── static/
│   ├── style.css                  # Custom CSS styles
│   └── app.js                     # Frontend JavaScript
├── FINAL_USO.csv                  # Gold price data
├── gold sentiment.csv             # News sentiment data
└── README.md                      # This file
```

## 🔧 How It Works

### 1. Data Preprocessing
- Loads gold price data (`FINAL_USO.csv`) and news sentiment data (`gold sentiment.csv`)
- Cleans and merges datasets by date
- Converts sentiment labels to numeric scores (-1, 0, 1)
- Aggregates multiple news items per day

### 2. Machine Learning Model
- **LSTM Architecture**: 2-layer LSTM with dropout for regularization
- **Features**: Historical gold prices + sentiment scores
- **Sequence Length**: 30 days of historical data
- **Prediction Horizon**: Next day and next week forecasts

### 3. Investment Recommendations
- Combines price predictions with sentiment analysis
- Generates Buy/Sell/Hold recommendations
- Provides confidence scores and detailed reasoning
- Considers trend alignment and magnitude

### 4. Web Interface
- **Dashboard**: Real-time price, predictions, and recommendations
- **Charts**: Interactive price trends and sentiment analysis
- **Upload**: Custom dataset upload and model retraining
- **Responsive**: Works on desktop and mobile devices

## 📊 Model Performance

The LSTM model is evaluated using:
- **RMSE (Root Mean Square Error)**: Measures prediction accuracy
- **MAE (Mean Absolute Error)**: Average prediction error
- **Validation Split**: 20% of data used for validation

## 🎯 Investment Logic

The recommendation engine uses the following logic:

| Price Trend | Sentiment | Recommendation | Confidence |
|-------------|-----------|----------------|------------|
| Up + Positive | Strong | BUY | High |
| Down + Negative | Strong | SELL | High |
| Up + Negative | Mixed | HOLD | Medium |
| Down + Positive | Mixed | HOLD | Medium |
| Stable + Neutral | Weak | HOLD | Low |

## 🔄 API Endpoints

- `GET /` - Main dashboard
- `GET /api/current_price` - Live gold price
- `GET /api/prediction` - Price predictions and recommendations
- `GET /api/historical_data` - Historical data for charts
- `GET /api/chart_data` - Plotly chart data
- `POST /upload` - Upload custom datasets

## 🔑 Configuration and API Keys

This project uses a few external services. Configure the following as needed:

- **METALPRICE_API_KEY (optional)**: Enables live spot prices via MetalpriceAPI.com.
  - If not set, the app falls back to public/free sources and safe defaults.
- **GEMINI_API_KEY (optional)**: Used by the experimental Indian price helper in `app.py`.
  - Note: The current code configures Gemini using a key defined directly in `app.py`. For production, set it via environment variables and update the code accordingly.

### Set environment variables on Windows PowerShell

```powershell
# From project root after activating your venv
$env:METALPRICE_API_KEY="<your_metalpriceapi_key>"
$env:GEMINI_API_KEY="<your_gemini_key>"
$env:RETAIL_PREMIUM_PCT="0.12"
python app.py
```

You can also see example commands in `SETUP_GUIDE.txt`.

### Optional: Using MetalpriceAPI

When `METALPRICE_API_KEY` is provided, the app will try these endpoints:

- XAU→USD: `https://api.metalpriceapi.com/v1/latest?base=XAU&currencies=USD`
- XAU→INR: `https://api.metalpriceapi.com/v1/latest?base=XAU&currencies=INR`
- USD→INR: `https://api.metalpriceapi.com/v1/latest?base=USD&currencies=INR`

If any request fails or the key is missing, it gracefully falls back to free/public APIs and defaults.

### Security note

Avoid committing API keys to source control. Prefer environment variables. If you plan to use a `.env` file, add it to `.gitignore` and load it with `python-dotenv` (not currently required by this project).

## 📈 Customization

### Adding New Features
1. **New Indicators**: Add technical indicators to the model
2. **Alternative Data**: Include economic indicators, weather data, etc.
3. **Model Improvements**: Try different architectures (GRU, Transformer)
4. **Sentiment Sources**: Add more news sources or social media data

### Modifying Recommendations
Edit `recommendation_engine.py` to adjust:
- Confidence thresholds
- Recommendation logic
- Risk tolerance levels

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Model Training Fails**
   - Check if CSV files exist and are properly formatted
   - Ensure sufficient data (at least 100 days)
   - Run `python train_models.py` to regenerate models

3. **Charts Not Loading**
   - Check browser console for JavaScript errors
   - Ensure Plotly library is loaded
   - Try refreshing the page

4. **Port Already in Use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

### Performance Optimization

- **Reduce Model Complexity**: Lower epochs in training
- **Smaller Dataset**: Use fewer historical days
- **Caching**: Implement Redis for API responses
- **CDN**: Use CDN for static assets

## 📝 Data Format

### Gold Price Data (`FINAL_USO.csv`)
Required columns:
- `Date`: Date in YYYY-MM-DD format
- `SF_Price`: Gold price (Spot Future Price)

### Sentiment Data (`gold sentiment.csv`)
Required columns:
- `Dates`: Date in DD-MM-YYYY format
- `News`: News headline text
- `Sentiment label`: Sentiment classification (positive/negative/neutral/none)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This application is for educational and research purposes only. Investment decisions should not be based solely on automated recommendations. Always consult with financial advisors and conduct your own research before making investment decisions.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue with detailed error messages
4. Include system information (OS, Python version, etc.)

---

**Happy Investing! 🥇**
