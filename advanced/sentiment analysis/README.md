# Sentiment Analysis

## Project Overview

In this project, a deep learning model was built to perform sentiment analysis on movie reviews. Sentiment analysis is a key task in Natural Language Processing and has wide applications in areas such as brand monitoring, product analysis, and market research.

## Dataset

The dataset used in this project is the [IMDB movie reviews dataset](https://ai.stanford.edu/~amaas/data/sentiment/), which consists of 50,000 polarized movie reviews.

## Requirements

This project is implemented in Python, with the use of the following libraries:

- TensorFlow
- Keras
- Pandas
- Numpy
- Matplotlib
- NLTK

## Steps

1. **Data Exploration and Preprocessing**: The dataset was explored, cleaned, and preprocessed. This included tokenizing the text, removing stop words, and padding sequences.
2. **Model Building**: A recurrent neural network (RNN) was built using Long Short Term Memory (LSTM) units, a type of RNN that is often used for text data.
3. **Training**: The model was trained on the preprocessed data using an appropriate optimizer and loss function.
4. **Model Evaluation**: The model's performance was evaluated on a test set. Accuracy and loss curves were plotted to examine the model's behavior during training.
5. **Model Usage**: The model was used to predict sentiments of new movie reviews.

## Results

The final model achieved an accuracy of XX% on the test set. More detailed results and discussions can be found in the [Jupyter notebook](link-to-notebook).

## Future Work

Future work will include experimenting with different network architectures, implementing attention mechanisms, and trying transformer models like BERT for better performance.
