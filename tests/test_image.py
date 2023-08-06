import os

import numpy as np
import pytest
from dotenv import load_dotenv

from app.image import Image

load_dotenv()

# camera
WIDTH = int(os.getenv("WIDTH"))
HEIGHT = int(os.getenv("HEIGHT"))

rgb_image_data = np.random.randint(
    low=0, high=255, size=(HEIGHT, WIDTH, 3), dtype=np.uint8
)
gray_image_data = np.random.randint(
    low=0, high=255, size=(HEIGHT, WIDTH, 1), dtype=np.uint8
)


@pytest.fixture
def rgb_image_object():
    # Create an Image instance using the sample image data before each test
    img = Image(rgb_image_data)
    yield img


@pytest.fixture
def gray_image_object():
    # Create an Image instance using the sample image data before each test
    gray_img = Image(gray_image_data)
    yield gray_img


def test_color_to_gray(rgb_image_object):
    # Test converting the image to grayscale
    gray_img = rgb_image_object.color_to_gray()
    assert isinstance(gray_img, Image)
    assert (
        len(gray_img.get_image().shape) == 2
    )  # Grayscale images should have 2 dimensions


def test_denoise(rgb_image_object):
    # Test denoising the image
    denoised_img = rgb_image_object.denoise()
    assert isinstance(denoised_img, Image)


def test_clean_white_noise(rgb_image_object):
    # Test cleaning white noise from the image
    cleaned_img = rgb_image_object.clean_white_noise()
    assert isinstance(cleaned_img, Image)


def test_format_contrast(gray_image_object):
    # Test formatting the contrast of the image
    contrasted_img = gray_image_object.format_contrast()
    assert isinstance(contrasted_img, Image)


def test_normalise(rgb_image_object):
    # Test normalizing the image
    normalized_img = rgb_image_object.normalise()
    assert isinstance(normalized_img, np.ndarray)
    assert normalized_img.min() >= 0 and normalized_img.max() <= 1


def test_get_image(rgb_image_object):
    # Test getting the image data
    img_data = rgb_image_object.get_image()
    assert isinstance(img_data, np.ndarray)
    assert img_data.shape == (HEIGHT, WIDTH, 3)
    assert np.array_equal(img_data, rgb_image_data)


if __name__ == "__main__":
    pytest.main()
