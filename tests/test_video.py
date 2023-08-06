import os

import pytest
from dotenv import load_dotenv

from app.camera import Camera
from app.motion import Detector
from app.video import Streaming

# Load environment variables from .env file
load_dotenv()

# Environment variables for testing
VID_DIR = os.getenv("VID_DIR")
TIME_FORMAT = os.getenv("TIME_FORMAT")
STREAM_TIME_MINS = float(os.getenv("STREAM_TIME_MINS"))

FPS = int(os.getenv("FPS"))
WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))
N_FRAMES = int(os.getenv("N_FRAMES"))
SIM_THRESHOLD = float(os.getenv("THRESHOLD"))


@pytest.fixture
def camera_object():
    # Create a Camera instance for testing
    camera_obj = Camera()
    yield camera_obj
    camera_obj.end()


@pytest.fixture
def motion_detector_object():
    # Create a Motion Detector instance for testing
    motion_detector_obj = Detector()
    yield motion_detector_obj


def test_streaming_functionality(camera_object, motion_detector_object):
    # Test the overall functionality of the Streaming class
    stream = Streaming(camera_object, motion_detector_object)

    # Ensure the video streaming works without errors
    stream_gen = stream.start()
    for _ in range(int(STREAM_TIME_MINS * FPS) - 10):
        frame_bytes = next(stream_gen)
        assert isinstance(frame_bytes, bytes)


if __name__ == "__main__":
    pytest.main()
