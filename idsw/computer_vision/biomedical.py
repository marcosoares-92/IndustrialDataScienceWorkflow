"""
idsw.computer_vision.biomedical
===============================
Biomedical image analysis pipelines based on scipy.ndimage, covering multi-dimensional
volume analysis, connected component labeling, morphological measurements, and intensity windowing.
"""

import numpy as np
import scipy.ndimage as ndimage
import pandas as pd
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars


def apply_windowing(image, window_center, window_width):
    """
    apply_windowing:
    Applies Hounsfield Unit (HU) windowing to CT or MRI biomedical scans.
    Maps voxel intensities within [window_center - window_width/2, window_center + window_width/2] to [0, 255].

    : param: image: numpy ndarray of voxel intensities.
    : param: window_center: center level of the window (e.g. 40 for soft tissue, 400 for bone, -600 for lung).
    : param: window_width: width of the window (e.g. 400 for soft tissue, 1500 for bone).
    : return: windowed image scaled to [0, 255] uint8.
    """
    img = np.asarray(image, dtype = float)
    min_val = window_center - (window_width / 2.0)
    max_val = window_center + (window_width / 2.0)

    windowed = np.clip(img, min_val, max_val)
    windowed = ((windowed - min_val) / (max_val - min_val) * 255.0).astype(np.uint8)
    return windowed


def biomedical_segmentation(volume_or_slice, threshold = None, min_size = 30):
    """
    biomedical_segmentation:
    Segments anatomical structures or regions of interest from 2D or 3D biomedical scans.
    Identifies connected components, filters small noise artifacts, and returns labeled masks.

    : param: volume_or_slice: 2D or 3D numpy ndarray.
    : param: threshold: intensity threshold. If None, uses mean + standard deviation.
    : param: min_size: minimum pixel/voxel count to retain an object.
    : return: tuple (labeled_array, num_features, cleaned_mask).
    """
    arr = np.asarray(volume_or_slice)

    if threshold is None:
        threshold = np.mean(arr) + np.std(arr)

    mask = arr > threshold
    # Fill holes
    filled_mask = ndimage.binary_fill_holes(mask)

    # Label connected components
    structure = ndimage.generate_binary_structure(arr.ndim, 1)
    labeled_array, num_features = ndimage.label(filled_mask, structure = structure)

    # Filter out components smaller than min_size
    component_sizes = ndimage.sum(filled_mask, labeled_array, range(num_features + 1))
    too_small = component_sizes < min_size
    too_small_mask = too_small[labeled_array]
    labeled_array[too_small_mask] = 0

    # Relabel clean components
    cleaned_mask = labeled_array > 0
    labeled_array, num_features = ndimage.label(cleaned_mask, structure = structure)

    if ControlVars.show_results:
        print(f"Biomedical segmentation complete: {num_features} distinct anatomical objects detected.")

    return labeled_array, num_features, cleaned_mask


def measure_biomedical_objects(segmented_mask, intensity_image = None):
    """
    measure_biomedical_objects:
    Calculates quantitative morphological measurements for each segmented region:
    volume/area (voxel count), center of mass (centroid), bounding box, and intensity statistics.

    : param: segmented_mask: integer labeled ndarray where each unique int > 0 represents an object.
    : param: intensity_image: optional raw image array for computing mean and max voxel intensity.
    : return: pandas DataFrame with object measurements.
    """
    labels = np.unique(segmented_mask)
    labels = labels[labels != 0]

    records = []
    for lbl in labels:
        mask_lbl = (segmented_mask == lbl)
        volume = int(np.sum(mask_lbl))
        com = ndimage.center_of_mass(mask_lbl)
        slices = ndimage.find_objects(segmented_mask == lbl)[0]

        rec = {
            "label_id": int(lbl),
            "voxel_count": volume,
            "center_of_mass": tuple(np.round(com, 2)),
            "bounding_box": str(slices)
        }

        if intensity_image is not None:
            voxels = intensity_image[mask_lbl]
            rec["mean_intensity"] = float(np.mean(voxels))
            rec["std_intensity"] = float(np.std(voxels))
            rec["max_intensity"] = float(np.max(voxels))
            rec["min_intensity"] = float(np.min(voxels))

        records.append(rec)

    measurements_df = pd.DataFrame(records)

    if ControlVars.show_results and len(measurements_df) > 0:
        print("Biomedical Object Morphological Measurements:")
        try:
            from IPython.display import display
            display(measurements_df.head(10))
        except Exception:
            print(measurements_df.head(10).to_string())

    return measurements_df


def biomedical_resample(image, zoom_factors = (1.0, 1.0, 1.0), order = 1):
    """
    biomedical_resample:
    Resamples a multi-dimensional medical volume to isotropic voxel spacing.

    : param: image: numpy ndarray (2D or 3D).
    : param: zoom_factors: tuple of scaling factors per axis.
    : param: order: spline interpolation order (default 1 for linear).
    : return: resampled numpy array.
    """
    return ndimage.zoom(image, zoom = zoom_factors, order = order)
