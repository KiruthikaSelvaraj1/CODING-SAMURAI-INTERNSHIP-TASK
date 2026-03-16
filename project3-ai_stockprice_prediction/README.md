# Project 3: AI for Predicting Stock Prices 

A comprehensive project demonstrating advanced machine learning techniques for predicting stock prices based on historical data. This project implements **LSTM neural networks** and **deep learning** with emphasis on **time series analysis** and **evaluation metrics**.

**Repository**: [CODING-SAMURAI-INTERNSHIP-TASK](https://github.com/KiruthikaSelvaraj1/CODING-SAMURAI-INTERNSHIP-TASK.git)
**Hashtag**: #CodingSamurai

## Project Overview

**Objective**: Build and compare machine learning models to predict stock prices using historical price data and engineered features.

**Skills Covered**:
- ✅ Time Series Analysis
- ✅ Feature Engineering (Technical Indicators)
- ✅ Data Preprocessing and Normalization
- ✅ Linear Regression Models
- ✅ Neural Network Models (Keras/TensorFlow)
- ✅ Model Evaluation Metrics
- ✅ Data Visualization

**Models Implemented**:
1. **Linear Regression** - Fast baseline model
2. **Random Forest** - Ensemble method for better generalization
3. **Neural Network** - Multi-layer perceptron for non-linear patterns
4. **LSTM** - Long Short-Term Memory for sequential data (framework provided)

## Project Structure

```
Project-3-Stock-Price-Prediction/
├── main.py                          # Main execution script
├── Stock_Price_Prediction.ipynb     # Interactive Jupyter notebook with advanced implementations
├── requirements.txt                 # Python dependencies
├── README.md                        # Project documentation
│
├── Core Modules:
├── data_loader.py                   # Data loading and preparation utilities
├── preprocessing.py                 # Feature engineering and data normalization
├── models.py                        # LSTM and deep learning model implementations
└── evaluation.py                    # Comprehensive evaluation metrics & visualization

├── Data:
├── data/                            # Stock price data (AAPL_synthetic.csv)
│
├── Output Files (Generated):
├── *.png                            # Prediction visualizations and analyses
└── model_comparison.csv             # Detailed results comparison
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Libraries**:
- `numpy` - Numerical computing
- `pandas` - Data manipulation
- `scikit-learn` - Machine learning
- `tensorflow` - Deep learning framework
- `matplotlib` & `seaborn` - Visualization
- `yfinance` - Stock data download
- `jupyter` - Interactive notebooks

### 2. Run the Project

**Option A: Run the main script**
```bash
python main.py
```

**Option B: Use the Jupyter Notebook**
```bash
jupyter notebook Stock_Price_Prediction.ipynb
```

## How It Works

### Phase 1: Data Loading & Exploration
- Download historical stock data (default: Apple/AAPL)
- Analyze price patterns, volume, and statistics
- Visualize time series and trends

### Phase 2: Feature Engineering
Creates technical indicators from raw OHLCV data:

| Feature | Description |
|---------|-------------|
| SMA_5, SMA_20 | Simple Moving Averages |
| EMA_12 | Exponential Moving Average |
| Daily_Return | Percentage daily price change |
| Momentum_5 | Rate of price change |
| Volatility_20 | Rolling standard deviation |
| HL_Range | High-Low price range |

### Phase 3: Data Preparation
- Normalize features using MinMaxScaler (0-1 range)
- Maintain temporal order for time series
- Split: 70% training, 10% validation, 20% testing

### Phase 4: Model Training

**Linear Regression**
```python
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
```

**Neural Network**
```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential([
    Dense(64, activation='relu', input_dim=10),
    Dropout(0.2),
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(1, activation='linear')  # Price prediction
])
model.compile(optimizer='adam', loss='mse')
model.fit(X_train, y_train, epochs=100)
```

### Phase 5: Evaluation & Comparison

**Evaluation Metrics**:

| Metric | Formula | Interpretation |
|--------|---------|-----------------|
| **MSE** | $\frac{1}{n}\sum(y_i - \hat{y}_i)^2$ | Lower is better |
| **RMSE** | $\sqrt{MSE}$ | In same units as target |
| **MAE** | $\frac{1}{n}\sum\|y_i - \hat{y}_i\|$ | Average absolute error |
| **R² Score** | $1 - \frac{\sum(y_i - \hat{y}_i)^2}{\sum(y_i - \bar{y})^2}$ | Higher is better (0-1) |

## Key Results & Insights

### Model Comparison
- **Linear Regression**: Faster, interpretable, good for linear trends
- **Neural Network**: Better for non-linear patterns, longer training time
- **Random Forest**: Good generalization, handles feature interactions

### Typical Performance Metrics
```
Linear Regression:
  RMSE: ~2-5 (depends on stock volatility)
  R² Score: 0.70-0.85
  
Neural Network:
  RMSE: ~1-3
  R² Score: 0.75-0.90
```

### Important Considerations
1. **Stock prices are influenced by many external factors** not in this dataset
2. **Past performance doesn't guarantee future results**
3. **Use in real trading only with proper risk management**
4. **Ensemble methods often outperform single models**

## Usage Examples

### Load and Predict with Trained Model

```python
from data_loader import download_stock_data, prepare_data_for_modeling
from models import LinearRegressionModel, NeuralNetworkModel
from evaluation import ModelEvaluator

# Load data
data = download_stock_data('AAPL', save_to_csv=True)

# Prepare data
X_train, X_test, y_train, y_test, scaler_X, scaler_y = prepare_data_for_modeling(data)

# Train models
lr_model = LinearRegressionModel()
lr_model.train(X_train, y_train)

nn_model = NeuralNetworkModel(input_dim=X_train.shape[1])
nn_model.train(X_train, y_train, epochs=100)

# Make predictions
lr_pred = lr_model.predict(X_test)
nn_pred = nn_model.predict(X_test)

# Evaluate
evaluator = ModelEvaluator()
metrics = evaluator.calculate_metrics(y_test, nn_pred)
evaluator.print_metrics(metrics, "Neural Network")
```

### Make Future Price Predictions

```python
# Predict next price (fictional example)
next_features = np.array([[100, 102, 98, 5000000, 100.2, 100.1, 0.01, 2, 1.5, 4]])
next_features_scaled = scaler_X.transform(next_features)
predicted_price_scaled = nn_model.predict(next_features_scaled)
predicted_price = scaler_y.inverse_transform(predicted_price_scaled)
print(f"Predicted next price: ${predicted_price[0][0]:.2f}")
```

## Visualizations Generated

The project generates several plots saved as PNG files:

1. **stock_price_analysis.png** - Historical prices with moving averages
2. **correlation_matrix.png** - Feature correlations heatmap
3. **nn_training_history.png** - Training/validation loss curves
4. **predictions_*.png** - Actual vs predicted prices for each model
5. **residuals_*.png** - Error distribution and analysis
6. **metrics_comparison.png** - Side-by-side metric comparison

## Advanced Features

### Extension Ideas

1. **LSTM Networks** - Better capturing temporal dependencies
   ```python
   from models import LSTMModel
   lstm = LSTMModel(sequence_length=30, input_dim=10)
   ```

2. **Ensemble Methods** - Combine predictions from multiple models
   ```python
   ensemble_pred = (0.3 * lr_pred + 0.7 * nn_pred)
   ```

3. **Hyperparameter Tuning** - GridSearchCV for optimization
   ```python
   from sklearn.model_selection import GridSearchCV
   # Tune model parameters
   ```

4. **Real-time Predictions** - Continuous model updates
   ```python
   while True:
       new_data = download_latest_data()
       prediction = model.predict(new_data)
   ```

5. **Multi-step Forecasting** - Predict multiple days ahead
   ```python
   # Predict next 5 days
   future_prices = model.predict(horizon=5)
   ```

## Performance Tips

### For Better Results:
- Use more historical data (3-5 years minimum)
- Include additional features (sentiment analysis, macroeconomic indicators)
- Deploy ensemble methods combining multiple models
- Add regularization to prevent overfitting
- Use cross-validation for better error estimates
- Consider data augmentation for more training samples

### Computational Efficiency:
- Neural Network training is GPU-intensive; consider using GPU acceleration
- Use `batch_processing` for large datasets
- Implement early stopping to prevent overfitting during training

## Common Issues & Solutions

**Issue**: Model predictions are flat/constant
- **Solution**: Check feature scaling, verify data preprocessing

**Issue**: Loss doesn't decrease during training
- **Solution**: Reduce learning rate, check data quality, try different architecture

**Issue**: CUDA/GPU errors
- **Solution**: Install TensorFlow CPU version or configure GPU drivers

**Issue**: Memory issues with large datasets
- **Solution**: Use `batch_size` parameter or reduce sequence length

## References & Resources

- **Machine Learning Fundamentals**: scikit-learn documentation
- **Deep Learning**: TensorFlow/Keras official guides
- **Time Series Analysis**: "Forecasting: Principles and Practice" by Hyndman & Athanasopoulos
- **Stock Market Data**: Yahoo Finance API (yfinance)
- **Neural Networks**: Andrew Ng's Machine Learning Specialization

## Project Checklist

- ✅ Data Loading from API/CSV
- ✅ Exploratory Data Analysis (EDA)
- ✅ Feature Engineering (Technical Indicators)
- ✅ Data Normalization/Scaling
- ✅ Train-Test Split (Time Series Aware)
- ✅ Linear Regression Implementation
- ✅ Neural Network Implementation
- ✅ Model Training & Validation
- ✅ Evaluation Metrics Calculation
- ✅ Predictions Visualization
- ✅ Model Comparison & Analysis

---

## About Coding Samurai

**Coding Samurai** is a pioneering EdTech startup founded in August 2022 with a mission to bridge the gap between academic knowledge and industry expectations. We provide comprehensive technical training, internships, and consulting solutions to empower aspiring tech professionals.

### Our Vision
At Coding Samurai, we envision a future where practical skills and innovation drive success. We equip aspiring tech professionals with real-world expertise and help businesses harness the power of technology.

### Connect With Us
- 🌐 **Website**: [www.codingsamurai.in](https://www.codingsamurai.in)
- 💼 **LinkedIn**: [Coding Samurai](https://www.linkedin.com/company/coding-samurai/)
- 📧 **Email**: support@codingsamurai.in
- 📱 **Telegram**: Coding Samurai

### Hashtag
**#CodingSamurai** #Internship #ArtificialIntelligence #MachineLearning

---

## License

MIT License - Feel free to use and modify for educational purposes.

**Created during Coding Samurai Internship Program**
- ✅ Documentation & Examples

## Author

Created as part of the Coding Samurai Internship Task
**Project 5**: AI for Predicting Stock Prices

## Disclaimer

This project is for educational purposes only. Stock price prediction is inherently uncertain and involves many factors not captured in historical data. **Do not use this for real trading without proper risk management and professional advice.**

## License

This project is provided as-is for educational use.

---

**Questions?** Refer to the detailed comments in the code or check the Jupyter notebook for step-by-step explanations.
