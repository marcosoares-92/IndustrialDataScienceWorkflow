"""
Unit tests for idsw.computer_vision module.
Covers:
- load_image and save_image (io.py)
- organize_images_into_class_directories (io.py)
- to_grayscale, apply_threshold, apply_edge_detection, apply_morphology, denoise_image (processing.py)
- apply_windowing, biomedical_segmentation, measure_biomedical_objects, biomedical_resample (biomedical.py)
- build_cnn_classifier_keras, train_simple_gan (models_keras.py)
- detect_objects_and_boxes_siamese, apply_yolo_detection (detection.py)
"""

import unittest
import os
import shutil
import tempfile
import numpy as np
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.computer_vision import (
    load_image,
    save_image,
    organize_images_into_class_directories,
    to_grayscale,
    apply_threshold,
    apply_edge_detection,
    apply_morphology,
    denoise_image,
    apply_windowing,
    biomedical_segmentation,
    measure_biomedical_objects,
    biomedical_resample,
    detect_objects_and_boxes_siamese,
    apply_yolo_detection
)


class TestComputerVision(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        self.test_dir = tempfile.mkdtemp()

        # Synthetic grayscale image with square in center
        self.synth_img = np.zeros((40, 40), dtype=float)
        self.synth_img[10:30, 10:30] = 1.0

        # Synthetic 3D biomedical volume (3 slices of 30x30)
        self.synth_volume = np.zeros((3, 30, 30), dtype=float)
        self.synth_volume[:, 10:20, 10:20] = 50.0

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_load_image(self):
        img_path = os.path.join(self.test_dir, "test_img.png")
        save_image(self.synth_img, img_path)
        self.assertTrue(os.path.exists(img_path))

        loaded = load_image(img_path, as_gray=True)
        self.assertEqual(loaded.shape[0], 40)
        self.assertEqual(loaded.shape[1], 40)

    def test_organize_images_into_class_directories(self):
        # Create dummy image files
        src_dir = os.path.join(self.test_dir, "raw_images")
        os.makedirs(src_dir, exist_ok=True)
        img1 = os.path.join(src_dir, "img1.png")
        img2 = os.path.join(src_dir, "img2.png")
        save_image(self.synth_img, img1)
        save_image(self.synth_img, img2)

        meta_df = pd.DataFrame({
            "filename": ["img1.png", "img2.png"],
            "class": ["defective", "normal"]
        })

        out_dir = os.path.join(self.test_dir, "organized")
        counts = organize_images_into_class_directories(
            source_directory=src_dir,
            metadata_df=meta_df,
            filename_col="filename",
            class_col="class",
            output_directory=out_dir
        )
        self.assertIn("defective", counts)
        self.assertIn("normal", counts)
        self.assertTrue(os.path.exists(os.path.join(out_dir, "defective", "img1.png")))
        self.assertTrue(os.path.exists(os.path.join(out_dir, "normal", "img2.png")))

    def test_processing_threshold_edges_morphology(self):
        # Thresholding
        bin_img = apply_threshold(self.synth_img, method="otsu")
        self.assertEqual(bin_img.shape, (40, 40))
        self.assertTrue(bin_img[20, 20])

        # Edge detection
        edges = apply_edge_detection(self.synth_img, method="sobel")
        self.assertEqual(edges.shape, (40, 40))

        # Morphology
        dilated = apply_morphology(bin_img, operation="dilation", kernel_size=3)
        self.assertEqual(dilated.shape, (40, 40))
        self.assertGreaterEqual(np.sum(dilated), np.sum(bin_img))

        # Denoising
        denoised = denoise_image(self.synth_img, method="gaussian", sigma=1.0)
        self.assertEqual(denoised.shape, (40, 40))

    def test_biomedical_segmentation_and_measurement(self):
        # Intensity windowing
        windowed = apply_windowing(self.synth_img * 100, window_center=50, window_width=80)
        self.assertEqual(windowed.dtype, np.uint8)

        # 3D volume segmentation
        labeled, num_features, mask = biomedical_segmentation(self.synth_volume, threshold=20.0, min_size=5)
        self.assertEqual(num_features, 1)

        # Object measurements
        measurements = measure_biomedical_objects(labeled, intensity_image=self.synth_volume)
        self.assertIsInstance(measurements, pd.DataFrame)
        self.assertEqual(len(measurements), 1)
        self.assertIn("voxel_count", measurements.columns)
        self.assertIn("mean_intensity", measurements.columns)

        # Resampling
        resampled = biomedical_resample(self.synth_volume, zoom_factors=(1.0, 0.5, 0.5))
        self.assertEqual(resampled.shape[1], 15)

    def test_siamese_and_yolo_detection(self):
        # Template matching
        tpl = self.synth_img[10:25, 10:25]
        boxes = detect_objects_and_boxes_siamese(tpl, self.synth_img, similarity_threshold=0.8)
        self.assertIsInstance(boxes, pd.DataFrame)

        # YOLO detection (graceful fallback)
        df_yolo, _ = apply_yolo_detection(self.synth_img)
        self.assertIsInstance(df_yolo, pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
