# Recommender System

## Project Overview

In this project, I developed a recommender system for movies. Recommender systems are vital in the digital space as they help users discover new content and help businesses increase user engagement on their platform.

## Dataset

The dataset used for this project is the [MovieLens dataset](https://grouplens.org/datasets/movielens/), which contains ratings of movies by a large number of users.

## Requirements

This project is implemented in Python, with the use of the following libraries:

- Pandas
- Numpy
- Scikit-learn
- LightFM

## Steps

1. **Data Exploration**: Performed exploratory data analysis to understand the structure and characteristics of the dataset.
2. **Data Preprocessing**: Preprocessed the data, such as handling missing values and transforming data types, if necessary.
3. **Model Building**: Implemented two types of recommender systems: Content-based and Collaborative filtering. The LightFM library was used for the latter.
4. **Model Evaluation**: Evaluated the performance of the models using precision at k and AUC score.
5. **Model Usage**: Used the trained model to generate movie recommendations for users.

## Results

The final model achieved a precision at k of XX and an AUC score of YY on the test set. More detailed results and discussions can be found in the [Jupyter notebook](link-to-notebook).

## Future Work

Plans for future work include experimenting with hybrid methods, integrating implicit feedback, and exploring deep learning approaches for recommendation systems.
