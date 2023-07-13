import time
from datetime import datetime

import cv2
import numpy as np
import matplotlib.pyplot as plt


import camera
import image


class Detector:
    def __init__(self, webcam: camera.Camera):
        self.camera = webcam

        self.__alr_in_motion = False
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
        gray_img = img.color_to_gray()
        # contrasted_img = gray_img.format_contrast()
        denoised_img = gray_img.denoise(k=1, s=1)
        clean_img = denoised_img.clean_white_noise(radius=1)
        return clean_img

    def __image_subtraction(self, img1, img2):
        subtraction = cv2.absdiff(img1, img2)
        subtracted_img = image.Image(subtraction)
        return subtracted_img

    def __image_similarity(self, img1, img2):
        subtracted_img = self.__image_subtraction(img1, img2)
        normalised_img = subtracted_img.normalise()
        img_similarity = round(100 - (np.mean(normalised_img) * 100), 2)
        current_time = datetime.now().strftime("%H%M%S.%f")[:-3]
        cv2.imwrite(f"pics/sub_{current_time}_{img_similarity}.jpeg",
                    subtracted_img.get_image())
        return img_similarity

    def get_transformed_frame(
        self
    ):
        raw_image = self.camera.read_frame(saving=self.__alr_in_motion)
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
        self.__alr_in_motion = False
        motion_end_time = datetime.now().strftime("%Y-%m-%d %H-%M")
        motion_period = (self.__motion_start_time, motion_end_time)
        self.__motion_time_store.append(motion_period)
        file_name = f"{self.__motion_start_time}-{motion_end_time}.jpeg"
        self.__motion_start_time = None
        cv2.imwrite(file_name, self.__motion_frame)
        self.camera.end_record_mp4()

    # false, false
    def no_motion_detected(self, raw_frame, score):
        pass

    # false, true
    def start_new_motion(self, raw_frame, score):
        self.__alr_in_motion = True
        self.__motion_start_time = datetime.now().strftime("%Y-%m-%d %H-%M")
        self.__motion_percent = score
        self.__motion_frame = raw_frame
        self.camera.start_record_mp4(f'{self.__motion_start_time}')

    def detect(self, time_min=10080):  # 1 week
        self.initialise()
        raw_prev_frame, transformed_prev_frame = self.__base_frame
        idx = 0
        end_time = time.time() + 60 * time_min
        while time.time() < end_time:
            time.sleep(0.1)
            raw_frame, transformed_frame = self.get_transformed_frame()
            similarity_score = self.__image_similarity(transformed_prev_frame,
                                                       transformed_frame)
            
            new_movement_detected = similarity_score < 90
            print(idx, (self.__alr_in_motion, new_movement_detected), similarity_score)
            motion_update_fn = self.motion_logic[
                (self.__alr_in_motion, new_movement_detected)
            ]
            motion_update_fn(raw_frame, similarity_score)
            raw_prev_frame, transformed_prev_frame = raw_frame, transformed_frame
            idx += 1

    def get_motion_detected_count(self):
        return len(self.__motion_time_store)
