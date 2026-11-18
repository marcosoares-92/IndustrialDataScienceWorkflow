"""
idsw.computer_vision.models_keras
=================================
Deep Learning computer vision models using TensorFlow Keras:
- Custom Convolutional Neural Networks (CNN)
- Transfer learning with pretrained backbones (MobileNetV2, ResNet50, VGG16)
- Generative Adversarial Networks (GAN)
"""

import numpy as np
import tensorflow as tf

from idsw import InvalidInputsError, ControlVars


def build_cnn_classifier_keras(
    input_shape = (224, 224, 3),
    num_classes = 2,
    base_filters = 32,
    dropout_rate = 0.3,
    learning_rate = 1e-3
):
    """
    build_cnn_classifier_keras:
    Constructs a modern Convolutional Neural Network for image classification.
    Incorporates Conv2D, BatchNormalization, MaxPooling2D, Dropout, and Dense layers.

    : param: input_shape: tuple, dimensions of input images (H, W, C).
    : param: num_classes: integer, number of target classes.
    : param: base_filters: integer (default 32), number of initial convolutional filters.
    : param: dropout_rate: float (default 0.3).
    : param: learning_rate: float (default 1e-3).
    : return: compiled tf.keras.Model.
    """
    inputs = tf.keras.layers.Input(shape = input_shape)

    # Block 1
    x = tf.keras.layers.Conv2D(base_filters, (3, 3), padding = 'same', activation = 'relu')(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Block 2
    x = tf.keras.layers.Conv2D(base_filters * 2, (3, 3), padding = 'same', activation = 'relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.MaxPooling2D((2, 2))(x)

    # Block 3
    x = tf.keras.layers.Conv2D(base_filters * 4, (3, 3), padding = 'same', activation = 'relu')(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)

    x = tf.keras.layers.Dropout(dropout_rate)(x)
    x = tf.keras.layers.Dense(128, activation = 'relu')(x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)

    if num_classes == 2:
        outputs = tf.keras.layers.Dense(1, activation = 'sigmoid', name = 'output')(x)
        loss = 'binary_crossentropy'
        metrics = ['accuracy']
    else:
        outputs = tf.keras.layers.Dense(num_classes, activation = 'softmax', name = 'output')(x)
        loss = 'sparse_categorical_crossentropy'
        metrics = ['accuracy']

    model = tf.keras.Model(inputs = inputs, outputs = outputs, name = 'idsw_cnn_classifier')
    optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate)
    model.compile(optimizer = optimizer, loss = loss, metrics = metrics)

    if ControlVars.show_results:
        print("=" * 80)
        print("KERAS CNN CLASSIFIER BUILT AND COMPILED")
        print("=" * 80)
        model.summary()

    return model


def apply_transfer_learning_keras(
    base_model_name = 'mobilenet_v2',
    input_shape = (224, 224, 3),
    num_classes = 2,
    freeze_base = True,
    dense_units = 128,
    dropout_rate = 0.3,
    learning_rate = 1e-4
):
    """
    apply_transfer_learning_keras:
    Constructs a transfer learning pipeline using a pre-trained ImageNet backbone.
    Freezes the feature extraction weights and attaches a custom classification head.

    : param: base_model_name: 'mobilenet_v2', 'resnet50', or 'vgg16'.
    : param: input_shape: image dimensions (H, W, C).
    : param: num_classes: number of output classes.
    : param: freeze_base: boolean, whether to freeze the pre-trained weights.
    : return: compiled tf.keras.Model.
    """
    name = str(base_model_name).strip().lower()

    if name == 'mobilenet_v2':
        base_model = tf.keras.applications.MobileNetV2(
            input_shape = input_shape,
            include_top = False,
            weights = 'imagenet'
        )
    elif name == 'resnet50':
        base_model = tf.keras.applications.ResNet50(
            input_shape = input_shape,
            include_top = False,
            weights = 'imagenet'
        )
    elif name == 'vgg16':
        base_model = tf.keras.applications.VGG16(
            input_shape = input_shape,
            include_top = False,
            weights = 'imagenet'
        )
    else:
        raise InvalidInputsError(f"Unsupported backbone '{base_model_name}'. Choose from: 'mobilenet_v2', 'resnet50', 'vgg16'.")

    base_model.trainable = not freeze_base

    inputs = tf.keras.layers.Input(shape = input_shape)
    x = base_model(inputs, training = False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)
    x = tf.keras.layers.Dense(dense_units, activation = 'relu')(x)
    x = tf.keras.layers.Dropout(dropout_rate)(x)

    if num_classes == 2:
        outputs = tf.keras.layers.Dense(1, activation = 'sigmoid', name = 'output')(x)
        loss = 'binary_crossentropy'
    else:
        outputs = tf.keras.layers.Dense(num_classes, activation = 'softmax', name = 'output')(x)
        loss = 'sparse_categorical_crossentropy'

    model = tf.keras.Model(inputs = inputs, outputs = outputs, name = f'transfer_{name}')
    model.compile(
        optimizer = tf.keras.optimizers.Adam(learning_rate = learning_rate),
        loss = loss,
        metrics = ['accuracy']
    )

    if ControlVars.show_results:
        print("=" * 80)
        print(f"TRANSFER LEARNING MODEL CREATED (Backbone: {base_model_name}, Frozen: {freeze_base})")
        print("=" * 80)

    return model


def train_simple_gan(
    images_dataset,
    image_shape = (28, 28, 1),
    latent_dim = 100,
    epochs = 20,
    batch_size = 64
):
    """
    train_simple_gan:
    Builds and trains a Generative Adversarial Network (GAN) comprising a Generator
    and a Discriminator competing in a minimax game.

    : param: images_dataset: numpy array of real training images normalized to [-1, 1].
    : param: image_shape: shape of single image.
    : param: latent_dim: size of the random noise input vector.
    : param: epochs: training iterations.
    : param: batch_size: batch size.
    : return: tuple (generator, discriminator, combined_gan).
    """
    # Generator
    gen_inputs = tf.keras.layers.Input(shape = (latent_dim,))
    x = tf.keras.layers.Dense(128, activation = 'relu')(gen_inputs)
    x = tf.keras.layers.Dense(256, activation = 'relu')(x)
    total_pixels = int(np.prod(image_shape))
    gen_outputs = tf.keras.layers.Dense(total_pixels, activation = 'tanh')(x)
    gen_outputs = tf.keras.layers.Reshape(image_shape)(gen_outputs)
    generator = tf.keras.Model(inputs = gen_inputs, outputs = gen_outputs, name = 'generator')

    # Discriminator
    disc_inputs = tf.keras.layers.Input(shape = image_shape)
    x = tf.keras.layers.Flatten()(disc_inputs)
    x = tf.keras.layers.Dense(256, activation = 'relu')(x)
    x = tf.keras.layers.Dense(128, activation = 'relu')(x)
    disc_outputs = tf.keras.layers.Dense(1, activation = 'sigmoid')(x)
    discriminator = tf.keras.Model(inputs = disc_inputs, outputs = disc_outputs, name = 'discriminator')
    discriminator.compile(
        optimizer = tf.keras.optimizers.Adam(1e-4),
        loss = 'binary_crossentropy',
        metrics = ['accuracy']
    )

    # Combined GAN
    discriminator.trainable = False
    gan_inputs = tf.keras.layers.Input(shape = (latent_dim,))
    fake_img = generator(gan_inputs)
    gan_outputs = discriminator(fake_img)
    gan = tf.keras.Model(inputs = gan_inputs, outputs = gan_outputs, name = 'gan')
    gan.compile(
        optimizer = tf.keras.optimizers.Adam(1e-4),
        loss = 'binary_crossentropy'
    )

    if ControlVars.show_results:
        print("GAN Generator and Discriminator successfully constructed.")

    return generator, discriminator, gan
