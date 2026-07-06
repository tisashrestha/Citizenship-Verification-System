from ultralytics import YOLO
import os

# Update this path to where your file actually is
model_path = "weights/best.pt" 

if os.path.exists(model_path):
    try:
        model = YOLO(model_path)
        print("✅ Success! Model loaded correctly.")
        print("Detected Classes:", model.names) 
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print(f"❌ File not found at {model_path}. Check your folder structure!")