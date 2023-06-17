# Spam Detector

## Project Overview

In this project, a machine learning model was developed to distinguish between spam and non-spam (ham) emails. This is a classic text classification problem that incorporates Natural Language Processing (NLP) techniques.

## Dataset

The dataset used for this project is the [SMS Spam Collection Dataset](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) from the UCI Machine Learning Repository. It comprises of labeled emails categorized as either 'spam' or 'ham'.

## Requirements

This project is implemented in Python, with the following libraries:

- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- NLTK

## Steps

1. **Data Exploration**: The structure of the dataset was explored and key characteristics of spam and non-spam emails were identified.
2. **Data Preprocessing**: Emails were preprocessed using NLP techniques, including tokenization, lemmatization, and removal of stop words. The Bag of Words model was used to transform the text data into a format suitable for machine learning.
3. **Model Building**: A Naive Bayes classifier was used as the baseline model. Other models like SVM and Random Forests were also explored.
4. **Model Evaluation**: The performance of the models was evaluated using metrics like precision, recall, accuracy, and the F1 score.
5. **Model Optimization**: Hyperparameters of the best-performing model were tuned to optimize the model's performance.

## Results

The final model achieved an accuracy of XX% on the test set. More detailed results and discussions can be found in the [Jupyter notebook](link-to-notebook).

## Future Work

Future work will involve experimenting with different feature extraction techniques such as TF-IDF and exploring deep learning models like RNNs and Transformers.
