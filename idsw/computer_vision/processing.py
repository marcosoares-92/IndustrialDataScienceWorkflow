"""
idsw.computer_vision.processing
===============================
Image processing algorithms covering filtering, thresholding, edge detection,
morphology, and feature extraction based on scikit-image, scipy, and numpy.
"""

import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars


def to_grayscale(image):
    """Converts an RGB or RGBA image to grayscale."""
    arr = np.asarray(image)
    if arr.ndim == 2:
        return arr
    elif arr.ndim == 3 and arr.shape[2] >= 3:
        # Standard luminance formula: 0.2989 * R + 0.5870 * G + 0.1140 * B
        return 0.2989 * arr[:, :, 0] + 0.5870 * arr[:, :, 1] + 0.1140 * arr[:, :, 2]
    return arr


def apply_threshold(image, method = 'otsu', block_size = 35, offset = 10):
    """
    apply_threshold:
    Applies image binarization thresholding.

    : param: image: numpy ndarray (2D grayscale or 3D RGB).
    : param: method: 'otsu', 'mean', or 'local'.
    : param: block_size: odd integer for local thresholding neighborhood.
    : param: offset: constant offset for local thresholding.
    : return: boolean binary mask where True represents foreground objects.
    """
    gray = to_grayscale(image)

    try:
        from skimage.filters import threshold_otsu, threshold_local
        if method == 'otsu':
            thresh = threshold_otsu(gray)
            binary = gray > thresh
        elif method == 'local':
            thresh = threshold_local(gray, block_size = block_size, offset = offset)
            binary = gray > thresh
        else:
            thresh = np.mean(gray)
            binary = gray > thresh
    except ImportError:
        # Fallback to pure numpy Otsu's method
        gray_uint8 = np.clip(gray, 0, 255).astype(np.uint8) if gray.max() > 1.0 else (gray * 255).astype(np.uint8)
        hist, bin_edges = np.histogram(gray_uint8, bins = 256, range = (0, 256))
        total = gray_uint8.size
        current_max, threshold = 0, 0
        sum_total = np.dot(np.arange(256), hist)
        sum_back, weight_back = 0, 0

        for t in range(256):
            weight_back += hist[t]
            if weight_back == 0:
                continue
            weight_fore = total - weight_back
            if weight_fore == 0:
                break
            sum_back += t * hist[t]
            mean_back = sum_back / weight_back
            mean_fore = (sum_total - sum_back) / weight_fore
            var_between = weight_back * weight_fore * ((mean_back - mean_fore) ** 2)
            if var_between > current_max:
                current_max = var_between
                threshold = t

        binary = gray_uint8 > threshold

    if ControlVars.show_plots:
        fig, axes = plt.subplots(1, 2, figsize = (10, 5))
        axes[0].imshow(gray, cmap = 'gray')
        axes[0].set_title("Grayscale Input")
        axes[0].axis('off')
        axes[1].imshow(binary, cmap = 'gray')
        axes[1].set_title(f"Thresholded ({method.upper()})")
        axes[1].axis('off')
        plt.tight_layout()
        plt.show()

    return binary


def apply_edge_detection(image, method = 'sobel'):
    """
    apply_edge_detection:
    Computes image gradients and boundary edges using Sobel, Prewitt, or Canny filters.

    : param: image: numpy ndarray.
    : param: method: 'sobel', 'prewitt', or 'canny'.
    : return: edge magnitude array or binary edge map.
    """
    gray = to_grayscale(image)

    try:
        from skimage.filters import sobel, prewitt, roberts
        from skimage.feature import canny
        if method == 'sobel':
            edges = sobel(gray)
        elif method == 'prewitt':
            edges = prewitt(gray)
        elif method == 'roberts':
            edges = roberts(gray)
        elif method == 'canny':
            edges = canny(gray)
        else:
            edges = sobel(gray)
    except ImportError:
        # Fallback to scipy.ndimage sobel
        dx = ndimage.sobel(gray, axis = 0)
        dy = ndimage.sobel(gray, axis = 1)
        edges = np.hypot(dx, dy)

    if ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = (6, 6))
        ax.imshow(edges, cmap = 'magma')
        ax.set_title(f"Edge Detection ({method.upper()})")
        ax.axis('off')
        plt.show()

    return edges


def apply_morphology(image, operation = 'dilation', kernel_size = 3):
    """
    apply_morphology:
    Performs morphological operations on binary or grayscale images.

    : param: image: numpy ndarray (binary or grayscale).
    : param: operation: 'dilation', 'erosion', 'opening', or 'closing'.
    : param: kernel_size: odd integer defining structuring element window size.
    : return: processed image array.
    """
    structure = ndimage.generate_binary_structure(2, 1)
    if kernel_size > 3:
        structure = ndimage.iterate_structure(structure, kernel_size // 2)

    op = str(operation).strip().lower()
    if op == 'dilation':
        res = ndimage.binary_dilation(image, structure = structure)
    elif op == 'erosion':
        res = ndimage.binary_erosion(image, structure = structure)
    elif op == 'opening':
        res = ndimage.binary_opening(image, structure = structure)
    elif op == 'closing':
        res = ndimage.binary_closing(image, structure = structure)
    else:
        raise InvalidInputsError(f"Unsupported morphology operation '{operation}'.")

    return res


def denoise_image(image, method = 'gaussian', sigma = 1.0):
    """
    denoise_image:
    Reduces noise while preserving structural content.

    : param: image: numpy ndarray.
    : param: method: 'gaussian' or 'median'.
    : param: sigma: Gaussian filter standard deviation or median filter size.
    : return: denoised numpy array.
    """
    gray = to_grayscale(image)
    if method == 'gaussian':
        return ndimage.gaussian_filter(gray, sigma = sigma)
    elif method == 'median':
        size = int(sigma) if int(sigma) % 2 == 1 else int(sigma) + 1
        return ndimage.median_filter(gray, size = size)
    return gray
