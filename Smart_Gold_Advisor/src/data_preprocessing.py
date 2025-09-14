import pandas as pd
import numpy as np
from datetime import datetime
import re
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    def __init__(self):
        self.gold_data = None
        self.sentiment_data = None
        self.merged_data = None
        
    def load_data(self, gold_file='data/FINAL_USO.csv', sentiment_file='data/gold sentiment.csv'):
        """Load and examine the CSV files"""
        print("Loading data files...")
        
        # Load gold price data
        self.gold_data = pd.read_csv(gold_file)
        print(f"Gold data shape: {self.gold_data.shape}")
        print(f"Gold data columns: {list(self.gold_data.columns)}")
        
        # Load sentiment data
        self.sentiment_data = pd.read_csv(sentiment_file)
        print(f"Sentiment data shape: {self.sentiment_data.shape}")
        print(f"Sentiment data columns: {list(self.sentiment_data.columns)}")
        
        return self.gold_data, self.sentiment_data
    
    def clean_gold_data(self):
        """Clean and prepare gold price data"""
        print("Cleaning gold price data...")
        
        # Convert Date column to datetime
        self.gold_data['Date'] = pd.to_datetime(self.gold_data['Date'])
        
        # Select relevant columns (Date and SF_Price for gold price)
        self.gold_data = self.gold_data[['Date', 'SF_Price']].copy()
        
        # Remove rows with missing SF_Price
        self.gold_data = self.gold_data.dropna(subset=['SF_Price'])
        
        # Sort by date
        self.gold_data = self.gold_data.sort_values('Date').reset_index(drop=True)
        
        print(f"Cleaned gold data shape: {self.gold_data.shape}")
        print(f"Date range: {self.gold_data['Date'].min()} to {self.gold_data['Date'].max()}")
        
        return self.gold_data
    
    def clean_sentiment_data(self):
        """Clean and prepare sentiment data"""
        print("Cleaning sentiment data...")
        
        # Rename columns for consistency
        self.sentiment_data.columns = ['Date', 'News', 'Sentiment']
        
        # Remove rows with invalid dates
        self.sentiment_data = self.sentiment_data[self.sentiment_data['Date'] != '#VALUE!']
        self.sentiment_data = self.sentiment_data[self.sentiment_data['Date'].notna()]
        
        # Convert Date column to datetime with error handling
        self.sentiment_data['Date'] = pd.to_datetime(self.sentiment_data['Date'], format='%d-%m-%Y', errors='coerce')
        
        # Remove rows where date conversion failed
        self.sentiment_data = self.sentiment_data[self.sentiment_data['Date'].notna()]
        
        # Clean news text
        self.sentiment_data['News'] = self.sentiment_data['News'].astype(str)
        self.sentiment_data['News'] = self.sentiment_data['News'].str.lower()
        self.sentiment_data['News'] = self.sentiment_data['News'].str.strip()
        
        # Remove special characters but keep spaces
        self.sentiment_data['News'] = self.sentiment_data['News'].apply(
            lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x)
        )
        
        # Convert sentiment labels to numeric
        sentiment_mapping = {'negative': -1, 'neutral': 0, 'positive': 1, 'none': 0}
        self.sentiment_data['Sentiment_score'] = self.sentiment_data['Sentiment'].map(sentiment_mapping)
        
        # Remove rows with missing sentiment scores
        self.sentiment_data = self.sentiment_data.dropna(subset=['Sentiment_score'])
        
        # Sort by date
        self.sentiment_data = self.sentiment_data.sort_values('Date').reset_index(drop=True)
        
        print(f"Cleaned sentiment data shape: {self.sentiment_data.shape}")
        print(f"Date range: {self.sentiment_data['Date'].min()} to {self.sentiment_data['Date'].max()}")
        print(f"Sentiment distribution: {self.sentiment_data['Sentiment_score'].value_counts().to_dict()}")
        
        return self.sentiment_data
    
    def aggregate_sentiment_by_date(self):
        """Aggregate multiple news per day to average sentiment and combined headlines"""
        print("Aggregating sentiment data by date...")
        
        # Group by date and aggregate
        aggregated = self.sentiment_data.groupby('Date').agg({
            'Sentiment_score': 'mean',
            'News': lambda x: ' | '.join(x.unique()[:5])  # Combine headlines, limit to 5
        }).reset_index()
        
        # Rename columns
        aggregated.columns = ['Date', 'Sentiment_score', 'News']
        
        self.sentiment_data = aggregated
        print(f"Aggregated sentiment data shape: {self.sentiment_data.shape}")
        
        return self.sentiment_data
    
    def merge_data(self):
        """Merge gold price and sentiment data by date"""
        print("Merging gold price and sentiment data...")
        
        # Merge on date
        self.merged_data = pd.merge(
            self.gold_data, 
            self.sentiment_data, 
            on='Date', 
            how='left'
        )
        
        # Fill missing sentiment scores with 0 (neutral)
        self.merged_data['Sentiment_score'] = self.merged_data['Sentiment_score'].fillna(0)
        
        # Fill missing news with empty string
        self.merged_data['News'] = self.merged_data['News'].fillna('')
        
        # Sort by date
        self.merged_data = self.merged_data.sort_values('Date').reset_index(drop=True)
        
        print(f"Merged data shape: {self.merged_data.shape}")
        print(f"Final columns: {list(self.merged_data.columns)}")
        print(f"Date range: {self.merged_data['Date'].min()} to {self.merged_data['Date'].max()}")
        
        return self.merged_data
    
    def preprocess_all(self, gold_file='data/FINAL_USO.csv', sentiment_file='data/gold sentiment.csv'):
        """Run complete preprocessing pipeline"""
        print("Starting complete data preprocessing pipeline...")
        
        # Load data
        self.load_data(gold_file, sentiment_file)
        
        # Clean data
        self.clean_gold_data()
        self.clean_sentiment_data()
        
        # Aggregate sentiment
        self.aggregate_sentiment_by_date()
        
        # Merge data
        self.merge_data()
        
        print("Data preprocessing completed successfully!")
        return self.merged_data
    
    def save_processed_data(self, filename='processed_gold_data.csv'):
        """Save the processed data to CSV"""
        if self.merged_data is not None:
            self.merged_data.to_csv(filename, index=False)
            print(f"Processed data saved to {filename}")
        else:
            print("No processed data to save. Run preprocess_all() first.")

if __name__ == "__main__":
    # Test the preprocessing
    preprocessor = DataPreprocessor()
    processed_data = preprocessor.preprocess_all()
    preprocessor.save_processed_data()
    
    print("\nSample of processed data:")
    print(processed_data.head())
    print(f"\nData types:")
    print(processed_data.dtypes)
