import cv2
import numpy as np

def zerkalo(path):
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    image = cv2.flip(image, 1)
    return image
def BlackWhite(path):
    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_image = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)
    return binary_image