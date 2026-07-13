import os
import cv2

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from paddleocr import PaddleOCR
from preprocess import preprocess

ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en",
    use_gpu=False
)


def extract_text(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return ""

    processed = preprocess(image)

    if len(processed.shape) == 2:
        processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2BGR)

    result = ocr.ocr(processed, cls=True)

    if not result or not result[0]:
        return ""

    texts = []

    for line in result[0]:
        texts.append(line[1][0])

    return "\n".join(texts)