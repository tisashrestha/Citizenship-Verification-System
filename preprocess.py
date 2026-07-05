import cv2

def preprocess(image):
    # PaddleOCR performs best on slightly denoised grayscale or even BGR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Denoise to remove background texture
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    return denoised