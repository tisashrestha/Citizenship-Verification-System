import cv2

def preprocess(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(
        gray,None,10,7,21
    )

    return cv2.cvtColor(
        denoised,cv2.COLOR_GRAY2BGR
    )