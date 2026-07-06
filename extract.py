import os
import cv2
import logging

# Standard Windows stability fixes
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from paddleocr import PaddleOCR
from preprocess import preprocess

# Version 2.8.1 supports these arguments perfectly
ocr = PaddleOCR(
    use_angle_cls=True, 
    lang="en", 
    use_mkldnn=False, 
    show_log=False
)

def extract_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return ""

    processed = preprocess(image)
    
    # Perform OCR
    result = ocr.ocr(processed, cls=True)

    if not result or not result[0]:
        return ""

    # Sort and extract text
    lines = result[0]
    lines.sort(key=lambda x: x[0][0][1])

    return "\n".join([line[1][0] for line in lines])