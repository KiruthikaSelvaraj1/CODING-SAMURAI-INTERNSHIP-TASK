"""
Evaluation metrics and visualization for model performance.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


class ModelEvaluator:
    """Evaluate and compare model predictions."""
    
    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """
        Calculate common regression metrics.
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
        
        Returns:
            dict: Dictionary of metrics
        """
        y_true = y_true.ravel()
        y_pred = y_pred.ravel()
        
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100 if np.all(y_true != 0) else np.inf
        r2 = r2_score(y_true, y_pred)
        
        # Mean Absolute Percentage Error
        mape_valid = np.mean(np.abs((y_true - y_pred) / (np.abs(y_true) + 1e-8))) * 100
        
        return {
            'MSE': mse,
            'RMSE': rmse,
            'MAE': mae,
            'MAPE (%)': mape_valid,
            'R² Score': r2
        }
    
    @staticmethod
    def print_metrics(metrics, model_name: str = "Model"):
        """
        Print metrics in a formatted way.
        
        Args:
            metrics (dict): Metrics dictionary
            model_name (str): Name of the model
        """
        print(f"\n{'='*50}")
        print(f"Performance Metrics - {model_name}")
        print(f"{'='*50}")
        for key, value in metrics.items():
            print(f"{key:.<30} {value:>10.4f}")
        print(f"{'='*50}\n")
    
    @staticmethod
    def plot_predictions(y_true, y_pred, dates=None, model_name: str = "Model", figsize: tuple = (14, 6)):
        """
        Plot actual vs predicted values.
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            dates (np.ndarray): Date values for x-axis
            model_name (str): Name of the model
            figsize (tuple): Figure size
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        x_axis = np.arange(len(y_true)) if dates is None else dates
        
        ax.plot(x_axis, y_true, label='Actual Price', linewidth=2, marker='o', markersize=3)
        ax.plot(x_axis, y_pred, label='Predicted Price', linewidth=2, marker='s', markersize=3, alpha=0.8)
        
        ax.fill_between(range(len(y_true)), y_true.ravel(), y_pred.ravel(), alpha=0.2, color='red')
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Price (Normalized)')
        ax.set_title(f'Actual vs Predicted Stock Prices - {model_name}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    @staticmethod
    def plot_residuals(y_true, y_pred, model_name: str = "Model", figsize: tuple = (12, 5)):
        """
        Plot residuals analysis.
        
        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Name of the model
            figsize (tuple): Figure size
        """
        residuals = (y_true - y_pred).ravel()
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Residuals over time
        axes[0].plot(residuals, linewidth=1)
        axes[0].axhline(y=0, color='r', linestyle='--', alpha=0.7)
        axes[0].set_xlabel('Sample')
        axes[0].set_ylabel('Residual')
        axes[0].set_title(f'Residuals Over Time - {model_name}')
        axes[0].grid(True, alpha=0.3)
        
        # Residuals distribution
        axes[1].hist(residuals, bins=30, edgecolor='black', alpha=0.7)
        axes[1].axvline(x=0, color='r', linestyle='--', linewidth=2)
        axes[1].set_xlabel('Residual Value')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title(f'Distribution of Residuals - {model_name}')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


def compare_models(models_dict, X_test, y_test, dates=None):
    """
    Compare multiple models' performance.
    
    Args:
        models_dict (dict): Dictionary with model names as keys and model objects as values
        X_test (np.ndarray): Test features
        y_test (np.ndarray): Test targets
        dates (np.ndarray): Date values for visualization
    
    Returns:
        pd.DataFrame: Comparison of metrics across models
    """
    results = {}
    evaluator = ModelEvaluator()
    
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    
    for model_name, model in models_dict.items():
        y_pred = model.predict(X_test)
        metrics = evaluator.calculate_metrics(y_test, y_pred)
        evaluator.print_metrics(metrics, model_name)
        results[model_name] = metrics
    
    # Create comparison dataframe
    comparison_df = pd.DataFrame(results).T
    
    print("\nSummary Comparison:")
    print(comparison_df.to_string())
    print("="*60 + "\n")
    
    return comparison_df


def plot_metrics_comparison(comparison_df, figsize: tuple = (12, 6)):
    """
    Plot comparison of metrics across models.
    
    Args:
        comparison_df (pd.DataFrame): Comparison dataframe
        figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(2, 3, figsize=figsize)
    axes = axes.ravel()
    
    metrics = comparison_df.columns
    
    for idx, metric in enumerate(metrics):
        if idx < len(axes):
            comparison_df[metric].plot(kind='bar', ax=axes[idx], color='steelblue')
            axes[idx].set_title(metric)
            axes[idx].set_ylabel('Value')
            axes[idx].tick_params(axis='x', rotation=45)
            axes[idx].grid(True, alpha=0.3)
    
    # Hide unused subplots
    for idx in range(len(metrics), len(axes)):
        axes[idx].set_visible(False)
    
    plt.tight_layout()
    return fig
