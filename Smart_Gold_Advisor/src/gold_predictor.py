import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
import joblib
import warnings
warnings.filterwarnings('ignore')

class GoldPricePredictor:
    def __init__(self, sequence_length=30):
        self.sequence_length = sequence_length
        self.scaler_price = MinMaxScaler()
        self.scaler_sentiment = MinMaxScaler()
        self.model = None
        self.is_trained = False
        
    def prepare_data(self, data):
        """Prepare data for training"""
        print("Preparing data for training...")
        
        # Extract features
        prices = data['SF_Price'].values.reshape(-1, 1)
        sentiment = data['Sentiment_score'].values.reshape(-1, 1)
        
        # Scale the data
        prices_scaled = self.scaler_price.fit_transform(prices)
        sentiment_scaled = self.scaler_sentiment.fit_transform(sentiment)
        
        # Create features
        X, y = [], []
        for i in range(self.sequence_length, len(prices_scaled)):
            # Price features
            price_features = prices_scaled[i-self.sequence_length:i].flatten()
            sentiment_features = sentiment_scaled[i-self.sequence_length:i].flatten()
            
            # Combine features
            combined_features = np.concatenate([price_features, sentiment_features])
            X.append(combined_features)
            y.append(prices_scaled[i][0])
        
        X, y = np.array(X), np.array(y)
        
        print(f"Training data shape: X={X.shape}, y={y.shape}")
        return X, y
    
    def build_model(self):
        """Build Random Forest model"""
        print("Building Random Forest model...")
        
        # Use Random Forest for better performance without TensorFlow
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        print("Model: Random Forest Regressor")
        return model
    
    def train_model(self, data, validation_split=0.2):
        """Train the model"""
        print("Training Random Forest model...")
        
        # Prepare data
        X, y = self.prepare_data(data)
        
        # Split data
        split_idx = int(len(X) * (1 - validation_split))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Build model
        self.model = self.build_model()
        
        # Train model
        self.model.fit(X_train, y_train)
        
        self.is_trained = True
        
        # Evaluate model
        train_pred = self.model.predict(X_train)
        val_pred = self.model.predict(X_val)
        
        # Inverse transform predictions
        train_pred_actual = self.scaler_price.inverse_transform(train_pred.reshape(-1, 1)).flatten()
        val_pred_actual = self.scaler_price.inverse_transform(val_pred.reshape(-1, 1)).flatten()
        y_train_actual = self.scaler_price.inverse_transform(y_train.reshape(-1, 1)).flatten()
        y_val_actual = self.scaler_price.inverse_transform(y_val.reshape(-1, 1)).flatten()
        
        # Calculate metrics
        train_rmse = np.sqrt(mean_squared_error(y_train_actual, train_pred_actual))
        val_rmse = np.sqrt(mean_squared_error(y_val_actual, val_pred_actual))
        train_mae = mean_absolute_error(y_train_actual, train_pred_actual)
        val_mae = mean_absolute_error(y_val_actual, val_pred_actual)
        
        print(f"\nModel Performance:")
        print(f"Training RMSE: {train_rmse:.2f}")
        print(f"Validation RMSE: {val_rmse:.2f}")
        print(f"Training MAE: {train_mae:.2f}")
        print(f"Validation MAE: {val_mae:.2f}")
        
        return {
            'train_rmse': train_rmse,
            'val_rmse': val_rmse,
            'train_mae': train_mae,
            'val_mae': val_mae
        }
    
    def predict_next_day(self, data):
        """Predict gold price for the next day"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        # Get last sequence_length days of data
        last_prices = data['SF_Price'].tail(self.sequence_length).values.reshape(-1, 1)
        last_sentiment = data['Sentiment_score'].tail(self.sequence_length).values.reshape(-1, 1)
        
        # Scale the data
        prices_scaled = self.scaler_price.transform(last_prices)
        sentiment_scaled = self.scaler_sentiment.transform(last_sentiment)
        
        # Combine features
        price_features = prices_scaled.flatten()
        sentiment_features = sentiment_scaled.flatten()
        combined_features = np.concatenate([price_features, sentiment_features])
        
        X = combined_features.reshape(1, -1)
        
        # Make prediction
        prediction_scaled = self.model.predict(X)[0]
        prediction = self.scaler_price.inverse_transform([[prediction_scaled]])[0][0]
        
        return prediction
    
    def predict_next_week(self, data):
        """Predict gold prices for the next week"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        predictions = []
        current_data = data.copy()
        
        for day in range(7):
            # Predict next day
            next_price = self.predict_next_day(current_data)
            predictions.append(next_price)
            
            # Add predicted price to data for next prediction
            # Use average sentiment for future days
            avg_sentiment = current_data['Sentiment_score'].mean()
            
            # Create new row
            last_date = current_data['Date'].iloc[-1]
            next_date = last_date + pd.Timedelta(days=1)
            
            new_row = pd.DataFrame({
                'Date': [next_date],
                'SF_Price': [next_price],
                'Sentiment_score': [avg_sentiment],
                'News': ['']
            })
            
            current_data = pd.concat([current_data, new_row], ignore_index=True)
        
        return predictions
    
    def save_model(self, model_path='models/gold_predictor_model.pkl', scaler_path='models/scalers.pkl'):
        """Save the trained model and scalers"""
        if self.is_trained:
            joblib.dump(self.model, model_path)
            joblib.dump({
                'price_scaler': self.scaler_price,
                'sentiment_scaler': self.scaler_sentiment
            }, scaler_path)
            print(f"Model saved to {model_path}")
            print(f"Scalers saved to {scaler_path}")
        else:
            print("No trained model to save")
    
    def load_model(self, model_path='models/gold_predictor_model.pkl', scaler_path='models/scalers.pkl'):
        """Load a pre-trained model and scalers"""
        try:
            self.model = joblib.load(model_path)
            scalers = joblib.load(scaler_path)
            self.scaler_price = scalers['price_scaler']
            self.scaler_sentiment = scalers['sentiment_scaler']
            self.is_trained = True
            print(f"Model loaded from {model_path}")
            print(f"Scalers loaded from {scaler_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.is_trained = False

if __name__ == "__main__":
    # Test the model
    from data_preprocessing import DataPreprocessor
    
    # Load and preprocess data
    preprocessor = DataPreprocessor()
    data = preprocessor.preprocess_all()
    
    # Train model
    predictor = GoldPricePredictor()
    predictor.train_model(data)
    
    # Make predictions
    next_day_price = predictor.predict_next_day(data)
    next_week_prices = predictor.predict_next_week(data)
    
    print(f"\nPredictions:")
    print(f"Next day price: ${next_day_price:.2f}")
    print(f"Next week prices: {[f'${p:.2f}' for p in next_week_prices]}")
    
    # Save model
    predictor.save_model()