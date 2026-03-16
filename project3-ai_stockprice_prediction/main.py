"""
Main script for stock price prediction using multiple models.
Demonstrates time series analysis, feature engineering, and model comparison.
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from data_loader import download_stock_data, prepare_data_for_modeling
from preprocessing import engineer_features, analyze_data, plot_stock_data, plot_correlation
from models import LinearRegressionModel, RandomForestModel
from models import TENSORFLOW_AVAILABLE

# Import NeuralNetworkModel only if TensorFlow is available
if TENSORFLOW_AVAILABLE:
    from models import NeuralNetworkModel
else:
    NeuralNetworkModel = None

from evaluation import ModelEvaluator, compare_models, plot_metrics_comparison


def main():
    """Main execution function."""
    
    print("\n" + "="*70)
    print("STOCK PRICE PREDICTION - MACHINE LEARNING PROJECT")
    print("="*70)
    
    # ==================== Data Loading ====================
    print("\n[1] LOADING DATA")
    ticker = 'AAPL'  # Apple stock
    data = download_stock_data(ticker, save_to_csv=True)
    
    # ==================== Data Analysis ====================
    print("\n[2] EXPLORATORY DATA ANALYSIS")
    analyze_data(data, ticker)
    
    # Show raw data
    print(f"First 5 rows of data:")
    print(data.head())
    
    # ==================== Feature Engineering ====================
    print("\n[3] FEATURE ENGINEERING")
    data = engineer_features(data, lookback_period=5)
    print(f"Engineered features: {list(data.columns[4:])}")
    print(data.head())
    
    # ==================== Visualization ====================
    print("\n[4] DATA VISUALIZATION")
    fig1 = plot_stock_data(data, show_features=True)
    fig1.savefig('stock_price_analysis.png', dpi=100, bbox_inches='tight')
    print("✓ Saved: stock_price_analysis.png")
    
    fig2 = plot_correlation(data)
    if fig2:
        fig2.savefig('correlation_matrix.png', dpi=100, bbox_inches='tight')
        print("✓ Saved: correlation_matrix.png")
    
    # ==================== Data Preparation ====================
    print("\n[5] PREPARING DATA FOR MODELING")
    X_train, X_test, y_train, y_test, scaler_X, scaler_y = prepare_data_for_modeling(
        data, target_col='close', test_size=0.2
    )
    
    # Also prepare validation set from training data
    val_split = int(len(X_train) * 0.2)
    X_val, y_val = X_train[-val_split:], y_train[-val_split:]
    X_train, y_train = X_train[:-val_split], y_train[:-val_split]
    
    print(f"Final training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    # ==================== Model Training ====================
    print("\n[6] TRAINING MODELS")
    
    # Linear Regression
    print("\n--- Linear Regression Model ---")
    lr_model = LinearRegressionModel()
    lr_model.train(X_train, y_train)
    
    # Random Forest
    print("\n--- Random Forest Model ---")
    rf_model = RandomForestModel(n_estimators=100, max_depth=15)
    rf_model.train(X_train, y_train)
    
    # Neural Network
    models = {
        'Linear Regression': lr_model,
        'Random Forest': rf_model
    }
    
    if TENSORFLOW_AVAILABLE:
        print("\n--- Neural Network Model ---")
        nn_model = NeuralNetworkModel(input_dim=X_train.shape[1], hidden_layers=[64, 32])
        nn_model.train(X_train, y_train, X_val=X_val, y_val=y_val, epochs=100, batch_size=32, verbose=0)
        
        # Save training history plot
        fig3 = nn_model.plot_training_history()
        fig3.savefig('nn_training_history.png', dpi=100, bbox_inches='tight')
        print("\n✓ Saved: nn_training_history.png")
        
        models['Neural Network'] = nn_model
    else:
        print("\n⚠️  TensorFlow not available - skipping Neural Network training")
        print("   To enable: pip install tensorflow")
    
    # ==================== Model Evaluation ====================
    print("\n[7] MODEL EVALUATION")
    
    # Compare only the models that were trained
    # models dict was already created above
    
    # Compare models
    comparison_df = compare_models(models, X_test, y_test)
    comparison_df.to_csv('model_comparison.csv')
    print("✓ Saved: model_comparison.csv")
    
    # ==================== Predictions and Visualization ====================
    print("\n[8] PREDICTION VISUALIZATION")
    
    evaluator = ModelEvaluator()
    
    for model_name, model in models.items():
        y_pred = model.predict(X_test)
        
        # Plot predictions
        fig = evaluator.plot_predictions(y_test, y_pred, model_name=model_name)
        filename = f'predictions_{model_name.lower().replace(" ", "_")}.png'
        fig.savefig(filename, dpi=100, bbox_inches='tight')
        print(f"✓ Saved: {filename}")
        
        # Plot residuals
        fig = evaluator.plot_residuals(y_test, y_pred, model_name=model_name)
        filename = f'residuals_{model_name.lower().replace(" ", "_")}.png'
        fig.savefig(filename, dpi=100, bbox_inches='tight')
        print(f"✓ Saved: {filename}")
    
    # Plot metrics comparison
    fig = plot_metrics_comparison(comparison_df)
    fig.savefig('metrics_comparison.png', dpi=100, bbox_inches='tight')
    print("✓ Saved: metrics_comparison.png")
    
    # ==================== Summary ====================
    print("\n[9] SUMMARY")
    print("\nBest Model (by R² Score):", comparison_df['R² Score'].idxmax())
    print("Lowest RMSE:", comparison_df['RMSE'].idxmin())
    print("\nAll visualizations and results have been saved.")
    
    print("\n" + "="*70)
    print("PROJECT COMPLETED SUCCESSFULLY!")
    print("="*70 + "\n")
    
    return models, comparison_df


if __name__ == "__main__":
    models, results = main()
