import cv2
import numpy as np

def get_laplacian_blur(img)->float:
    if type(img) is str:
        img = cv2.imread(img)
    assert type(img) is np.ndarray
    return cv2.Laplacian(img, cv2.CV_64F).var()
