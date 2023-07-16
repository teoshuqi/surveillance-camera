import os
import time
from datetime import datetime
from typing import Dict

import camera
import cv2
import image
import motion
import numpy as np
from dotenv import load_dotenv

load_dotenv()
# video
IMG_DIR = os.getenv("VID_DIR")
TIME_FORMAT = os.getenv("TIME_FORMAT")
STREAM_TIME_MINS = int(os.getenv("STREAM_TIME_MINS"))

# camera
FPS = int(os.getenv("FPS"))
WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))

# motion detector
N_FRAMES = int(os.getenv("N_FRAMES"))
SIM_THRESHOLD = float(os.getenv("THRESHOLD"))


class Streaming:
    """
    Imitates a video streaming object that uses a Camera object to read frames
    and a Motion Detector object to detect motion by comparing every 10 frames.
    """

    def __init__(self, camera: camera.Camera, detector: motion.Detector) -> None:
        """Initialize the VideoStreaming object.

        Args:
            camera (Camera): The camera object for reading frames.
            motion_detector (Detector): The detector object for detecting
                                        motion.
        """
        self.__camera = camera
        self.__detector = detector

    def start(self) -> None:
        """
        Starts the video streaming process.
        """
        prev_img = self.__initialize_camera()
        start_time = time.time()
        params = {
            "frameno": 0,
            "in_motion": False,
            "is_moving": False,
            "idle_score": 100.0,
            "frame": prev_img.get_image(),
            "current_time": "",
        }

        # Streaming video for specified durations (in mins)
        while (time.time() - start_time) < STREAM_TIME_MINS * 60:
            # Get current time and frame from camera
            params["current_time"] = datetime.now().strftime(TIME_FORMAT)
            params["frame"] = self.__camera.read_frame(params["current_time"])

            # Every n frames, compare current and previous frames
            # to detect motion
            if params["frameno"] % N_FRAMES == 0:
                img = image.Image(params["frame"])
                is_moving, score = self.__detector.detect_motion(
                    prev_img, img, SIM_THRESHOLD
                )
                params["is_moving"], params["idle_score"] = is_moving, score

            # Determine if status of motion (starting, ending, no change)
            params = self.__process_motion(params)

            # Encode frame to bytes for streaming
            frame_bytes = self.__encode_frame_to_bytes(params["frame"])
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
            )

            prev_img = img
            params["frameno"] += 1

        self.__camera.end()

    def __initialize_camera(self) -> image.Image:
        """
        Initializes the camera with the desired frame rate and dimensions.
        """
        self.__camera.start(FPS, (WIDTH, HEIGHT))
        time.sleep(0.1)  # allow camera to turn on and stabilise
        first_frame = self.__camera.read_frame()
        first_img = image.Image(first_frame)
        return first_img

    def __process_motion(self, params: dict) -> Dict:
        """
        Processes the motion by recording frames or starting/stopping
        video recording.

        Args:
            params (dict): Dictionary with motion detection score,
                                  whether there is movement detected,
                                  the current time and frame etc.

        Returns:
            params (dict): Updated dictionary with new information
                                  if there is currently motion
        """
        # Movement detected and current motion continues
        if params["in_motion"] and params["is_moving"]:
            self.__camera.record_frame(params["frame"])
        # Movement detected, new motion starting
        elif not params["in_motion"] and params["is_moving"]:
            self.__start_motion_recording(params["current_time"])
            print("start", params["current_time"])
            params["in_motion"] = True
        # No movement detected, current motion ending
        elif params["in_motion"] and not params["is_moving"]:
            self.__end_motion_recording()
            print("end", params["current_time"])
            params["in_motion"] = False
        return params

    def __start_motion_recording(self, curr_time: str = datetime.now()) -> None:
        """
        Starts recording a video when motion is detected.

        Args:
            current_time_str (str): The current timestamp as a string.
        """

        filename = f"{IMG_DIR}/{curr_time}"  # video format added using env
        self.__camera.start_record_video(filename)

    def __end_motion_recording(self) -> None:
        """
        Stops recording the video when motion ends.

        """
        self.__camera.end_record_video()

    def __encode_frame_to_bytes(self, frame: np.ndarray) -> bytes:
        """
        Encodes the frame into bytes format for streaming purposes.

        Args:
            frame (Frame): The frame to encode.
        """
        ret, buffer = cv2.imencode(".jpg", frame)
        if not ret:
            print("Something is wrong with the frames or camera")
            return

        frame_bytes = buffer.tobytes()
        return frame_bytes
