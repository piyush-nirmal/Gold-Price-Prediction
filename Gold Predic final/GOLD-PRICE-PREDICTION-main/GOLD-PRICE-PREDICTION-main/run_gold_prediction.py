# Gold Price Prediction Script
# Importing libraries that will be used in this script.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')

print("Starting Gold Price Prediction Analysis...")

# Loading the csv data to a Pandas Dataframe
print("Loading data...")
gold_data = pd.read_csv("gld_price_data.csv")

print("Data loaded successfully!")
print(f"Dataset shape: {gold_data.shape}")
print(f"Columns: {list(gold_data.columns)}")

# Display first few rows
print("\nFirst 5 rows:")
print(gold_data.head())

# Display basic info
print("\nDataset info:")
print(gold_data.info())

# Check for null values
print("\nNull values:")
print(gold_data.isnull().sum())

# Statistical measures
print("\nStatistical measures:")
print(gold_data.describe())

# Drop the "date" column as it's not needed for prediction
print("\nDropping Date column...")
data = gold_data.drop(['Date'], axis=1)

# Check for duplicates
print(f"Number of duplicates: {data.duplicated().sum()}")

# Check for null values after dropping date
print("Null values after dropping date:")
print(data.isnull().sum())

# Remove outliers from USO (as done in the original notebook)
print("\nRemoving outliers from USO...")
q = data["USO"].quantile(0.98)
data = data[(data["USO"] < q)]
print(f"Data shape after outlier removal: {data.shape}")

# Compute correlation
print("\nComputing correlation...")
correlation = data.corr()
print("Correlation with GLD:")
print(correlation['GLD'])

# Splitting the data
print("\nSplitting data into training and testing sets...")
X = data.drop(['GLD'], axis=1)  # Features
Y = data['GLD']  # Target

# Split into train and test sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

print(f"Training set size: {X_train.shape}")
print(f"Test set size: {X_test.shape}")

# Model Training: Random Forest Regressor
print("\nTraining Random Forest Regressor...")
regressor = RandomForestRegressor(n_estimators=100)
regressor.fit(X_train, Y_train)
print("Model trained successfully!")

# Evaluation
print("\nMaking predictions on test data...")
test_data_prediction = regressor.predict(X_test)

# Calculate R-squared error
error_score = metrics.r2_score(Y_test, test_data_prediction)
print(f'R squared error: {error_score}')

# Display some predictions vs actual values
print("\nFirst 10 predictions vs actual values:")
for i in range(10):
    print(f"Actual: {Y_test.iloc[i]:.2f}, Predicted: {test_data_prediction[i]:.2f}")

# Create visualizations
print("\nCreating visualizations...")

# Set figure size for all plots
plt.rcParams['figure.figsize'] = [12, 8]

# Plot 1: Actual vs Predicted values
plt.figure(figsize=(12, 6))
plt.plot(Y_test.values, color='blue', label='Actual Value', alpha=0.7)
plt.plot(test_data_prediction, color='red', label='Predicted Value', alpha=0.7)
plt.title('Actual Price vs Predicted Price')
plt.xlabel('Number of values')
plt.ylabel('Gold Price')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('actual_vs_predicted.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot 2: Distribution comparison
plt.figure(figsize=(12, 6))
plt.hist(Y_test.values, color='purple', label='Actual Value', alpha=0.7, bins=30)
plt.hist(test_data_prediction, color='green', label='Predicted Value', alpha=0.7, bins=30)
plt.title('Actual Price of Gold vs Predicted Price of Gold')
plt.xlabel('Gold Price')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('distribution_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot 3: Correlation heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(correlation, cbar=True, square=True, fmt='.2f', annot=True, 
            annot_kws={'size':10}, cmap='Greens')
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Feature importance
print("\nFeature importance:")
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': regressor.feature_importances_
}).sort_values('importance', ascending=False)

print(feature_importance)

# Plot feature importance
plt.figure(figsize=(10, 6))
sns.barplot(data=feature_importance, x='importance', y='feature')
plt.title('Feature Importance in Gold Price Prediction')
plt.xlabel('Importance')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*50)
print("ANALYSIS COMPLETE!")
print("="*50)
print(f"Model Performance (R² Score): {error_score:.4f}")
print(f"Model Accuracy: {error_score*100:.2f}%")
print("\nFiles saved:")
print("- actual_vs_predicted.png")
print("- distribution_comparison.png") 
print("- correlation_heatmap.png")
print("- feature_importance.png")

# Test the prediction function with sample data
print("\n" + "="*50)
print("TESTING PREDICTION FUNCTION")
print("="*50)

def predict_gold_price(spx, uso, slv, eur_usd):
    """Predict gold price based on input features"""
    input_data = np.array([[spx, uso, slv, eur_usd]])
    prediction = regressor.predict(input_data)
    return prediction[0]

# Test with sample values from the dataset
sample_values = [
    (1310.5, 70.550003, 15.902, 1.464794),  # Expected ~88.17
    (1336.910034, 69.800003, 16.674999, 1.483107),  # Expected ~92.06
    (1556.219971, 33.040001, 28.02, 1.298802)  # Expected ~152.99
]

print("Testing predictions with sample data:")
for i, (spx, uso, slv, eur_usd) in enumerate(sample_values, 1):
    prediction = predict_gold_price(spx, uso, slv, eur_usd)
    print(f"Sample {i}: SPX={spx:.2f}, USO={uso:.2f}, SLV={slv:.2f}, EUR/USD={eur_usd:.4f}")
    print(f"Predicted Gold Price: ${prediction:.2f}")
    print("-" * 40)

print("\nGold Price Prediction Model is ready for use!")
