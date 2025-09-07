"""
Advanced News Sentiment Analysis for Gold Price Prediction
=========================================================

This module provides sophisticated news sentiment analysis
for gold and precious metals markets using multiple sources.
"""

import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
import pandas as pd
from datetime import datetime, timedelta
import time
import json

class NewsSentimentAnalyzer:
    def __init__(self):
        """Initialize the news sentiment analyzer"""
        self.gold_keywords = [
            'gold', 'precious metals', 'bullion', 'GLD', 'gold ETF',
            'inflation', 'fed', 'federal reserve', 'interest rates',
            'dollar', 'USD', 'safe haven', 'economic uncertainty',
            'geopolitical', 'crisis', 'recession', 'market volatility'
        ]
        
        self.positive_keywords = [
            'rise', 'increase', 'up', 'gain', 'surge', 'rally',
            'strong', 'positive', 'bullish', 'optimistic', 'growth',
            'demand', 'investment', 'safe haven', 'inflation hedge'
        ]
        
        self.negative_keywords = [
            'fall', 'drop', 'decline', 'down', 'loss', 'crash',
            'weak', 'negative', 'bearish', 'pessimistic', 'recession',
            'crisis', 'uncertainty', 'volatility', 'risk'
        ]
        
        self.news_sources = [
            {
                'name': 'Reuters Gold News',
                'url': 'https://www.reuters.com/business/energy/',
                'selector': '.story-title'
            },
            {
                'name': 'MarketWatch Gold',
                'url': 'https://www.marketwatch.com/investing/future/gc00',
                'selector': '.headline'
            }
        ]
        
        print("📰 News Sentiment Analyzer Initialized!")
    
    def fetch_news_headlines(self, source_url, max_headlines=10):
        """Fetch news headlines from a source"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(source_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try different selectors for headlines
            selectors = [
                'h1', 'h2', 'h3', '.headline', '.title', '.story-title',
                '[class*="headline"]', '[class*="title"]'
            ]
            
            headlines = []
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements[:max_headlines]:
                    text = element.get_text().strip()
                    if text and len(text) > 10:  # Filter out very short text
                        headlines.append(text)
                if headlines:
                    break
            
            return headlines[:max_headlines]
            
        except Exception as e:
            print(f"❌ Error fetching news from {source_url}: {e}")
            return []
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of a text using TextBlob"""
        try:
            blob = TextBlob(text)
            return blob.sentiment.polarity  # -1 to 1 scale
        except:
            return 0
    
    def calculate_keyword_sentiment(self, text):
        """Calculate sentiment based on keyword analysis"""
        text_lower = text.lower()
        
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        
        if positive_count + negative_count == 0:
            return 0
        
        return (positive_count - negative_count) / (positive_count + negative_count)
    
    def is_gold_related(self, text):
        """Check if text is related to gold/precious metals"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.gold_keywords)
    
    def analyze_news_sentiment(self):
        """Analyze sentiment from multiple news sources"""
        print("📰 Analyzing news sentiment...")
        
        all_headlines = []
        sentiment_scores = []
        
        # Fetch headlines from multiple sources
        for source in self.news_sources:
            print(f"  📡 Fetching from {source['name']}...")
            headlines = self.fetch_news_headlines(source['url'])
            
            for headline in headlines:
                if self.is_gold_related(headline):
                    all_headlines.append({
                        'headline': headline,
                        'source': source['name'],
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
        
        # Analyze sentiment for each headline
        for headline_data in all_headlines:
            headline = headline_data['headline']
            
            # TextBlob sentiment
            textblob_sentiment = self.analyze_sentiment(headline)
            
            # Keyword-based sentiment
            keyword_sentiment = self.calculate_keyword_sentiment(headline)
            
            # Combined sentiment (weighted average)
            combined_sentiment = (textblob_sentiment * 0.6) + (keyword_sentiment * 0.4)
            
            sentiment_scores.append(combined_sentiment)
            
            print(f"    📄 '{headline[:50]}...' -> {combined_sentiment:.3f}")
        
        # Calculate overall sentiment
        if sentiment_scores:
            overall_sentiment = np.mean(sentiment_scores)
            sentiment_std = np.std(sentiment_scores)
            
            # Adjust for volatility (high volatility = more uncertainty)
            volatility_adjustment = -abs(sentiment_std) * 0.1
            adjusted_sentiment = overall_sentiment + volatility_adjustment
            
            print(f"  📊 Overall Sentiment: {overall_sentiment:.3f}")
            print(f"  📈 Volatility: {sentiment_std:.3f}")
            print(f"  🎯 Adjusted Sentiment: {adjusted_sentiment:.3f}")
            
            return {
                'overall_sentiment': overall_sentiment,
                'adjusted_sentiment': adjusted_sentiment,
                'volatility': sentiment_std,
                'headlines_analyzed': len(all_headlines),
                'headlines': all_headlines,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            print("  ⚠️ No gold-related headlines found")
            return {
                'overall_sentiment': 0,
                'adjusted_sentiment': 0,
                'volatility': 0,
                'headlines_analyzed': 0,
                'headlines': [],
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def get_market_sentiment_indicators(self):
        """Get additional market sentiment indicators"""
        try:
            print("📊 Analyzing market sentiment indicators...")
            
            # VIX (Volatility Index) - Fear indicator
            vix_sentiment = self.get_vix_sentiment()
            
            # Dollar strength sentiment
            dollar_sentiment = self.get_dollar_sentiment()
            
            # Economic indicators sentiment
            economic_sentiment = self.get_economic_sentiment()
            
            # Combine indicators
            combined_indicators = {
                'vix_sentiment': vix_sentiment,
                'dollar_sentiment': dollar_sentiment,
                'economic_sentiment': economic_sentiment,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return combined_indicators
            
        except Exception as e:
            print(f"❌ Error analyzing market indicators: {e}")
            return {}
    
    def get_vix_sentiment(self):
        """Analyze VIX (Volatility Index) for market fear"""
        try:
            # This is a simplified version - in production, you'd fetch real VIX data
            # For now, we'll simulate based on market conditions
            return 0.1  # Neutral sentiment
        except:
            return 0
    
    def get_dollar_sentiment(self):
        """Analyze dollar strength sentiment"""
        try:
            # Simplified dollar strength analysis
            return -0.1  # Slightly negative (weak dollar = positive for gold)
        except:
            return 0
    
    def get_economic_sentiment(self):
        """Analyze economic indicators sentiment"""
        try:
            # Simplified economic sentiment
            return 0.05  # Slightly positive
        except:
            return 0
    
    def save_sentiment_data(self, sentiment_data):
        """Save sentiment analysis data to file"""
        try:
            with open('news_sentiment.json', 'w') as f:
                json.dump(sentiment_data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving sentiment data: {e}")

def main():
    """Test the news sentiment analyzer"""
    print("🌟 Testing News Sentiment Analyzer")
    print("=" * 50)
    
    analyzer = NewsSentimentAnalyzer()
    
    # Analyze news sentiment
    sentiment_data = analyzer.analyze_news_sentiment()
    
    # Get market indicators
    market_indicators = analyzer.get_market_sentiment_indicators()
    
    # Combine results
    combined_data = {
        'news_sentiment': sentiment_data,
        'market_indicators': market_indicators,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save data
    analyzer.save_sentiment_data(combined_data)
    
    print("\n📊 SENTIMENT ANALYSIS SUMMARY")
    print("=" * 50)
    print(f"Overall Sentiment: {sentiment_data['overall_sentiment']:.3f}")
    print(f"Adjusted Sentiment: {sentiment_data['adjusted_sentiment']:.3f}")
    print(f"Headlines Analyzed: {sentiment_data['headlines_analyzed']}")
    print(f"Volatility: {sentiment_data['volatility']:.3f}")

if __name__ == "__main__":
    import numpy as np
    main()
