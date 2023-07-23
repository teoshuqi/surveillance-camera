import os

import numpy as np
import pytest
from dotenv import load_dotenv

from app.image import Image
from app.motion import Detector

load_dotenv()
# video
CODEC = os.getenv("CODEC")
VID_FORMAT = os.getenv("VID_FORMAT")

# camera
FPS = int(os.getenv("FPS"))
WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))

# motion detector
SIM_THRESHOLD = float(os.getenv("THRESHOLD"))


@pytest.fixture
def create_sample_image():
    # Create a sample image for testing,
    image_data = np.random.randint(
        low=0, high=255, size=(HEIGHT, WIDTH, 3), dtype=np.uint8
    )
    return Image(image_data)


def test_image_transform(create_sample_image):
    # Test the __image_transform method of Detector class
    detector = Detector()
    img = create_sample_image

    transformed_img = detector._Detector__image_transform(img)

    # Assertions
    assert isinstance(transformed_img, Image)


def test_image_subtraction(create_sample_image):
    # Test the __image_subtraction method of Detector class
    detector = Detector()
    img1 = create_sample_image
    img2 = create_sample_image

    subtracted_img = detector._Detector__image_subtraction(img1, img2)

    # Assertions
    assert isinstance(subtracted_img, Image)


def test_image_similarity(create_sample_image):
    # Test the __image_similarity method of Detector class
    detector = Detector()
    img1 = create_sample_image
    img2 = create_sample_image

    similarity_score = detector._Detector__image_similarity(img1, img2)

    # Assertions
    assert isinstance(similarity_score, float)
    assert 0 <= similarity_score <= 100


def test_detect_motion(create_sample_image):
    # Test the detect_motion method of Detector class
    detector = Detector()
    prev_frame = create_sample_image
    current_frame = create_sample_image

    has_movement, similarity_score = detector.detect_motion(
        prev_frame, current_frame, SIM_THRESHOLD
    )

    # Assertions
    assert isinstance(has_movement, bool)
    assert isinstance(similarity_score, float)
    assert 0 <= similarity_score <= 100


if __name__ == "__main__":
    pytest.main()
