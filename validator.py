import os
from ultralytics import YOLO

# Load your trained model (make sure best.pt is in the same directory)
# If you are using YOLOv11, the ultralytics library handles it.
model_path = "weights/best.pt" 

def validate_front_side(image_path, confidence_threshold=0.5):
    """
    Validates the front side of the citizenship using YOLO.
    Returns: (is_valid, message, detections)
    """
    if not os.path.exists(model_path):
        return False, "YOLO Model weights (best.pt) not found.", []

    model = YOLO(model_path)
    results = model.predict(source=image_path, conf=confidence_threshold, save=False)
    
    detections = []
    # Adjust these names based on your 'classes.txt'
    # Example classes: ['photo', 'legal_thing', 'data']
    found_classes = set()
    
    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            conf = float(box.conf[0])
            detections.append({"label": label, "conf": conf})
            found_classes.add(label)

    # Logic: Card is valid if it has a photo AND legal markers
    # Modify the set below based on exactly what you labeled in Colab
    required_elements = {'photo', 'legal'} 
    is_authentic = required_elements.issubset(found_classes)

    if is_authentic:
        return True, "Front side visual markers verified.", detections
    else:
        missing = required_elements - found_classes
        return False, f"Visual markers missing: {', '.join(missing)}", detections