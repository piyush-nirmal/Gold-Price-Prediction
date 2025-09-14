import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import time
import random

class RealTimeSentimentAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            'rise', 'up', 'gain', 'increase', 'surge', 'rally', 'bullish', 'strong',
            'positive', 'optimistic', 'growth', 'demand', 'inflation', 'safe haven',
            'uncertainty', 'crisis', 'fear', 'volatility', 'dollar weak', 'fed cut',
            'stimulus', 'quantitative easing', 'recession', 'geopolitical'
        ]
        
        self.negative_keywords = [
            'fall', 'down', 'drop', 'decline', 'plunge', 'crash', 'bearish', 'weak',
            'negative', 'pessimistic', 'loss', 'supply', 'deflation', 'dollar strong',
            'fed hike', 'rate increase', 'tapering', 'recovery', 'stability', 'peace'
        ]
        
        self.neutral_keywords = [
            'stable', 'unchanged', 'flat', 'sideways', 'consolidation', 'range',
            'technical', 'analysis', 'chart', 'support', 'resistance', 'trend'
        ]

    def fetch_gold_news(self, num_articles=10):
        """Fetch recent gold news from multiple sources"""
        news_articles = []
        
        try:
            # Fetch from Reuters Gold News
            reuters_url = "https://www.reuters.com/business/energy/"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(reuters_url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('a', href=True)[:num_articles]
                
                for article in articles:
                    title = article.get_text(strip=True)
                    if title and any(keyword in title.lower() for keyword in ['gold', 'precious', 'metal', 'bullion']):
                        news_articles.append({
                            'title': title,
                            'source': 'Reuters',
                            'timestamp': datetime.now()
                        })
        except Exception as e:
            print(f"Error fetching Reuters news: {e}")
        
        # If no real news found, generate sample news for demonstration
        if not news_articles:
            news_articles = self.generate_sample_news(num_articles)
        
        return news_articles

    def generate_sample_news(self, num_articles=10):
        """Generate sample gold news for demonstration"""
        sample_news = [
            "Gold prices surge as inflation concerns mount",
            "Federal Reserve hints at rate cuts, boosting gold demand",
            "Geopolitical tensions drive safe-haven gold buying",
            "Dollar weakness supports gold price rally",
            "Gold futures fall on profit-taking after recent gains",
            "Strong economic data weighs on gold prices",
            "Gold consolidates near resistance levels",
            "Central bank buying supports gold market",
            "Gold prices stable amid mixed economic signals",
            "Technical analysis suggests gold may break higher"
        ]
        
        news_articles = []
        for i, title in enumerate(sample_news[:num_articles]):
            news_articles.append({
                'title': title,
                'source': 'Sample News',
                'timestamp': datetime.now() - timedelta(hours=i)
            })
        
        return news_articles

    def analyze_sentiment(self, text):
        """Analyze sentiment of news text"""
        text_lower = text.lower()
        
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in text_lower)
        neutral_count = sum(1 for keyword in self.neutral_keywords if keyword in text_lower)
        
        total_keywords = positive_count + negative_count + neutral_count
        
        if total_keywords == 0:
            return 0.0, "neutral"
        
        # Calculate sentiment score (-1 to +1)
        sentiment_score = (positive_count - negative_count) / total_keywords
        
        # Determine sentiment strength
        if sentiment_score > 0.3:
            sentiment_strength = "very_positive"
        elif sentiment_score > 0.1:
            sentiment_strength = "positive"
        elif sentiment_score < -0.3:
            sentiment_strength = "very_negative"
        elif sentiment_score < -0.1:
            sentiment_strength = "negative"
        else:
            sentiment_strength = "neutral"
        
        return sentiment_score, sentiment_strength

    def get_current_sentiment(self):
        """Get current market sentiment based on recent news"""
        print("Fetching current gold market sentiment...")
        
        # Fetch recent news
        news_articles = self.fetch_gold_news(10)
        
        if not news_articles:
            return 0.0, "neutral", "No recent news available"
        
        # Analyze sentiment for each article
        sentiment_scores = []
        news_summary = []
        
        for article in news_articles:
            sentiment_score, sentiment_strength = self.analyze_sentiment(article['title'])
            sentiment_scores.append(sentiment_score)
            news_summary.append(f"{article['title']} ({sentiment_strength})")
        
        # Calculate average sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        # Determine overall sentiment strength
        if avg_sentiment > 0.3:
            overall_sentiment = "very_positive"
        elif avg_sentiment > 0.1:
            overall_sentiment = "positive"
        elif avg_sentiment < -0.3:
            overall_sentiment = "very_negative"
        elif avg_sentiment < -0.1:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        # Create news summary
        latest_news = " | ".join(news_summary[:3])  # Show top 3 news items
        
        print(f"Analyzed {len(news_articles)} news articles")
        print(f"Average sentiment: {avg_sentiment:.3f} ({overall_sentiment})")
        
        return avg_sentiment, overall_sentiment, latest_news

# Test the sentiment analyzer
if __name__ == "__main__":
    analyzer = RealTimeSentimentAnalyzer()
    sentiment, strength, news = analyzer.get_current_sentiment()
    print(f"Current Sentiment: {sentiment:.3f} ({strength})")
    print(f"Latest News: {news}")
