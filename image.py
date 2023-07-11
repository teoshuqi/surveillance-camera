import numpy as np
from skimage import exposure
from skimage.color import rgb2gray
from skimage import filters
from skimage.morphology import ball, erosion, dilation
from skimage.metrics import structural_similarity as ssim

class Image:
    def __init__(self, img):
        self.img = img

    def denoise(self):
        self.img = filters.gaussian(self.img, sigma=10, truncate=1/5)
    
    def clean_white_noise(self):
        self.img = erosion(self.img, ball(5))
        self.img = dilation(self.img, ball(5))

    def format_contrast(self):
        self.img = exposure.equalize_hist(self.img)
    


def subtraction(img1, img2):
    image_subtraction = (img1 - img2) % 256
    return image_subtraction

def normalise(img):
    normalised_img = img/255
    return normalised_img

def detect_difference(img1, img2):
    diff_img = subtraction(img1, img2)
    normalised_img = normalise(diff_img)
    img_diff_percent = np.mean(normalised_img)*100
    return img_diff_percent

