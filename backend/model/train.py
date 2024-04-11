import tensorflow as tf
from tensorflow.keras import layers, models
import argparse

def create_data_generator(image_directory, batch_size, image_size):
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    generator = datagen.flow_from_directory(
        directory=image_directory,
        target_size=image_size,
        color_mode='rgb',
        batch_size=batch_size,
        class_mode=None,  # No labels needed
        shuffle=True
    )
    return generator

def create_autoencoder_generator(image_generator):
    for batch in image_generator:
        yield (batch, batch)

def build_autoencoder(input_shape):
    # Encoder
    encoder = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu')  # Latent representation (1D vector)
    ])
    
    # Decoder
    decoder = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(32,)),
        layers.Dense(128, activation='relu'),
        layers.Dense(input_shape[0] * input_shape[1] * input_shape[2], activation='sigmoid'),
        layers.Reshape(input_shape)
    ])
    
    # Autoencoder
    autoencoder = models.Sequential([encoder, decoder])
    
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
    
    return autoencoder

def main(train_directory, test_directory, batch_size, image_size, epochs, model_path):
    # Create the data generators
    train_generator = create_data_generator(train_directory, batch_size, image_size)
    test_generator = create_data_generator(test_directory, batch_size, image_size)

    # Create the autoencoder generator
    autoencoder_train_generator = create_autoencoder_generator(train_generator)
    autoencoder_test_generator = create_autoencoder_generator(test_generator)

    # Build the autoencoder
    autoencoder = build_autoencoder(input_shape=image_size + (3,))  # 3 channels for RGB

    # Train the autoencoder
    autoencoder.fit(
        autoencoder_train_generator,
        steps_per_epoch=len(train_generator),
        validation_data=autoencoder_test_generator,
        validation_steps=len(test_generator),
        epochs=epochs
    )

    # Save the model
    autoencoder.save(model_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train an autoencoder on image data.')
    parser.add_argument('--train_directory', type=str,default="backend/data/Train/", help='Path to the training data directory.')
    parser.add_argument('--test_directory', type=str,default="backend/data/Test/", help='Path to the testing data directory.')
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size for training.')
    parser.add_argument('--image_size', type=int, nargs=2, default=[32, 32], help='Size of the input images (width, height).')
    parser.add_argument('--epochs', type=int, default=2, help='Number of epochs to train.')
    parser.add_argument('--model_path', type=str, default='backend/model/encoder_model.keras', help='Path to save the trained model.')

    args = parser.parse_args()

    main(
        train_directory=args.train_directory,
        test_directory=args.test_directory,
        batch_size=args.batch_size,
        image_size=tuple(args.image_size),
        epochs=args.epochs,
        model_path=args.model_path
    )
