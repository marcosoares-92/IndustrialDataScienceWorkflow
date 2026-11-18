"""
idsw.computer_vision.io
=======================
Functions for reading, saving, and preparing image data files and directory structures
for deep learning and computer vision workflows.
"""

import os
import shutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars


def load_image(file_path, as_gray = False, target_size = None):
    """
    load_image:
    Loads an image from file_path into a NumPy array with pixel values in [0, 1] or [0, 255].
    Supports resizing and conversion to grayscale.

    : param: file_path: str, full path to the image file.
    : param: as_gray: bool (default False), whether to convert the image to grayscale.
    : param: target_size: tuple (height, width) or None, target resolution for resizing.
    : return: numpy ndarray representing the image.
    """
    if not os.path.exists(file_path):
        raise InvalidInputsError(f"Image file '{file_path}' does not exist.")

    try:
        from PIL import Image
        img = Image.open(file_path)
        if as_gray:
            img = img.convert('L')
        else:
            img = img.convert('RGB')

        if target_size is not None and isinstance(target_size, (tuple, list)):
            img = img.resize((target_size[1], target_size[0]))

        img_arr = np.array(img)
        return img_arr

    except ImportError:
        # Fallback to matplotlib.image
        import matplotlib.image as mpimg
        img_arr = mpimg.imread(file_path)
        if as_gray and img_arr.ndim == 3:
            img_arr = np.mean(img_arr[:, :, :3], axis = 2)
        return img_arr


def save_image(image_array, file_path, quality = 95):
    """
    save_image:
    Saves a NumPy image array to a file.

    : param: image_array: numpy ndarray.
    : param: file_path: destination file path.
    : param: quality: JPEG compression quality (default 95).
    : return: str, path of saved image.
    """
    if not isinstance(image_array, np.ndarray):
        raise InvalidInputsError("image_array must be a valid numpy ndarray.")

    arr = image_array.copy()
    if arr.dtype != np.uint8:
        if arr.max() <= 1.0 and arr.min() >= 0.0:
            arr = (arr * 255).astype(np.uint8)
        else:
            arr = np.clip(arr, 0, 255).astype(np.uint8)

    try:
        from PIL import Image
        img = Image.fromarray(arr)
        img.save(file_path, quality = quality)
    except ImportError:
        plt.imsave(file_path, arr)

    if ControlVars.show_results:
        print(f"Image successfully saved to '{file_path}'.")

    return file_path


def organize_images_into_class_directories(
    source_directory,
    metadata_df,
    filename_col = 'filename',
    class_col = 'class',
    output_directory = 'organized_dataset',
    copy_files = True
):
    """
    organize_images_into_class_directories:
    Organizes a flat directory of images into subdirectories named after their respective class labels.
    This structure is strictly required by TensorFlow (image_dataset_from_directory, ImageDataGenerator)
    and PyTorch (ImageFolder).

    : param: source_directory: str, folder containing raw images.
    : param: metadata_df: pandas DataFrame containing mapping between filenames and classes.
    : param: filename_col: str, column name with image filenames.
    : param: class_col: str, column name with class labels.
    : param: output_directory: str, target directory where class folders will be created.
    : param: copy_files: bool (default True). If True, copies files; if False, moves files.
    : return: dictionary with class counts.
    """
    if not os.path.exists(source_directory):
        raise InvalidInputsError(f"source_directory '{source_directory}' does not exist.")

    if not isinstance(metadata_df, pd.DataFrame):
        raise InvalidInputsError("metadata_df must be a pandas DataFrame.")

    if filename_col not in metadata_df.columns or class_col not in metadata_df.columns:
        raise InvalidInputsError(f"Columns '{filename_col}' and '{class_col}' must be present in metadata_df.")

    os.makedirs(output_directory, exist_ok = True)
    class_counts = {}

    for _, row in metadata_df.iterrows():
        fname = str(row[filename_col])
        cls_name = str(row[class_col])

        src_path = os.path.join(source_directory, fname)
        if not os.path.exists(src_path):
            continue

        target_class_dir = os.path.join(output_directory, cls_name)
        os.makedirs(target_class_dir, exist_ok = True)

        dest_path = os.path.join(target_class_dir, fname)
        if copy_files:
            shutil.copy2(src_path, dest_path)
        else:
            shutil.move(src_path, dest_path)

        class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

    if ControlVars.show_results:
        print("=" * 80)
        print(f"IMAGES ORGANIZED INTO CLASS DIRECTORIES AT: '{output_directory}'")
        print("=" * 80)
        for c, count in class_counts.items():
            print(f"  - Class '{c}': {count} images")

    return class_counts


def create_image_data_generators(
    train_directory,
    val_directory = None,
    target_size = (224, 224),
    batch_size = 32,
    augment = True
):
    """
    create_image_data_generators:
    Builds TensorFlow Keras ImageDataGenerators or image_dataset_from_directory pipelines
    with data augmentation (rotation, zoom, horizontal flip, shear).

    : param: train_directory: directory with training class folders.
    : param: val_directory: directory with validation class folders (optional).
    : param: target_size: image dimensions (height, width).
    : param: batch_size: batch size.
    : param: augment: whether to apply data augmentation to training images.
    : return: tuple (train_generator, val_generator).
    """
    import tensorflow as tf

    if augment:
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rescale = 1.0 / 255.0,
            rotation_range = 20,
            width_shift_range = 0.2,
            height_shift_range = 0.2,
            shear_range = 0.15,
            zoom_range = 0.2,
            horizontal_flip = True,
            fill_mode = 'nearest'
        )
    else:
        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1.0 / 255.0)

    val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale = 1.0 / 255.0)

    train_gen = train_datagen.flow_from_directory(
        train_directory,
        target_size = target_size,
        batch_size = batch_size,
        class_mode = 'categorical'
    )

    val_gen = None
    if val_directory is not None and os.path.exists(val_directory):
        val_gen = val_datagen.flow_from_directory(
            val_directory,
            target_size = target_size,
            batch_size = batch_size,
            class_mode = 'categorical'
        )

    return train_gen, val_gen
