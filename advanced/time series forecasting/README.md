# Time Series Forecasting

## Project Overview

In this project, I applied time series forecasting models to predict future sales data. This is a critical task for many businesses to ensure proper inventory management, budget planning, and business strategy development.

## Dataset

The dataset used in this project is the [Monthly Champagne sales](https://datamarket.com/data/set/22n4/monthly-champagne-sales-million-litres-64-72#!ds=22n4&display=line) from DataMarket. It represents the sales data of a champagne brand in a period of several years.

## Requirements

This project is implemented in Python, with the use of the following libraries:

- Pandas
- NumPy
- Matplotlib
- statsmodels

## Steps

1. **Data Exploration**: I analyzed the time series data to identify trends, seasonality, and irregularities.
2. **Data Preprocessing**: Preprocessed the data to make it stationary, a requirement for many time series forecasting techniques.
3. **Model Building**: I applied the ARIMA (AutoRegressive Integrated Moving Average) model, a popular method for time series forecasting.
4. **Model Evaluation**: Evaluated the model based on metrics like Mean Absolute Error (MAE), Mean Squared Error (MSE), and Root Mean Squared Error (RMSE).
5. **Forecasting**: Used the model to predict future sales and visualized the results.

## Results

The final model achieved an RMSE of XX on the test set. More detailed results and discussions can be found in the [Jupyter notebook](link-to-notebook).

## Future Work

In the future, I plan to explore more advanced techniques such as state space models and machine learning models for time series forecasting.
