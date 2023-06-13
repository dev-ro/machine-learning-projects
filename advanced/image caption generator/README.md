# Image Caption Generator

## Project Overview

In this project, a model was created that generates captions for images. This task, which combines Computer Vision and Natural Language Processing techniques, is a step towards enabling machines to understand and describe the content of images just like humans.

## Dataset

The dataset used for this project is the [Flickr8k dataset](https://www.kaggle.com/shadabhussain/flickr8k). This dataset includes 8,000 images that are each paired with five different captions, which provide clear descriptions of the salient entities and events.

## Requirements

This project is implemented in Python, with the use of the following libraries:

- TensorFlow
- Keras
- Pandas
- Numpy
- Matplotlib
- NLTK

## Steps

1. **Data Preprocessing**: The images were preprocessed using transfer learning (VGG16 model) and the text data was tokenized.
2. **Model Building**: A deep learning model was created using the Encoder-Decoder architecture, where a Convolutional Neural Network (CNN) was used as an encoder and a Recurrent Neural Network (RNN) was used as a decoder.
3. **Training**: The model was trained using an appropriate optimizer and loss function.
4. **Model Evaluation**: The model's performance was evaluated using BLEU scores, a popular metric for measuring the quality of machine-generated text.
5. **Model Usage**: The trained model was used to generate captions for new images.

## Results

The final model achieved a BLEU score of XX on the test set. More detailed results and discussions can be found in the [Jupyter notebook](link-to-notebook).

## Future Work

Future plans include trying other pre-trained models for image features extraction, experimenting with attention mechanisms in the model, and increasing the size of the dataset to improve the model's performance.
