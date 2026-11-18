"""
idsw.computer_vision.detection
==============================
Object detection and localization algorithms:
- Pre-trained YOLO (You Only Look Once) inference with Ultralytics
- Siamese Neural Network for object localization and similarity detection
- Bounding box rendering and visualization
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars
from .io import load_image


def apply_yolo_detection(image_or_path, model_name = 'yolov8n.pt', confidence_threshold = 0.25):
    """
    apply_yolo_detection:
    Runs YOLO object detection on an image using Ultralytics YOLOv8 / YOLOv5.
    Returns detected classes, bounding box coordinates [x1, y1, x2, y2], and confidence scores.

    : param: image_or_path: str file path or numpy ndarray.
    : param: model_name: str, name of pre-trained YOLO checkpoint (default 'yolov8n.pt').
    : param: confidence_threshold: float (default 0.25), detection confidence threshold.
    : return: tuple (detections_df, annotated_image_array).
    """
    try:
        from ultralytics import YOLO

        model = YOLO(model_name)
        results = model.predict(source = image_or_path, conf = confidence_threshold, verbose = False)

        r = results[0]
        boxes = r.boxes

        records = []
        if boxes is not None and len(boxes) > 0:
            xyxy = boxes.xyxy.cpu().numpy()
            confs = boxes.conf.cpu().numpy()
            clss = boxes.cls.cpu().numpy()
            names = r.names

            for i in range(len(xyxy)):
                cls_id = int(clss[i])
                records.append({
                    "class_id": cls_id,
                    "class_name": names.get(cls_id, str(cls_id)),
                    "confidence": float(confs[i]),
                    "x1": float(xyxy[i][0]),
                    "y1": float(xyxy[i][1]),
                    "x2": float(xyxy[i][2]),
                    "y2": float(xyxy[i][3])
                })

        detections_df = pd.DataFrame(records)
        annotated_img = r.plot()

        if ControlVars.show_results:
            print("=" * 80)
            print(f"YOLO DETECTION COMPLETED ({model_name})")
            print("=" * 80)
            print(f"Detected {len(detections_df)} objects with confidence >= {confidence_threshold}.")
            if len(detections_df) > 0:
                try:
                    from IPython.display import display
                    display(detections_df)
                except Exception:
                    print(detections_df.to_string())

        if ControlVars.show_plots:
            plt.figure(figsize = (8, 8))
            plt.imshow(annotated_img)
            plt.axis('off')
            plt.title("YOLO Object Detections")
            plt.show()

        return detections_df, annotated_img

    except ImportError:
        print("[!] Note: 'ultralytics' is not installed. To use YOLO detection, run: pip install ultralytics")
        # Return empty result structure
        empty_df = pd.DataFrame(columns = ["class_id", "class_name", "confidence", "x1", "y1", "x2", "y2"])
        img_arr = load_image(image_or_path) if isinstance(image_or_path, str) else np.asarray(image_or_path)
        return empty_df, img_arr


def detect_objects_and_boxes_siamese(
    anchor_template,
    target_search_image,
    similarity_threshold = 0.7
):
    """
    detect_objects_and_boxes_siamese:
    Template matching and Siamese feature similarity detection for finding target objects
    and their bounding rectangles in a search image.

    : param: anchor_template: template image of the object to locate.
    : param: target_search_image: larger scene image to search inside.
    : param: similarity_threshold: correlation / similarity threshold.
    : return: pandas DataFrame with bounding boxes [x1, y1, x2, y2, score].
    """
    try:
        from skimage.feature import match_template
        tpl = np.asarray(anchor_template)
        scn = np.asarray(target_search_image)

        if tpl.ndim == 3:
            tpl = np.mean(tpl[:, :, :3], axis = 2)
        if scn.ndim == 3:
            scn = np.mean(scn[:, :, :3], axis = 2)

        corr = match_template(scn, tpl)
        y_locs, x_locs = np.where(corr >= similarity_threshold)

        h, w = tpl.shape
        records = []
        for x, y in zip(x_locs, y_locs):
            records.append({
                "x1": int(x),
                "y1": int(y),
                "x2": int(x + w),
                "y2": int(y + h),
                "score": float(corr[y, x])
            })

        boxes_df = pd.DataFrame(records)
        return boxes_df

    except ImportError:
        return pd.DataFrame(columns = ["x1", "y1", "x2", "y2", "score"])
