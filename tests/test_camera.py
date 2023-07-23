import os

import numpy as np
import pytest
from dotenv import load_dotenv

from app.camera import Camera

load_dotenv()
# video
VID_DIR = os.getenv("VID_DIR")
CODEC = os.getenv("CODEC")
VID_FORMAT = os.getenv("VID_FORMAT")

# camera
FPS = int(os.getenv("FPS"))
WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))


@pytest.fixture
def camera():
    # Create a camera instance before each test
    cam = Camera(camid=0)
    yield cam
    # Release the camera and clean up after each test
    cam.end()


def test_start_and_end(camera):
    # Check if the camera starts and ends properly
    camera.start()
    assert camera.get_frame_size() == (WIDTH, HEIGHT)
    assert camera.get_fps() == FPS
    camera.end()


def test_read_frame(camera):
    camera.start()
    frame = camera.read_frame()
    print(type(frame))
    assert isinstance(frame, np.ndarray)
    camera.end()


def test_record_video(camera):
    camera.start()
    test_filepath = f"{VID_DIR}/test_video.{VID_FORMAT}"
    camera.start_record_video(name=test_filepath)
    for _ in range(10):
        frame = camera.read_frame()
        camera.record_frame(frame)
    camera.end_record_video()
    camera.end()
    assert os.path.exists(test_filepath), f"Video file '{test_filepath}' not found."
    assert test_filepath.endswith(
        VID_FORMAT
    ), f"'{test_filepath}' is not a valid video file."


if __name__ == "__main__":
    pytest.main()
