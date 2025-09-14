#!/usr/bin/env python3
"""
Training script for Smart Gold Investment Advisor
This script initializes and trains the machine learning models
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_preprocessing import DataPreprocessor
from gold_predictor import GoldPricePredictor
from recommendation_engine import InvestmentRecommendationEngine

def create_directories():
    """Create necessary directories"""
    directories = ['models', 'templates', 'static', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def train_models():
    """Train the machine learning models"""
    print("=" * 60)
    print("SMART GOLD INVESTMENT ADVISOR - MODEL TRAINING")
    print("=" * 60)
    
    try:
        # Step 1: Data Preprocessing
        print("\n1. Loading and preprocessing data...")
        preprocessor = DataPreprocessor()
        
        # Check if CSV files exist
        gold_file = 'data/FINAL_USO.csv'
        sentiment_file = 'data/gold sentiment.csv'
        
        if not os.path.exists(gold_file):
            print(f"Warning: {gold_file} not found. Creating sample data...")
            create_sample_data()
            gold_file = 'sample_gold_data.csv'
            sentiment_file = 'sample_sentiment_data.csv'
        
        # Process data
        processed_data = preprocessor.preprocess_all(gold_file, sentiment_file)
        processed_data.to_csv('processed_gold_data.csv', index=False)
        print(f"✓ Processed data saved to processed_gold_data.csv")
        print(f"✓ Data shape: {processed_data.shape}")
        
        # Step 2: Model Training
        print("\n2. Training Random Forest model...")
        predictor = GoldPricePredictor(sequence_length=30)
        
        # Train with Random Forest
        history = predictor.train_model(processed_data)
        predictor.save_model()
        print("✓ Model trained and saved successfully")
        
        # Step 3: Test Predictions
        print("\n3. Testing predictions...")
        next_day_price = predictor.predict_next_day(processed_data)
        next_week_prices = predictor.predict_next_week(processed_data)
        
        print(f"✓ Next day prediction: ${next_day_price:.2f}")
        print(f"✓ Next week predictions: {[f'${p:.2f}' for p in next_week_prices]}")
        
        # Step 4: Test Recommendation Engine
        print("\n4. Testing recommendation engine...")
        current_price = processed_data['SF_Price'].iloc[-1]
        current_sentiment = processed_data['Sentiment_score'].iloc[-1]
        latest_news = processed_data['News'].iloc[-1]
        
        recommendation_engine = InvestmentRecommendationEngine()
        recommendation = recommendation_engine.generate_recommendation(
            current_price, next_day_price, current_sentiment, latest_news
        )
        
        print(f"✓ Recommendation: {recommendation['recommendation']}")
        print(f"✓ Confidence: {recommendation['confidence']:.2f}")
        
        print("\n" + "=" * 60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nTo start the web application, run:")
        print("python app.py")
        print("\nThen open your browser to: http://localhost:5000")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        print("Creating fallback demo data...")
        create_demo_data()
        return False

def create_sample_data():
    """Create sample data if original files are not available"""
    print("Creating sample gold price data...")
    
    # Create sample gold price data
    dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
    np.random.seed(42)
    
    # Generate realistic gold price data
    base_price = 1800
    trend = np.linspace(0, 200, len(dates))  # Upward trend
    noise = np.random.normal(0, 50, len(dates))
    seasonal = 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25)
    
    prices = base_price + trend + noise + seasonal
    
    gold_data = pd.DataFrame({
        'Date': dates,
        'SF_Price': prices
    })
    
    gold_data.to_csv('sample_gold_data.csv', index=False)
    print("✓ Created sample_gold_data.csv")
    
    # Create sample sentiment data
    sentiment_dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
    sentiments = np.random.choice(['positive', 'negative', 'neutral'], len(sentiment_dates), p=[0.3, 0.3, 0.4])
    
    news_templates = [
        "Gold prices rise on inflation concerns",
        "Economic uncertainty drives gold demand",
        "Federal Reserve policy impacts gold market",
        "Global tensions boost safe-haven demand",
        "Dollar strength weighs on gold prices",
        "Central bank buying supports gold market",
        "Interest rate changes affect gold outlook",
        "Market volatility increases gold appeal"
    ]
    
    news = [np.random.choice(news_templates) for _ in range(len(sentiment_dates))]
    
    sentiment_data = pd.DataFrame({
        'Dates': sentiment_dates.strftime('%d-%m-%Y'),
        'News': news,
        'Sentiment label': sentiments
    })
    
    sentiment_data.to_csv('sample_sentiment_data.csv', index=False)
    print("✓ Created sample_sentiment_data.csv")

def create_demo_data():
    """Create demo data for fallback"""
    print("Creating demo data for fallback...")
    
    dates = pd.date_range(start='2020-01-01', end='2024-01-01', freq='D')
    np.random.seed(42)
    
    processed_data = pd.DataFrame({
        'Date': dates,
        'SF_Price': np.random.normal(1800, 100, len(dates)),
        'Sentiment_score': np.random.normal(0, 0.3, len(dates)),
        'News': ['Sample news'] * len(dates)
    })
    
    processed_data.to_csv('processed_gold_data.csv', index=False)
    print("✓ Created demo processed_gold_data.csv")

def main():
    """Main training function"""
    print(f"Starting training at {datetime.now()}")
    
    # Create directories
    create_directories()
    
    # Train models
    success = train_models()
    
    if success:
        print("\n🎉 All models trained successfully!")
        print("You can now run the web application with: python app.py")
    else:
        print("\n⚠️ Training completed with demo data")
        print("You can still run the web application with: python app.py")

if __name__ == "__main__":
    main()
