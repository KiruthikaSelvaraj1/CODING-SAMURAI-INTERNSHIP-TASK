"""
Data loading module for stock price prediction.
Downloads historical stock data from Yahoo Finance.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import numpy as np


def generate_synthetic_data(ticker: str, save_to_csv: bool = False, days: int = 1260):
    """
    Generate realistic synthetic stock data for demonstration.
    
    Args:
        ticker (str): Stock ticker symbol
        save_to_csv (bool): Whether to save data to CSV file
        days (int): Number of days of data to generate (default 5 years)
    
    Returns:
        pd.DataFrame: Synthetic stock data
    """
    np.random.seed(42)
    
    # Generate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate realistic prices using random walk
    base_price = 100.0
    returns = np.random.normal(0.0005, 0.02, len(dates))
    prices = base_price * np.exp(np.cumsum(returns))
    
    # Generate OHLCV data
    data = pd.DataFrame({
        'date': dates,
        'open': prices * (1 + np.random.normal(0, 0.005, len(dates))),
        'high': prices * (1 + np.abs(np.random.normal(0.01, 0.01, len(dates)))),
        'low': prices * (1 - np.abs(np.random.normal(0.01, 0.01, len(dates)))),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, len(dates))
    })
    
    if save_to_csv:
        os.makedirs('data', exist_ok=True)
        filename = f'data/{ticker}_synthetic.csv'
        data.to_csv(filename, index=False)
        print(f"Synthetic data saved to {filename}")
    
    print(f"Generated {len(data)} days of synthetic data for {ticker}")
    return data


def download_stock_data(ticker: str, start_date: str = None, end_date: str = None, save_to_csv: bool = False):
    """
    Download historical stock data using yfinance.
    Falls back to synthetic data if download fails.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        start_date (str): Start date in format 'YYYY-MM-DD'. Default is 5 years ago.
        end_date (str): End date in format 'YYYY-MM-DD'. Default is today.
        save_to_csv (bool): Whether to save data to CSV file.
    
    Returns:
        pd.DataFrame: Historical stock data with OHLCV data
    """
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')
    
    if end_date is None:
        end_date = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Downloading {ticker} data from {start_date} to {end_date}...")
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker}")
        
        # Reset index to make Date a column
        data.reset_index(inplace=True)
        
        # Rename columns to lowercase for consistency
        data.columns = [col.lower() for col in data.columns]
        
        if save_to_csv:
            os.makedirs('data', exist_ok=True)
            filename = f'data/{ticker}_historical.csv'
            data.to_csv(filename, index=False)
            print(f"Data saved to {filename}")
        
        print(f"Downloaded {len(data)} records")
        return data
    
    except Exception as e:
        print(f"\n⚠️  Warning: Failed to download data from yfinance")
        print(f"   Error: {str(e)}")
        print(f"   Using synthetic data instead for demonstration...\n")
        return generate_synthetic_data(ticker, save_to_csv)


def load_stock_data_from_csv(filepath: str):
    """
    Load stock data from CSV file.
    
    Args:
        filepath (str): Path to CSV file
    
    Returns:
        pd.DataFrame: Stock data
    """
    data = pd.read_csv(filepath)
    data['date'] = pd.to_datetime(data['date'])
    return data


def prepare_data_for_modeling(data: pd.DataFrame, target_col: str = 'close', 
                              feature_cols: list = None, test_size: float = 0.2):
    """
    Prepare data for time series modeling.
    
    Args:
        data (pd.DataFrame): Stock data
        target_col (str): Column to predict
        feature_cols (list): Features to use. If None, uses all numeric columns except target.
        test_size (float): Proportion of data for testing
    
    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler_X, scaler_y)
    """
    from sklearn.preprocessing import MinMaxScaler
    
    if feature_cols is None:
        feature_cols = [col for col in data.columns 
                       if col not in ['date'] and data[col].dtype in ['float64', 'int64']]
    
    # Sort by date
    data = data.sort_values('date').reset_index(drop=True)
    
    X = data[feature_cols].values
    y = data[target_col].values.reshape(-1, 1)
    
    # Scale features
    scaler_X = MinMaxScaler()
    X_scaled = scaler_X.fit_transform(X)
    
    # Scale target
    scaler_y = MinMaxScaler()
    y_scaled = scaler_y.fit_transform(y)
    
    # Time series split (not random!)
    split_idx = int(len(data) * (1 - test_size))
    
    X_train, X_test = X_scaled[:split_idx], X_scaled[split_idx:]
    y_train, y_test = y_scaled[:split_idx], y_scaled[split_idx:]
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    print(f"Features: {feature_cols}")
    
    return X_train, X_test, y_train, y_test, scaler_X, scaler_y
