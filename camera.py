import cv2

import image


class Camera:
    def __init__(self, camid):
        self.id = camid
        self.cap = None
        self.__frame_size = (None, None)
        self.__fps = None
        self.__record_file = None

    def __set_frame_size(self, height, width):
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__frame_size = (height, width)

    def __set_fps(self, fps):
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.__fps = fps

    def get_frame_size(self):
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.__frame_size = (height, width)
        return self.__frame_size

    def get_fps(self):
        self.__fps = self.cap.get(cv2.CAP_PROP_FPS)
        return self.__fps

    def start(self, fps, frame_size):
        self.cap = cv2.VideoCapture(self.id)

        if not self.cap.isOpened():
            print(f"Cannot open camera {self.id}.")
        else:
            print("Camera started. Setting frame size and fps.")
            self.__set_frame_size(*frame_size)
            self.__set_fps(fps)

    def end(self):
        if self.cap:
            self.cap.release()
            print("Camera closed.")
        else:
            print(f"Camera {self.id} not opened")
        cv2.destroyAllWindows()

    def start_record_mp4(self, name="video.mp4"):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.__record_file = cv2.VideoWriter(
            name, fourcc, self.__fps, self.__frame_size
        )

    def end_record_mp4(self):
        self.__record_file.release()
        self.__record_file = None

    def read_frame(self, saving=False):
        ret, frame = self.cap.read()
        if not ret:
            print(f"Can't receive frame from {self.id}. Exiting ...")
            return None
        has_record_started = self.__record_file is not None
        if saving & has_record_started:
            self.__record_file.write(frame)
        return image.Image(frame)
