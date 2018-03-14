# Artificial Intelligence Nanodegree (AIND)

This repo contains my projects, code, and reports for Udacity's [AI Nanodegree](https://www.udacity.com/ai)


The following projects are included:

## Classic Search and AI Projects 

1. [Solve a Sudoku with AI](AIND-Sudoku/)

> Uses classic _constraint propagation_ strategies to solve Sudoku.

2. [Build a Game-Playing Agent](AIND-Isolation/)

> Uses _adversarial search agent_ to play a game called "Isolation", a deterministic, two-player game in which players alternate turns to move a piece from one to another. Implements classic **search algorithms** such as _MiniMax_, _Alpha Beta Search_, _Iterative Deepening Search_, and _Heuristic Search_ algorithms to show different plays.

3. [Implement a Planning Search](AIND-Planning-master/)

> This project implements classic **planning algorithms** often used in logistics problems. Implemented example is for an airline cargo problem. It defines _planning problem_ with initial state and the goal, uses _progression search_ to search the _state space_, and defines _heuristics_ to reach the goals. It experiments with **breadth-first search** and **depth-first search**.

4. [Build a Sign Language Recognizer](AIND-Recognizer/)

> This project implements _probabilistic models_ such as **Hidden Markov Models (HMM)** to implement a sign-language recognizer.

## Deep Learning Projects

The following projects implement deep neural networks that use computer vision to solve challenging real-world tasks, such as image classification, time series prediction, sequence modeling, and a final capstone project for facial keypoints detection.

5. [Dog Breed Classifier](https://github.com/laventura/AIND_dog_breed_classifier)

> This project uses **convolutional neural networks (CNN)** with _transfer learning_ from pre-trained networks (such as _VGG_, _Inception_, _ResNet_) to real world tasks such as classifying images. In this case, it is used to classify dog pictures from among ~130 dog-breeds, a task challenging enough for humans. 

> We use latest deep learning frameworks such as **Keras**(http://keras.io) and **TensorFlow** to create build a CNN architecture from pre-trained models _VGG_, _Inception_, etc. The pre-trained models significantly reduce the challenges in training a new classifier. We experiment with various architectures, and achieve over **82% accuracy** 👍

6. [Time Series Prediction and Text Generation](aind2-rnn/)

> In this project, we perform **sequence modeling** using **Recurrent Neural Networks (RNN) and LSTM**. We use RNNs to predict stock prices (a rather dicey, but interesting problem). We also use LSTMs to achieve **text generation** using a *char-rnn* style generator that learns to generate text character by character. We use this to generate fake _Sherlock Holmes_ style stories. 😀
We use **Keras** to implement the projects. 

7. [Computer Vision Capstone Project: Facial Keypoint Detection](FacialKeypoints-AIND/)

> In the final project, we use advanced _computer vision_ techniques to detect faces in images using filters, and generate facial keypoints.

> We implement a full computer vision pipeline to perform _image pre-processing_ (e.g. transforming color spaces, image de-noising, image blurring, identifying regions of interest, etc.) and _filtering_ to extract portions of images. Then we use _Haar cascades_ to detect faces. We then implement CNNs to identify facial landmarks, and then perform interesting operations on detected faces. 😎

> Project is implemented in _Keras_ and uses _CNN_ to identify features, and regressors to add facial keypoints. More image processing is performed using OpenCV.

