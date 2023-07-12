import time
from datetime import datetime

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error

import camera
import image


class Detector:
    def __init__(self, webcam: camera.Camera):
        self.camera = webcam

        self.__in_motion = False
        self.__motion_start_time = None
        self.__motion_frame = None
        self.__motion_percent = 0
        self.__motion_time_store = []
        self.__base_frame = None

        self.motion_logic = {
            (True, True): self.update_greatest_movement_in_motion,
            (True, False): self.stop_current_motion,
            (False, True): self.start_new_motion,
            (False, False): self.no_motion_detected,
        }

    def __image_transform(self, img):
        gray_img = img #img.color_to_gray()
        # contrasted_img = gray_img.format_contrast()
        # denoised_img = contrasted_img.denoise()
        # clean_img = denoised_img.clean_white_noise()
        return gray_img

    def __image_subtraction(self, img1, img2):
        subtraction = (img1 - img2) % 256
        subtracted_img = image.Image(subtraction)
        return subtracted_img

    def __image_similarity(self, img1, img2):
        subtracted_img = self.__image_subtraction(img1, img2)
        normalised_img = subtracted_img.normalise()
        img_similarity = round(100 - np.mean(normalised_img) * 100, 2)
        return img_similarity

    def get_transformed_frame(
        self,
    ):
        raw_image = self.camera.read_frame()
        raw_frame = raw_image.get_image()
        transformed_image = self.__image_transform(raw_image)
        final_frame = transformed_image.get_image()
        return raw_frame, final_frame

    def initialise(self):
        self.__base_frame = self.get_transformed_frame()

    # (in motion, new motion) true , true
    def update_greatest_movement_in_motion(self, raw_frame, score):
        if self.__motion_percent < score:
            self.__motion_frame = raw_frame

    # true, false
    def stop_current_motion(self, raw_frame, score):
        self.__in_motion = False
        motion_end_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        motion_period = (self.__motion_start_time, motion_end_time)
        self.__motion_time_store.append(motion_period)
        self.__motion_start_time = None
        file_name = f"{self.__motion_start_time}-{motion_end_time}"
        cv2.imwrite(file_name, self.__motion_frame)

    # false, false
    def no_motion_detected(self, raw_frame, score):
        pass

    # false, true
    def start_new_motion(self, raw_frame, score):
        self.__in_motion = False
        self.__motion_start_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.__motion_percent = score
        self.__motion_frame = raw_frame

    def detect(self, time_min=10080):  # 1 week
        self.initialise()
        raw_prev_frame, transformed_prev_frame = self.__base_frame

        end_time = time.time() + 60 * time_min
        while time.time() < end_time:
            raw_frame, transformed_frame = self.get_transformed_frame()
            similarity_score = self.__image_similarity(transformed_prev_frame,
                                                       transformed_frame)
            current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            cv2.imwrite(f"pics/{current_time}_raw.jpeg", raw_frame)
            cv2.imwrite(f"pics/{current_time}_transform_{similarity_score}.jpeg", transformed_frame)
            new_movement_detected = similarity_score < 95
            already_in_motion = self.__in_motion
            print((already_in_motion, new_movement_detected), similarity_score)
            motion_update_fn = self.motion_logic[
                (already_in_motion, new_movement_detected)
            ]
            motion_update_fn(raw_frame, similarity_score)

    def get_motion_detected_count(self):
        return len(self.__motion_time_store)
