# Titanic Survival Prediction

## Project Overview

In this project, I have built a machine learning model to predict the survival of passengers on the Titanic. This is a well-known problem in the field of machine learning, often used for teaching binary classification.

## Dataset

The dataset used in this project is provided by Kaggle. It contains passenger data from the Titanic, including information like age, sex, passenger class, fare, and whether or not the passenger survived. You can access the dataset [here](https://www.kaggle.com/c/titanic/data).

## Requirements

This project is implemented in Python, with the use of the following libraries:

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn

## Steps

1. **Data Exploration**: The structure of the dataset was explored, including the types and distributions of variables.
2. **Data Cleaning**: This step involved dealing with missing values and outliers in the dataset.
3. **Feature Engineering**: New features were created from existing ones to provide more valuable information for the model.
4. **Data Preprocessing**: Data was preprocessed for machine learning, including encoding categorical variables, scaling numerical features, and splitting the data into training and test sets.
5. **Model Building**: A logistic regression model was initially built, and its performance served as a benchmark for other models. I then experimented with other algorithms like decision trees and random forests.
6. **Model Evaluation**: The performance of the models was evaluated using metrics appropriate for binary classification, such as accuracy, precision, recall, and the ROC AUC score.
7. **Model Optimization**: The hyperparameters of the best-performing model were tuned for optimal performance.

## Results

The final model achieved an accuracy of XX% on the test set. Detailed results and discussion can be found in the [Jupyter notebook](https://github.com/dev-ro/machine-learning-projects/blob/main/beginner/titanic%20survival%20prediction/titanic.ipynb).

## Future Work

In the future, I plan to explore more complex models and feature engineering techniques to further improve the performance.
