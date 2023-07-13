import numpy as np
import cv2
from skimage import exposure, filters
from skimage.color import rgb2gray
from skimage.morphology import square, dilation, erosion


class Image:
    def __init__(self, img: np.ndarray):
        self.__img = img

    def color_to_gray(self):
        gray = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
        gray_img = Image(gray)
        return gray_img

    def denoise(self, k=10, s=2):
        denoised = cv2.GaussianBlur(self.__img,
                                    ksize=(k, k),
                                    sigmaX=s,
                                    sigmaY=s)
        denoised_img = Image(denoised)
        return denoised_img

    def clean_white_noise(self, radius=10):
        kernel = np.ones((radius, radius), np.uint8)
        eroded = cv2.erode(self.__img, kernel)
        dilated = cv2.dilate(eroded, kernel)
        dilated_img = Image(dilated)
        return dilated_img

    def format_contrast(self):
        contrasted = cv2.equalizeHist(self.__img)
        contrasted_img = Image(contrasted)
        return contrasted_img

    def normalise(self):
        normalised = self.__img / 255
        return normalised

    def get_image(self):
        return self.__img
