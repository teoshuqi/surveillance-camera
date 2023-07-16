import os
from typing import Tuple

import cv2
from dotenv import load_dotenv

import scripts.image as image

load_dotenv(".env")
# video
IMG_DIR = os.getenv("VID_DIR")
TIME_FORMAT = os.getenv("TIME_FORMAT")
STREAM_TIME_MINS = os.getenv("STREAM_TIME_MINS")
CODEC = os.getenv("CODEC")
VID_FORMAT = os.getenv("VID_FORMAT")

# camera
FPS = os.getenv("FPS")
WIDTH = os.getenv("WIDTH")
HEIGHT = os.getenv("HEIGHT")

# motion detector
N_FRAMES = os.getenv("N_FRAMES")
SIM_THRESHOLD = float(os.getenv("THRESHOLD"))


class Camera:
    """
    A class to represent a camera.

    Args:
        camid: The ID of the camera.

    Attributes:
        __id: The camera id for opencv to identify
        __cap: Store OpenCV VideoCpature object to read video capture by camera
        __frame_size: Frame Size (height, width) of camera
        __fps: Frames per Seconds of camera
        __record_file: Store OpenCV VideoWriter object to save video
    """

    def __init__(self, camid: int = 0) -> None:
        self.__id = camid
        self.__cap = None
        self.__frame_size = (None, None)
        self.__fps = None
        self.__record_file = None

    def __set_frame_size(self, width: int, height: int) -> None:
        """
        Sets the frame size of the camera.

        Args:
            height (int): The height of the frame. Defaults to 480.
            width (int): The width of the frame. Defaults to 640.

        """
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__frame_size = (height, width)

    def __set_fps(self, fps: int) -> None:
        """
        Gets the fps of the camera.

        Args:
            fps (int): The fps of the camera.

        """

        self.__cap.set(cv2.CAP_PROP_FPS, fps)
        self.__fps = fps

    def get_frame_size(self) -> Tuple[int]:
        """
        Gets the frame size (width, height) of the camera.

        Returns:
            The frame size of the camera.

        """
        height = self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.__frame_size = (int(width), int(height))  # update camera settings
        return self.__frame_size

    def get_fps(self) -> int:
        """
        Gets the fps of the camera.

        Returns:
            The fps of the camera.

        """
        fps = self.__cap.get(cv2.CAP_PROP_FPS)
        self.__fps = fps  # update camera settings
        return self.__fps

    def start(self, fps: int = FPS, frame_size: tuple = (WIDTH, HEIGHT)) -> None:
        """
        Start the camera.

        Args:
            fps (int, optional): The fps of the camera. Defaults to 20.
            frame_size (tuple, optional): The frame size of the camera.
                                          Defaults to (640, 480).

        """
        self.__cap = cv2.VideoCapture(self.__id)

        if not self.__cap.isOpened():
            print(f"Cannot open camera {self.__id}.")
        else:
            print("Camera started. Setting frame size and fps.")
            self.__set_frame_size(*frame_size)
            self.__set_fps(fps)

    def end(self) -> None:
        """
        End the camera.

        """
        if self.__cap:
            self.__cap.release()
            print("Camera closed.")
        else:
            print(f"Camera {self.__id} not opened")
        cv2.destroyAllWindows()

    def read_frame(self, current_time: str = "") -> image.Image:
        """
        Read a frame from the camera and write current datetime on screen.

        Args:
            current_time (str, optional): Current time in string format

        Returns:
            The image frame.

        """
        ret, frame = self.__cap.read()
        frame = cv2.putText(
            frame,  # put current datetime at top left of frame
            text=current_time,
            org=(10, 15),
            fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL,
            fontScale=0.8,
            color=(0, 0, 255),
        )
        if not ret:
            print(f"Can't receive frame from {self.__id}. Exiting ...")
            return None
        return frame

    def start_record_video(self, name: str = "video") -> None:
        """
        Start recording the camera to a video file.

        Args:
            name (int, optional): The name of the video file.
                                  Defaults to "video.mov".

        """
        cam_fps = self.get_fps()
        cam_size = self.get_frame_size()

        fourcc = cv2.VideoWriter_fourcc(*CODEC)
        filename = f"{name}.{VID_FORMAT}"
        self.__record_file = cv2.VideoWriter(filename, fourcc, cam_fps, cam_size, True)

    def end_record_video(self) -> None:
        """
        End recording the camera to a video file.

        """
        if self.__record_file is not None:
            print("ending record")
            self.__record_file.release()
            self.__record_file = None

    def record_frame(self, frame):
        """
        Start saving frame to recording.

        """
        if self.__record_file is not None:
            self.__record_file.write(frame)
