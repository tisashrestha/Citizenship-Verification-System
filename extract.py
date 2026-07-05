import cv2
from paddleocr import PaddleOCR
from preprocess import preprocess

# Initialize once
ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)

def extract_text(image_path):
    # 1. Load image
    image = cv2.imread(image_path)
    if image is None:
        return ""

    # 2. Simple Preprocessing (PaddleOCR works better without aggressive thresholding)
    processed = preprocess(image)

    # 3. OCR (cls=True handles 90/180/270 degree rotations automatically)
    result = ocr.ocr(processed, cls=True)

    if not result or not result[0]:
        return ""

    # 4. Sort lines by coordinates (Top to Bottom)
    lines = result[0]
    lines.sort(key=lambda x: x[0][0][1])

    return "\n".join([line[1][0] for line in lines])