import cv2
import numpy as np


def clean_bgr2gray(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise from image
    smooth_img = cv2.GaussianBlur(gray_img,(5,5),0)

    # Apply Erode and Dilate operation
    kernel = np.ones((3, 3), np.uint8)
    eroded_img = cv2.erode(smooth_img, kernel)
    cleaned_img = cv2.dilate(eroded_img, kernel)

    return smooth_img

def contrast(img):
    eq_img = cv2.equalizeHist(img)
    return eq_img

def transform(img):
    contrast_img = contrast(img)
    clean_img = clean_bgr2gray(contrast_img)
    return clean_img

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

