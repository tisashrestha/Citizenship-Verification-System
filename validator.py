import os
import time
import torch
import streamlit as st
from ultralytics import YOLO

model_path = "weights/bestaug.pt"

if torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"


@st.cache_resource
def load_model():
    if not os.path.exists(model_path):
        return None

    return YOLO(model_path)


model = load_model()


def validate_front_side(image_path, confidence_threshold=0.7):

    if model is None:
        return False, "YOLO Model weights (bestt.pt) not found.", [], None

    start = time.time()

    results = model.predict(
        source=image_path,
        conf=confidence_threshold,
        device=DEVICE,
        save=False,
        verbose=False
    )

    print(f"YOLO inference time: {time.time() - start:.2f} seconds")

    detections = []
    found_classes = set()
    annotated_image = None

    for result in results:

        annotated_image = result.plot()

        for box in result.boxes:

            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            confidence = float(box.conf[0])

            detections.append(
                {
                    "label": label,
                    "conf": confidence
                }
            )

            found_classes.add(label)

    required_elements = {
        "photo",
        "legal",
        "data"
    }

    is_authentic = required_elements.issubset(found_classes)

    if is_authentic:
        return (
            True,
            "Front side visuals verified.",
            detections,
            annotated_image
        )

    missing = required_elements - found_classes

    return (
        False,
        f"Visual markers missing: {', '.join(missing)}",
        detections,
        annotated_image
    )