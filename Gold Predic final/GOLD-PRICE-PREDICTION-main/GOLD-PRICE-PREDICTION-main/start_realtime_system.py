"""
Real-Time Gold Price Prediction System - Startup Script
======================================================

This script starts the complete real-time gold price prediction system
including data fetching, sentiment analysis, predictions, and dashboard.
"""

import os
import sys
import time
import threading
import subprocess
from datetime import datetime
import json

class RealTimeSystemManager:
    def __init__(self):
        """Initialize the real-time system manager"""
        self.processes = {}
        self.running = False
        
        print("🚀 Real-Time Gold Price Prediction System Manager")
        print("=" * 60)
    
    def start_prediction_engine(self, interval_minutes=5):
        """Start the prediction engine"""
        try:
            print("🔮 Starting Prediction Engine...")
            
            # Import and run the prediction engine
            from realtime_gold_predictor import RealTimeGoldPredictor
            
            predictor = RealTimeGoldPredictor()
            
            # Run in a separate thread
            def run_predictions():
                predictor.start_scheduled_predictions(interval_minutes)
            
            prediction_thread = threading.Thread(target=run_predictions, daemon=True)
            prediction_thread.start()
            
            self.processes['prediction_engine'] = prediction_thread
            print("✅ Prediction Engine Started!")
            
        except Exception as e:
            print(f"❌ Error starting prediction engine: {e}")
    
    def start_dashboard(self):
        """Start the web dashboard"""
        try:
            print("📊 Starting Web Dashboard...")
            
            # Start dashboard in a separate process
            dashboard_process = subprocess.Popen([
                sys.executable, 'dashboard.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            self.processes['dashboard'] = dashboard_process
            print("✅ Web Dashboard Started!")
            print("🌐 Dashboard available at: http://127.0.0.1:8050")
            
        except Exception as e:
            print(f"❌ Error starting dashboard: {e}")
    
    def start_news_analyzer(self, interval_minutes=10):
        """Start the news sentiment analyzer"""
        try:
            print("📰 Starting News Sentiment Analyzer...")
            
            from news_sentiment import NewsSentimentAnalyzer
            import schedule
            
            analyzer = NewsSentimentAnalyzer()
            
            def analyze_news():
                sentiment_data = analyzer.analyze_news_sentiment()
                market_indicators = analyzer.get_market_sentiment_indicators()
                
                combined_data = {
                    'news_sentiment': sentiment_data,
                    'market_indicators': market_indicators,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                analyzer.save_sentiment_data(combined_data)
            
            # Schedule news analysis
            schedule.every(interval_minutes).minutes.do(analyze_news)
            
            # Run in a separate thread
            def run_news_analysis():
                while self.running:
                    schedule.run_pending()
                    time.sleep(1)
            
            news_thread = threading.Thread(target=run_news_analysis, daemon=True)
            news_thread.start()
            
            self.processes['news_analyzer'] = news_thread
            print("✅ News Sentiment Analyzer Started!")
            
        except Exception as e:
            print(f"❌ Error starting news analyzer: {e}")
    
    def start_api_monitor(self, interval_minutes=2):
        """Start the API data monitor"""
        try:
            print("🔌 Starting API Data Monitor...")
            
            from api_integration import FinancialDataAPI
            import schedule
            
            api = FinancialDataAPI()
            
            def monitor_apis():
                comprehensive_data = api.get_comprehensive_market_data()
                api.save_api_data(comprehensive_data, "live_market_data.json")
            
            # Schedule API monitoring
            schedule.every(interval_minutes).minutes.do(monitor_apis)
            
            # Run in a separate thread
            def run_api_monitor():
                while self.running:
                    schedule.run_pending()
                    time.sleep(1)
            
            api_thread = threading.Thread(target=run_api_monitor, daemon=True)
            api_thread.start()
            
            self.processes['api_monitor'] = api_thread
            print("✅ API Data Monitor Started!")
            
        except Exception as e:
            print(f"❌ Error starting API monitor: {e}")
    
    def create_system_status_file(self):
        """Create a system status file"""
        try:
            status = {
                'system_running': True,
                'start_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'components': {
                    'prediction_engine': 'prediction_engine' in self.processes,
                    'dashboard': 'dashboard' in self.processes,
                    'news_analyzer': 'news_analyzer' in self.processes,
                    'api_monitor': 'api_monitor' in self.processes
                },
                'dashboard_url': 'http://127.0.0.1:8050',
                'data_files': [
                    'realtime_predictions.json',
                    'news_sentiment.json',
                    'live_market_data.json'
                ]
            }
            
            with open('system_status.json', 'w') as f:
                json.dump(status, f, indent=2)
            
            print("📄 System status file created: system_status.json")
            
        except Exception as e:
            print(f"❌ Error creating status file: {e}")
    
    def start_complete_system(self):
        """Start the complete real-time system"""
        try:
            print("🌟 Starting Complete Real-Time Gold Price Prediction System...")
            print("=" * 70)
            
            self.running = True
            
            # Start all components
            self.start_prediction_engine(5)  # Every 5 minutes
            time.sleep(2)
            
            self.start_news_analyzer(10)     # Every 10 minutes
            time.sleep(2)
            
            self.start_api_monitor(2)        # Every 2 minutes
            time.sleep(2)
            
            self.start_dashboard()
            time.sleep(2)
            
            # Create status file
            self.create_system_status_file()
            
            print("\n🎉 SYSTEM STARTUP COMPLETE!")
            print("=" * 70)
            print("📊 Dashboard: http://127.0.0.1:8050")
            print("📄 Status File: system_status.json")
            print("📈 Prediction Data: realtime_predictions.json")
            print("📰 News Sentiment: news_sentiment.json")
            print("🔌 Market Data: live_market_data.json")
            print("\n⏹️  Press Ctrl+C to stop the system")
            print("=" * 70)
            
            # Keep the main thread alive
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.stop_system()
                
        except Exception as e:
            print(f"❌ Error starting complete system: {e}")
            self.stop_system()
    
    def stop_system(self):
        """Stop the complete system"""
        print("\n🛑 Stopping Real-Time System...")
        self.running = False
        
        # Stop dashboard process
        if 'dashboard' in self.processes:
            try:
                self.processes['dashboard'].terminate()
                print("✅ Dashboard stopped")
            except:
                pass
        
        # Update status file
        try:
            status = {
                'system_running': False,
                'stop_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'components': {
                    'prediction_engine': False,
                    'dashboard': False,
                    'news_analyzer': False,
                    'api_monitor': False
                }
            }
            
            with open('system_status.json', 'w') as f:
                json.dump(status, f, indent=2)
            
            print("📄 System status updated")
            
        except Exception as e:
            print(f"❌ Error updating status: {e}")
        
        print("👋 System stopped successfully!")

def show_menu():
    """Show the main menu"""
    print("\n🌟 REAL-TIME GOLD PRICE PREDICTION SYSTEM")
    print("=" * 50)
    print("Choose an option:")
    print("1. Start Complete System (All Components)")
    print("2. Start Prediction Engine Only")
    print("3. Start Dashboard Only")
    print("4. Start News Analyzer Only")
    print("5. Start API Monitor Only")
    print("6. Test Individual Components")
    print("7. Exit")
    print("=" * 50)

def test_components():
    """Test individual components"""
    print("\n🧪 Testing Individual Components...")
    print("=" * 40)
    
    # Test prediction engine
    print("1. Testing Prediction Engine...")
    try:
        from realtime_gold_predictor import RealTimeGoldPredictor
        predictor = RealTimeGoldPredictor()
        result = predictor.run_prediction_cycle()
        if result:
            print("   ✅ Prediction Engine: PASSED")
        else:
            print("   ❌ Prediction Engine: FAILED")
    except Exception as e:
        print(f"   ❌ Prediction Engine: ERROR - {e}")
    
    # Test news analyzer
    print("2. Testing News Analyzer...")
    try:
        from news_sentiment import NewsSentimentAnalyzer
        analyzer = NewsSentimentAnalyzer()
        result = analyzer.analyze_news_sentiment()
        if result:
            print("   ✅ News Analyzer: PASSED")
        else:
            print("   ❌ News Analyzer: FAILED")
    except Exception as e:
        print(f"   ❌ News Analyzer: ERROR - {e}")
    
    # Test API integration
    print("3. Testing API Integration...")
    try:
        from api_integration import FinancialDataAPI
        api = FinancialDataAPI()
        result = api.fetch_yahoo_finance_data(['GLD'])
        if result:
            print("   ✅ API Integration: PASSED")
        else:
            print("   ❌ API Integration: FAILED")
    except Exception as e:
        print(f"   ❌ API Integration: ERROR - {e}")
    
    print("\n✅ Component testing complete!")

def main():
    """Main function"""
    system_manager = RealTimeSystemManager()
    
    while True:
        show_menu()
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            system_manager.start_complete_system()
            
        elif choice == '2':
            system_manager.start_prediction_engine()
            input("\nPress Enter to stop...")
            system_manager.stop_system()
            
        elif choice == '3':
            system_manager.start_dashboard()
            input("\nPress Enter to stop...")
            system_manager.stop_system()
            
        elif choice == '4':
            system_manager.start_news_analyzer()
            input("\nPress Enter to stop...")
            system_manager.stop_system()
            
        elif choice == '5':
            system_manager.start_api_monitor()
            input("\nPress Enter to stop...")
            system_manager.stop_system()
            
        elif choice == '6':
            test_components()
            
        elif choice == '7':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
