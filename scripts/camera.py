import cv2

import image


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

    def __set_frame_size(self, height: int = 480, width: int = 640) -> None:
        """
        Sets the frame size of the camera.

        Args:
            height (int, optional): The height of the frame. Defaults to 480.
            width (int, optional): The width of the frame. Defaults to 640.

        """
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__frame_size = (height, width)

    def __set_fps(self, fps: int = 20) -> None:
        """
        Gets the fps of the camera.

        Returns:
            The fps of the camera.

        """

        self.__cap.set(cv2.CAP_PROP_FPS, fps)
        self.__fps = fps

    def get_frame_size(self) -> int:
        height = self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.__frame_size = (height, width)
        return self.__frame_size

    def get_fps(self) -> int:
        self.__fps = self.__cap.get(cv2.CAP_PROP_FPS)
        return self.__fps

    def start(self, fps: int = 20, frame_size: tuple = (480, 640)) -> None:
        """
        Start the camera.

        Args:
            fps (int, optional): The fps of the camera. Defaults to 20.
            frame_size (tuple, optional): The frame size of the camera.
                                          Defaults to (480, 640).

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

    def start_record_mp4(self, name: int = "video.mp4") -> None:
        """
        Start recording the camera to a mp4 file.

        Args:
            name (int, optional): The name of the mp4 file.
                                  Defaults to "video.mp4".

        """
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.__record_file = cv2.VideoWriter(
            name, fourcc, self.__fps, self.__frame_size
        )

    def end_record_mp4(self) -> None:
        """
        End recording the camera to a mp4 file.

        """
        self.__record_file.release()
        self.__record_file = None

    def read_frame(self, saving: bool = False) -> image.Image:
        """
        Read a frame from the camera.

        Args:
            saving (bool, optional): Whether to save the frame to a file.
            Defaults to False.

        Returns:
            The image frame.

        """
        ret, frame = self.__cap.read()
        if not ret:
            print(f"Can't receive frame from {self.__id}. Exiting ...")
            return None
        has_record_started = self.__record_file is not None
        if saving & has_record_started:
            self.__record_file.write(frame)
        return image.Image(frame)
