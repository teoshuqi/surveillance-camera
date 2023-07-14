import time
from datetime import datetime

import cv2
import numpy as np

import camera
import image
import os

from dotenv import load_dotenv

load_dotenv('../.env')
IMG_DIR = os.getenv('CAPTURES_DIR')
IMG_EXT = os.getenv('IMG_EXT')
TIME_FORMAT = os.getenv('TIME_FORMAT')
SIM_THRESHOLD = os.getenv('THRESHOLD')


class Detector:
    """
    This class detects motion in real time from camera.

    Args:
        webcam: A Camera object

    Attributes:
        __camera: The camera object that the detector will use to capture
                  frames.
        __alr_in_motion: A Boolean flag that indicates whether the detector is
                         currently detecting motion.
        __motion_start_time: The time at which the detector first detected
                             motion.
        __motion_frame: The np.ndarray frame which recorded the lowest
                        similarity percentage, i.e. largest movement.
        __frame_similarity: The similarity percentage of the current frame
                          compared to the previous frame.
        __motion_time_store: A list of the (start time, end time) at which
                             the detector has detected motion.
        __base_frame: The intial frame that the detector will use to compare
                      frames against.
        __motion_logic: The dictionary which stores the functions that for
                        the different scenarios in detecting motion.
"""
    def __init__(self, webcam: camera.Camera) -> None:
        self.__camera = webcam

        self.__alr_in_motion = False
        self.__motion_start_time = None
        self.__motion_frame = None
        self.__frame_similarity = 100
        self.__motion_time_store = []
        self.__base_frame = None

        self.__motion_logic = {
            (True, True): self.update_greatest_movement_in_motion,
            (True, False): self.stop_current_motion,
            (False, True): self.start_new_motion,
            (False, False): self.no_motion_detected,
        }

    def __image_transform(self, img: image.Image) -> image.Image:
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

    def __image_subtraction(self,
                            img1: image.Image,
                            img2: image.Image) -> image.Image:
        """
        Subtracts two images to get diffence of images.

        Args:
            img1: The first image to be subtracted.
            img2: The second image to be subtracted.

        Returns:
            The subtracted image.
        """

        subtraction = cv2.absdiff(img1.get_image(), img2.get_image())
        subtracted_img = image.Image(subtraction)
        return subtracted_img

    def __image_similarity(self,
                           img1: image.Image,
                           img2: image.Image) -> float:
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

    def get_transformed_frame(self) -> tuple(np.ndarray, np.ndarray):
        """
        Gets the camera frame after image transformation.

        Returns:
            The transformed frame.

        """
        raw_image = self.__camera.read_frame(saving=self.__alr_in_motion)
        raw_frame = raw_image.get_image()
        transformed_image = self.__image_transform(raw_image)
        final_frame = transformed_image.get_image()
        return raw_frame, final_frame

    def initialise(self) -> None:
        """
        Initialize the detector.

        """
        self.__base_frame = self.get_transformed_frame()

    # (in motion, new motion) true , true
    def update_greatest_movement_in_motion(self,
                                           raw_frame: np.ndarray,
                                           score: float = 100.0) -> None:
        """
        When camera detects motion, updates and stores the greatest movement.

        Args:
            raw_frame: The frame to be updated.
            score: The similarity score.

        """
        if self.__frame_similarity < score:
            self.__motion_frame = raw_frame

    # true, false
    def stop_current_motion(self,
                            raw_frame: np.ndarray,
                            score: float = 100.0) -> None:
        """
        Stops the current motion and stores frame with highest movement
        during motion.

        Args:
            raw_frame: The frame to be updated.
            score: The similarity score.

        """
        self.__alr_in_motion = False
        motion_end_time = datetime.now().strftime(TIME_FORMAT)
        motion_period = (self.__motion_start_time, motion_end_time)
        self.__motion_time_store.append(motion_period)
        print(f"Motion Detected from {self.__motion_start_time} \
              to {motion_end_time}")
        file_name = f"{IMG_DIR}/{self.__motion_start_time}-{motion_end_time}\
            .{IMG_EXT}"
        cv2.imwrite(file_name, self.__motion_frame)
        self.__camera.end_record_mp4()
        self.__motion_start_time = None

    # false, false
    def no_motion_detected(self,
                           raw_frame: np.ndarray,
                           score: float = 100.0) -> None:
        pass

    # false, true
    def start_new_motion(self,
                         raw_frame: np.ndarray,
                         score: float = 100.0) -> None:
        """
        Starts to record when new motion detected.

        Args:
            raw_frame: The frame to be updated.
            score: The similarity score.

        """

        self.__alr_in_motion = True
        self.__motion_start_time = datetime.now().strftime(TIME_FORMAT)
        self.__frame_similarity = score
        self.__motion_frame = raw_frame
        self.__camera.start_record_mp4(f"{self.__motion_start_time}")

    def detect_motion(self, time_min: int = 10080) -> None:
        """
        Continuously look for new frames, detect and stores motion using camera

        Args:
            time_min: Motion detection time period in minutes. Default 1 week.

        """
        self.initialise()
        _, transformed_prev_frame = self.__base_frame
        idx = 0
        end_time = time.time() + 60 * time_min
        while time.time() < end_time:
            time.sleep(0.1)
            raw_frame, transformed_frame = self.get_transformed_frame()
            similarity_score = self.__image_similarity(
                transformed_prev_frame, transformed_frame
            )

            new_movement_detected = similarity_score < SIM_THRESHOLD
            motion_update_fn = self.__motion_logic[
                (self.__alr_in_motion, new_movement_detected)
            ]
            motion_update_fn(raw_frame, similarity_score)
            _, transformed_prev_frame = raw_frame, transformed_frame
            idx += 1

    def get_motion_detected_count(self) -> int:
        """
        Count number of motion detected

        Returns:
                    Number of motion detected
        """
        print(self.__motion_time_store)
        return len(self.__motion_time_store)
