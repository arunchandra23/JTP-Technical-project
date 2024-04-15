# Image Recommendation System Using Autoencoders

## Overview

This project implements an image recommendation system that leverages an autoencoder model to analyze and recommend products based on visual similarity. Initially starting with handcrafted techniques and transitioning to deep learning, the system allows users to view products and receive suggestions for similar items, enhancing user engagement and satisfaction by providing a personalized shopping experience.

## Approach - 1

Initially, the project employed handcrafted image processing techniques, utilizing color histograms, texture features, and edge detection to analyze product images. While these methods provided a foundational approach to image similarity, they fell short in capturing complex patterns and variations across different products, leading to unsatisfactory recommendation accuracy.

Recognizing the limitations of the initial approach, the project transitioned to a more advanced deep learning method by employing an autoencoder. This shift was aimed at extracting deeper and more abstract features from the images in an unsupervised manner, significantly improving the quality and relevance of the recommendations.

[View the notebook here[Depricated]](./depricated/Approach_1.ipynb)

## Approach - 2

### Why Use an Autoencoder?

The autoencoder is central to our updated system for its ability to learn efficient representations (feature vectors) in an unsupervised manner. This capability is crucial since it allows us to effectively utilize unlabeled image data, focusing solely on the visual features of the products. These learned representations are then used to identify and recommend products that are visually similar to a given item.

### Model Architecture

The autoencoder model is designed to compress image data into a lower-dimensional latent space and then reconstruct the original data from this compressed form. The architecture is split into two main components: the encoder and the decoder.

#### Encoder

- **Input Layer:** Accepts RGB images resized to 32x32 pixels.
- **Convolutional Layers:** Two convolutional layers with ReLU activation are used. The first layer has 32 filters of size 3x3, followed by a max pooling layer. The second convolutional layer has 64 filters of size 3x3, also followed by a max pooling layer.
- **Flattening Layer:** Flattens the output of the convolutional layers into a single vector.
- **Dense Layer:** A dense layer with 128 neurons (ReLU activated) processes the flattened vector.
- **Latent Space Layer:** The final layer of the encoder outputs a 32-dimensional latent representation of the input.

#### Decoder

- **Dense Layer:** Starts with a dense layer of 64 neurons.
- **Reshape Layer:** Adjusts the dimensionality to match the expected input of the subsequent convolutional transpose layers.
- **Convolutional Transpose Layers:** Mirrors the encoder's convolutional layers but in reverse, using convolutional transpose operations to upscale the image back to its original dimensions.
- **Output Layer:** A convolutional layer with a sigmoid activation function produces the reconstructed image with the same shape as the input.

<p align="center">
  <img src="./model_architecture.png" alt="Model Architecture" style="height: 600px;" />
</p>

## Image Feature Extraction

Once trained, the encoder part of the autoencoder is used to extract features from images. These features, or latent representations, are then stored in a vector database (Qdrant), enabling efficient retrieval of similar images based on their content.

## Recommendations

The recommendation mechanism utilizes the vector database to perform cosine similarity, finding images whose feature vectors are closest to that of the query image, thereby suggesting products with the most visual similarity.

## Conclusion

The use of an autoencoder in this image recommendation system provides a robust method for handling and analyzing image data without the need for labels. This approach not only simplifies the processing pipeline but also enhances the system's ability to offer relevant and visually appealing product recommendations.
