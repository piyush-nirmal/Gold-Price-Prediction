import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class InvestmentRecommendationEngine:
    def __init__(self):
        self.current_price = None
        self.predicted_price = None
        self.sentiment_score = None
        self.recommendation = None
        self.confidence = None
        self.reasoning = []
        
    def analyze_price_trend(self, current_price, predicted_price):
        """Analyze price trend direction"""
        price_change = predicted_price - current_price
        price_change_pct = (price_change / current_price) * 100
        
        if price_change_pct > 1.0:
            return "strong_up", price_change_pct
        elif price_change_pct > 0.2:
            return "up", price_change_pct
        elif price_change_pct < -1.0:
            return "strong_down", price_change_pct
        elif price_change_pct < -0.2:
            return "down", price_change_pct
        else:
            return "stable", price_change_pct
    
    def analyze_sentiment(self, sentiment_score):
        """Analyze sentiment strength"""
        if sentiment_score > 0.3:
            return "very_positive", sentiment_score
        elif sentiment_score > 0.1:
            return "positive", sentiment_score
        elif sentiment_score < -0.3:
            return "very_negative", sentiment_score
        elif sentiment_score < -0.1:
            return "negative", sentiment_score
        else:
            return "neutral", sentiment_score
    
    def calculate_confidence(self, price_trend_strength, sentiment_strength, price_change_pct, sentiment_score):
        """Calculate confidence level based on trend alignment"""
        # Base confidence on trend alignment
        alignment_score = 0
        
        # Price trend and sentiment alignment
        if (price_trend_strength in ["strong_up", "up"] and sentiment_strength in ["very_positive", "positive"]) or \
           (price_trend_strength in ["strong_down", "down"] and sentiment_strength in ["very_negative", "negative"]):
            alignment_score = 0.8
        elif (price_trend_strength in ["strong_up", "up"] and sentiment_strength == "neutral") or \
             (price_trend_strength in ["strong_down", "down"] and sentiment_strength == "neutral") or \
             (price_trend_strength == "stable" and sentiment_strength in ["very_positive", "very_negative"]):
            alignment_score = 0.6
        elif price_trend_strength == "stable" and sentiment_strength == "neutral":
            alignment_score = 0.4
        else:
            alignment_score = 0.2
        
        # Adjust based on magnitude
        magnitude_factor = min(abs(price_change_pct) / 2.0, 1.0) * 0.2
        sentiment_factor = min(abs(sentiment_score) * 2, 1.0) * 0.2
        
        confidence = min(alignment_score + magnitude_factor + sentiment_factor, 1.0)
        return confidence
    
    def generate_recommendation(self, current_price, predicted_price, sentiment_score, latest_news=""):
        """Generate investment recommendation based on price prediction and sentiment"""
        self.current_price = current_price
        self.predicted_price = predicted_price
        self.sentiment_score = sentiment_score
        self.reasoning = []
        
        # Analyze trends
        price_trend, price_change_pct = self.analyze_price_trend(current_price, predicted_price)
        sentiment_strength, sentiment_value = self.analyze_sentiment(sentiment_score)
        
        # Calculate confidence
        self.confidence = self.calculate_confidence(price_trend, sentiment_strength, price_change_pct, sentiment_score)
        
        # Generate recommendation logic
        if price_trend in ["strong_up", "up"] and sentiment_strength in ["very_positive", "positive"]:
            self.recommendation = "BUY"
            self.reasoning.append(f"Price is predicted to increase by {price_change_pct:.2f}%")
            self.reasoning.append(f"Market sentiment is {sentiment_strength} ({sentiment_value:.2f})")
            self.reasoning.append("Positive sentiment aligns with upward price movement")
            
        elif price_trend in ["strong_down", "down"] and sentiment_strength in ["very_negative", "negative"]:
            self.recommendation = "SELL"
            self.reasoning.append(f"Price is predicted to decrease by {abs(price_change_pct):.2f}%")
            self.reasoning.append(f"Market sentiment is {sentiment_strength} ({sentiment_value:.2f})")
            self.reasoning.append("Negative sentiment aligns with downward price movement")
            
        elif price_trend in ["strong_up", "up"] and sentiment_strength in ["very_negative", "negative"]:
            self.recommendation = "HOLD"
            self.reasoning.append(f"Price trend suggests increase ({price_change_pct:.2f}%)")
            self.reasoning.append(f"But sentiment is {sentiment_strength} ({sentiment_value:.2f})")
            self.reasoning.append("Conflicting signals - wait for clearer direction")
            
        elif price_trend in ["strong_down", "down"] and sentiment_strength in ["very_positive", "positive"]:
            self.recommendation = "HOLD"
            self.reasoning.append(f"Price trend suggests decrease ({abs(price_change_pct):.2f}%)")
            self.reasoning.append(f"But sentiment is {sentiment_strength} ({sentiment_value:.2f})")
            self.reasoning.append("Conflicting signals - wait for clearer direction")
            
        else:
            self.recommendation = "HOLD"
            self.reasoning.append(f"Price trend is {price_trend} ({price_change_pct:.2f}%)")
            self.reasoning.append(f"Sentiment is {sentiment_strength} ({sentiment_value:.2f})")
            self.reasoning.append("Mixed signals suggest maintaining current position")
        
        # Add news context if available
        if latest_news and str(latest_news).strip():
            self.reasoning.append(f"Latest news: {str(latest_news)[:100]}...")
        
        # Add confidence level
        confidence_level = "High" if self.confidence > 0.7 else "Medium" if self.confidence > 0.4 else "Low"
        self.reasoning.append(f"Confidence level: {confidence_level} ({self.confidence:.2f})")
        
        return {
            'recommendation': self.recommendation,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'current_price': current_price,
            'predicted_price': predicted_price,
            'price_change_pct': price_change_pct,
            'sentiment_score': sentiment_score,
            'price_trend': price_trend,
            'sentiment_strength': sentiment_strength
        }
    
    def get_recommendation_summary(self):
        """Get a formatted summary of the recommendation"""
        if not self.recommendation:
            return "No recommendation available. Please generate recommendation first."
        
        summary = f"""
        Investment Recommendation: {self.recommendation}
        Confidence: {self.confidence:.2f}
        
        Current Price: ${self.current_price:.2f}
        Predicted Price: ${self.predicted_price:.2f}
        Expected Change: {((self.predicted_price - self.current_price) / self.current_price * 100):.2f}%
        
        Reasoning:
        """
        
        for i, reason in enumerate(self.reasoning, 1):
            summary += f"{i}. {reason}\n"
        
        return summary.strip()

if __name__ == "__main__":
    # Test the recommendation engine
    engine = InvestmentRecommendationEngine()
    
    # Test scenarios
    test_cases = [
        (1800, 1850, 0.5, "Gold prices surge on inflation concerns"),
        (1800, 1750, -0.4, "Economic uncertainty drives gold down"),
        (1800, 1820, -0.2, "Mixed signals in the market"),
        (1800, 1805, 0.1, "Stable market conditions"),
        (1800, 1780, 0.3, "Positive sentiment but price decline")
    ]
    
    for current, predicted, sentiment, news in test_cases:
        print(f"\n{'='*50}")
        print(f"Test Case: Current=${current}, Predicted=${predicted}, Sentiment={sentiment}")
        print(f"{'='*50}")
        
        result = engine.generate_recommendation(current, predicted, sentiment, news)
        print(engine.get_recommendation_summary())
