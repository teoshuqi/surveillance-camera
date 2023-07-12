import numpy as np
from skimage import exposure, filters
from skimage.color import rgb2gray
from skimage.morphology import square, dilation, erosion


class Image:
    def __init__(self, img: np.ndarray):
        self.__img = img

    def color_to_gray(self):
        gray = rgb2gray(self.__img)
        gray_img = Image(gray)
        return gray_img

    def denoise(self, sigma=10, truncate=2):
        denoised = filters.gaussian(self.__img, sigma=sigma, truncate=truncate)
        denoised_img = Image(denoised)
        return denoised_img

    def clean_white_noise(self, radius=2):
        kernel = square(radius)
        eroded = erosion(self.__img, kernel)
        dilated = dilation(eroded, kernel)
        dilated_img = Image(dilated)
        return dilated_img

    def format_contrast(self):
        contrasted = exposure.equalize_hist(self.__img)
        contrasted_img = Image(contrasted)
        return contrasted_img

    def normalise(self):
        normalised = self.__img / 255
        return normalised

    def get_image(self):
        return self.__img
