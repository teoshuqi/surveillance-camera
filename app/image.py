from __future__ import annotations

import cv2
import numpy as np


class Image:

    """
    A class to represent an image.

    Args:
        img (np.ndarray): The image data.

    Attributes:
        __img: The image in ndarray
    """

    def __init__(self, img: np.ndarray) -> None:
        self.__img = img

    def color_to_gray(self) -> Image:
        """
        Convert the image to grayscale.

        Returns:
            The grayscale image.

        """
        gray = cv2.cvtColor(self.__img, cv2.COLOR_BGR2GRAY)
        gray_img = Image(gray)
        return gray_img

    def denoise(self, k: int = 11, s: int = 3) -> Image:
        """
        Denoise the image using Gaussian blur.

        Args:
            k (int, optional): The kernel size. Defaults to 11.
            s (int, optional): The sigma value. Defaults to 3.

        Returns:
            The denoised image.

        """
        denoised = cv2.GaussianBlur(self.__img, ksize=(k, k), sigmaX=s)
        denoised_img = Image(denoised)
        return denoised_img

    def clean_white_noise(self, radius: int = 10) -> Image:
        """
        Clean white noise from the image using erosion and dilation.

        Args:
            radius (int, optional): The kernel radius. Defaults to 10.

        Returns:
            The cleaned image.

        """
        kernel = np.ones((radius, radius), np.uint8)
        eroded = cv2.erode(self.__img, kernel)
        dilated = cv2.dilate(eroded, kernel)
        dilated_img = Image(dilated)
        return dilated_img

    def format_contrast(self) -> Image:
        """
        Format the contrast of the image using histogram equalization.

        Returns:
            The image with formatted contrast.

        """
        contrasted = cv2.equalizeHist(self.__img)
        contrasted_img = Image(contrasted)
        return contrasted_img

    def normalise(self) -> np.ndarray:
        """
        Normalize the image to the range [0, 1].

        Returns:
            The normalized image.

        """
        normalised = self.__img / 255
        return normalised

    def get_image(self) -> np.ndarray:
        """
        Get the image data.

        Returns:
            The image data.

        """
        return self.__img
