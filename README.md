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
    - Frontend: You can start using the app by visiting [http://localhost:3000](http://localhost:3000)
    - Backend: The FastApi backend that serves the React frontend can be accessed using [http://localhost:8000](http://localhost:8000)
    - Database: The Qdrant vector database dashboard can be accessed using [http://localhost:6333/dashboard](http://localhost:6333/dashboard)


## Model Architecture

<!-- insert image here -->
<!-- ![plot](./assets/model_architecture.png) -->
<p align="center" style="height: 600px">
  <img src="./assets/model_architecture.png" />
</p>
