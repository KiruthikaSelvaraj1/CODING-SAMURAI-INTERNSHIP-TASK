"""
Data preprocessing and exploratory analysis for stock prices.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler


def engineer_features(data: pd.DataFrame, lookback_period: int = 5, in_place: bool = True):
    """
    Create technical indicators and time series features.
    
    Args:
        data (pd.DataFrame): Stock data with 'close' column
        lookback_period (int): Period for moving averages and returns
        in_place (bool): Whether to modify data in place
    
    Returns:
        pd.DataFrame: Data with engineered features
    """
    if not in_place:
        data = data.copy()
    
    # Sort by date
    data = data.sort_values('date').reset_index(drop=True)
    
    # Moving averages
    data['sma_5'] = data['close'].rolling(window=5).mean()
    data['sma_20'] = data['close'].rolling(window=20).mean()
    
    # Exponential moving average
    data['ema_12'] = data['close'].ewm(span=12).mean()
    
    # Daily returns
    data['daily_return'] = data['close'].pct_change()
    
    # Price momentum (rate of change)
    data['momentum_5'] = data['close'].diff(periods=5)
    
    # Volatility (rolling standard deviation)
    data['volatility_20'] = data['close'].rolling(window=20).std()
    
    # High-Low range
    data['hl_range'] = data['high'] - data['low']
    
    # Volume-Price Trend
    data['vpt'] = data['close'].pct_change() * data['volume']
    
    # Drop rows with NaN values created by rolling operations
    data = data.dropna().reset_index(drop=True)
    
    print(f"Features engineered. Shape: {data.shape}")
    return data


def analyze_data(data: pd.DataFrame, ticker: str = "Stock"):
    """
    Perform exploratory data analysis on stock data.
    
    Args:
        data (pd.DataFrame): Stock data
        ticker (str): Stock ticker for titles
    """
    print(f"\n{'='*50}")
    print(f"Data Summary for {ticker}")
    print(f"{'='*50}")
    print(f"Date range: {data['date'].min()} to {data['date'].max()}")
    print(f"Total records: {len(data)}")
    print(f"\nPrice Statistics (Close):")
    print(data['close'].describe())
    print(f"\nMissing values:")
    print(data.isnull().sum())
    print(f"\n{'='*50}\n")


def plot_stock_data(data: pd.DataFrame, figsize: tuple = (14, 8), show_features: bool = True):
    """
    Visualize stock price data and technical indicators.
    
    Args:
        data (pd.DataFrame): Stock data with 'date' and 'close' columns
        figsize (tuple): Figure size
        show_features (bool): Whether to plot technical indicators
    """
    if show_features and 'sma_20' in data.columns:
        fig, axes = plt.subplots(3, 1, figsize=figsize)
        
        # Price and moving averages
        axes[0].plot(data['date'], data['close'], label='Close Price', linewidth=2)
        axes[0].plot(data['date'], data['sma_5'], label='SMA 5', alpha=0.7)
        axes[0].plot(data['date'], data['sma_20'], label='SMA 20', alpha=0.7)
        axes[0].set_ylabel('Price ($)')
        axes[0].set_title('Stock Price and Moving Averages')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Daily returns
        axes[1].plot(data['date'], data['daily_return'], label='Daily Returns', color='green', alpha=0.7)
        axes[1].axhline(y=0, color='r', linestyle='--', alpha=0.5)
        axes[1].set_ylabel('Returns')
        axes[1].set_title('Daily Returns')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Volume
        axes[2].bar(data['date'], data['volume'], label='Volume', color='blue', alpha=0.5)
        axes[2].set_ylabel('Volume')
        axes[2].set_xlabel('Date')
        axes[2].set_title('Trading Volume')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
    else:
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(data['date'], data['close'], linewidth=2)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price ($)')
        ax.set_title('Stock Price Over Time')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_correlation(data: pd.DataFrame, figsize: tuple = (10, 8)):
    """
    Plot correlation matrix of features.
    
    Args:
        data (pd.DataFrame): Stock data with multiple features
        figsize (tuple): Figure size
    """
    numeric_data = data.select_dtypes(include=[np.number])
    
    if numeric_data.shape[1] > 1:
        fig, ax = plt.subplots(figsize=figsize)
        corr_matrix = numeric_data.corr()
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, ax=ax, square=True, cbar_kws={"shrink": 0.8})
        ax.set_title('Feature Correlation Matrix')
        plt.tight_layout()
        return fig
    else:
        print("Not enough features for correlation analysis")
        return None
