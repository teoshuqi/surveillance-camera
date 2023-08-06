import cv2
from app.image import Image
import numpy as np
from typing import Tuple


class Detector:
    """
    This class detects motion in real time from camera.

    """

    def __init__(self) -> None:
        pass

    def __image_transform(self, img: Image) -> Image:
        """
        Transforms the image by reducinf sharpness and noise.

        Args:
            img: The image to be transformed.

        Returns:
            The transformed image.

        """
        gray_img = img.color_to_gray()
        contrasted_img = gray_img.format_contrast()
        denoised_img = contrasted_img.denoise(k=1, s=1)
        clean_img = denoised_img.clean_white_noise(radius=1)
        return clean_img

    def __image_subtraction(self, img1: Image, img2: Image) -> Image:
        """
        Subtracts two images to get diffence of images.

        Args:
            img1: The first image to be subtracted.
            img2: The second image to be subtracted.

        Returns:
            The subtracted image.
        """

        subtraction = cv2.absdiff(img1.get_image(), img2.get_image())
        subtracted_img = Image(subtraction)
        return subtracted_img

    def __image_similarity(self, img1: Image, img2: Image) -> float:
        """
        Calculates the similarity score between two images.

        Args:
            img1: The first image.
            img2: The second image.

        Returns:
            The similarity score between the two images.

        """
        subtracted_img = self.__image_subtraction(img1, img2)
        normalised_img = subtracted_img.normalise()
        img_similarity = round(100 - (np.mean(normalised_img) * 100), 2)
        return img_similarity

    def detect_motion(self, prev_frame, current_frame, threshold) -> Tuple[bool, float]:
        """
        Detect motion using previous and current camera frames

        Args:
            prev_frame: Previous camera frame
            current_frame: Current camera frame

        """
        transformed_prev_frame = self.__image_transform(prev_frame)
        transformed_current_frame = self.__image_transform(current_frame)
        similarity_score = self.__image_similarity(
            transformed_prev_frame, transformed_current_frame
        )

        has_movement = bool(similarity_score < threshold)
        return has_movement, similarity_score
