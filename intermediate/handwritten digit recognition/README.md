# Handwritten Digit Recognition

## Project Overview

In this project, a Convolutional Neural Network (CNN) was implemented to recognize handwritten digits. This is a multiclass classification problem that is often used as a basic introduction to the application of deep learning techniques.

## Dataset

The dataset used in this project is the [MNIST dataset](http://yann.lecun.com/exdb/mnist/), a large database of handwritten digits that is widely used for training and testing in the field of machine learning.

## Requirements

This project is implemented in Python, with the use of the following libraries:

- TensorFlow
- Keras
- Matplotlib
- Numpy

## Steps

1. **Data Exploration and Preprocessing**: The dataset was explored and preprocessed, which included normalizing the image pixel values and encoding the labels.
2. **Model Building**: A Convolutional Neural Network (CNN) was built using the Keras library. It includes layers such as Convolution2D, MaxPooling2D, Flatten and Dense.
3. **Training**: The model was trained on the MNIST dataset using an appropriate optimizer and loss function for multiclass classification.
4. **Model Evaluation**: The model's performance was evaluated on a test set, and a confusion matrix was used to identify misclassified digits.
5. **Prediction Visualization**: Predictions were visualized using Matplotlib, including a display of the image, predicted label, and true label.

## Results

The final model achieved an accuracy of XX% on the test set. Detailed results and discussion can be found in the [Jupyter notebook](link-to-notebook).

## Future Work

In future work, I plan to experiment with more complex CNN architectures, data augmentation techniques, and other optimization methods to improve performance.
