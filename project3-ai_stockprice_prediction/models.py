"""
Machine learning models for stock price prediction.
Includes linear regression and simple neural network models.
"""

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# Try to import TensorFlow, but make it optional
try:
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, LSTM, Dropout
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    Sequential = None
    Dense = None
    LSTM = None
    Dropout = None
    Adam = None


class LinearRegressionModel:
    """Simple linear regression model for stock prediction."""
    
    def __init__(self):
        self.model = LinearRegression()
        self.is_trained = False
    
    def train(self, X_train, y_train):
        """
        Train the linear regression model.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training targets
        """
        print("Training Linear Regression model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print(f"Model trained. R² Score on training data: {self.model.score(X_train, y_train):.4f}")
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X (np.ndarray): Features to predict on
        
        Returns:
            np.ndarray: Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        return self.model.predict(X)
    
    def get_feature_importance(self, feature_names: list = None):
        """
        Get coefficients showing feature importance.
        
        Args:
            feature_names (list): Names of features
        
        Returns:
            dict: Feature names mapped to coefficients
        """
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(len(self.model.coef_[0]))]
        
        return {name: coef for name, coef in zip(feature_names, self.model.coef_[0])}


class RandomForestModel:
    """Random Forest model for stock price prediction."""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 10, random_state: int = 42):
        self.model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state,
            n_jobs=-1
        )
        self.is_trained = False
    
    def train(self, X_train, y_train):
        """
        Train the Random Forest model.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training targets
        """
        print("Training Random Forest model...")
        self.model.fit(X_train, y_train.ravel())
        self.is_trained = True
        print(f"Model trained. R² Score on training data: {self.model.score(X_train, y_train):.4f}")
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X (np.ndarray): Features to predict on
        
        Returns:
            np.ndarray: Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        return self.model.predict(X).reshape(-1, 1)
    
    def get_feature_importance(self, feature_names: list = None):
        """
        Get feature importance scores.
        
        Args:
            feature_names (list): Names of features
        
        Returns:
            dict: Feature names mapped to importance scores
        """
        if feature_names is None:
            feature_names = [f"Feature {i}" for i in range(self.model.n_features_in_)]
        
        return {name: importance for name, importance 
                in zip(feature_names, self.model.feature_importances_)}


class NeuralNetworkModel:
    """Simple feed-forward neural network for stock price prediction."""
    
    def __init__(self, input_dim: int, hidden_layers: list = None, dropout_rate: float = 0.2):
        """
        Initialize neural network.
        
        Args:
            input_dim (int): Number of input features
            hidden_layers (list): List of hidden layer sizes. Default: [64, 32]
            dropout_rate (float): Dropout rate for regularization
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is not installed. Install it with: pip install tensorflow")
        
        if hidden_layers is None:
            hidden_layers = [64, 32]
        
        self.model = Sequential()
        self.model.add(Dense(hidden_layers[0], activation='relu', input_dim=input_dim))
        self.model.add(Dropout(dropout_rate))
        
        for units in hidden_layers[1:]:
            self.model.add(Dense(units, activation='relu'))
            self.model.add(Dropout(dropout_rate))
        
        self.model.add(Dense(1, activation='linear'))
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        self.is_trained = False
        self.history = None
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs: int = 100, batch_size: int = 32, verbose: int = 1):
        """
        Train the neural network.
        
        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training targets
            X_val (np.ndarray): Validation features
            y_val (np.ndarray): Validation targets
            epochs (int): Number of training epochs
            batch_size (int): Batch size
            verbose (int): Verbosity level
        """
        print("Training Neural Network model...")
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose
        )
        self.is_trained = True
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X (np.ndarray): Features to predict on
        
        Returns:
            np.ndarray: Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        return self.model.predict(X, verbose=0)
    
    def plot_training_history(self, figsize: tuple = (12, 4)):
        """
        Plot training and validation loss/metrics.
        
        Args:
            figsize (tuple): Figure size
        """
        if self.history is None:
            print("No training history. Train the model first.")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Loss
        axes[0].plot(self.history.history['loss'], label='Training Loss')
        if 'val_loss' in self.history.history:
            axes[0].plot(self.history.history['val_loss'], label='Validation Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss (MSE)')
        axes[0].set_title('Model Loss')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # MAE
        axes[1].plot(self.history.history['mae'], label='Training MAE')
        if 'val_mae' in self.history.history:
            axes[1].plot(self.history.history['val_mae'], label='Validation MAE')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('MAE')
        axes[1].set_title('Mean Absolute Error')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig


class LSTMModel:
    """LSTM model for time series prediction."""
    
    def __init__(self, sequence_length: int, input_dim: int, hidden_units: list = None, dropout_rate: float = 0.2):
        """
        Initialize LSTM model.
        
        Args:
            sequence_length (int): Length of input sequences
            input_dim (int): Number of input features
            hidden_units (list): List of LSTM layer sizes
            dropout_rate (float): Dropout rate
        """
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow is not installed. Install it with: pip install tensorflow")
        
        if hidden_units is None:
            hidden_units = [50, 25]
        
        self.sequence_length = sequence_length
        self.model = Sequential()
        
        # First LSTM layer
        self.model.add(LSTM(hidden_units[0], activation='relu', input_shape=(sequence_length, input_dim), return_sequences=True))
        self.model.add(Dropout(dropout_rate))
        
        # Additional LSTM layers
        for units in hidden_units[1:]:
            self.model.add(LSTM(units, activation='relu', return_sequences=False))
            self.model.add(Dropout(dropout_rate))
        
        self.model.add(Dense(1))
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])
        self.is_trained = False
        self.history = None
    
    def train(self, X_train, y_train, X_val=None, y_val=None, epochs: int = 50, batch_size: int = 32, verbose: int = 1):
        """
        Train the LSTM model.
        
        Args:
            X_train (np.ndarray): Training sequences (samples, sequence_length, features)
            y_train (np.ndarray): Training targets
            X_val (np.ndarray): Validation sequences
            y_val (np.ndarray): Validation targets
            epochs (int): Number of training epochs
            batch_size (int): Batch size
            verbose (int): Verbosity level
        """
        print("Training LSTM model...")
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=validation_data,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose
        )
        self.is_trained = True
    
    def predict(self, X):
        """
        Make predictions.
        
        Args:
            X (np.ndarray): Sequences to predict on
        
        Returns:
            np.ndarray: Predictions
        """
        if not self.is_trained:
            raise ValueError("Model must be trained first")
        return self.model.predict(X, verbose=0)
