import os
import cv2
from ultralytics import YOLO

model_path = "weights/bestt.pt"

def validate_front_side(image_path, confidence_threshold=0.75):
    if not os.path.exists(model_path):
        return False, "YOLO Model weights (bestt.pt) not found.", [], None

    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=confidence_threshold, save=False)

    detections = []
    found_classes = set()
    annotated_image = None

    for result in results:
        annotated_image = result.plot()  
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            detections.append({"label": label, "conf": conf})
            found_classes.add(label)

    required_elements = {'photo', 'legal', 'data'}
    is_authentic = required_elements.issubset(found_classes)

    if is_authentic:
        return True, "Front side visuals verified.", detections, annotated_image
    else:
        missing = required_elements - found_classes
        return False, f"Visual markers missing: {', '.join(missing)}", detections, annotated_image