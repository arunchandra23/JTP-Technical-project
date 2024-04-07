# JTP-Technical-project - Image Recommendation System

## Overview

This project aims to build an Image Recommendation System that enhances the user's shopping experience by suggesting visually similar products. When a user views a product, the system recommends other products that resemble the viewed item, providing a personalized and engaging shopping experience.

### Core Engine

The recommendation engine is powered by an autoencoder model, which is employed to learn image features in an unsupervised manner. The encoder component of the autoencoder is utilized to generate feature vectors for the images, which are then stored in a Qdrant vector database. This enables efficient similarity search and retrieval of similar products based on their visual content.

### Dataset

The model is trained on a dataset from Kaggle, which contains 44k fashion products with multiple category labels, descriptions, and high-resolution images. The dataset can be found here: [Fashion Product Images Dataset](https://www.kaggle.com/datasets/paramaggarwal/fashion-product-images-dataset?rvi=1)

### Technology Stack

- **Backend:** The backend is built using **FastAPI**, a modern, fast web framework for building APIs with Python.
- **Frontend:** The frontend is developed using **React JS**, with **Redux** for state management, providing a responsive and interactive user interface.
- **Vector Database:** **Qdrant** is used as the vector database for storing and querying the image feature vectors, facilitating efficient similarity search.

## Model Architecture

### Encoder:

- **Input:** 32x32 RGB images
- **Convolutional Layer 1:** 32 filters, 3x3 kernel, ReLU activation
- **Max Pooling Layer 1:** 2x2 pool size
- **Convolutional Layer 2:** 64 filters, 3x3 kernel, ReLU activation
- **Max Pooling Layer 2:** 2x2 pool size
- **Flatten Layer**
- **Dense Layer 1:** 128 neurons, ReLU activation
- **Dense Layer 2:** 64 neurons, ReLU activation
- **Latent Space Layer:** 32 neurons, ReLU activation

### Decoder:

- **Dense Layer 1:** 64 neurons, ReLU activation
- **Dense Layer 2:** 128 neurons, ReLU activation
- **Reshape Layer**
- **Convolutional Transpose Layers:** Mirroring the encoder
- **Output Layer:** 3 filters (RGB channels), 3x3 kernel, sigmoid activation

<!-- insert image here -->
<!-- ![plot](./assets/model_architecture.png) -->
<p align="center">
  <img src="./assets/model_architecture.png" />
</p>

## Setup Instructions

1. **Clone the Repository:**
   ```python
   git clone -b main https://github.com/arunchandra23/JTP-Technical-project.git
   ```
2. **Inference:**
    ```bash
   cd JTP-Technical-project/
   ```
   - You can directly use the application by loading the saved model and embeddings with the docker
        ```bash
        docker-compose build
        docker-compose up
        ```
