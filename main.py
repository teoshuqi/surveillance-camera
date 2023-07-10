# importing the libraries
import cv2
import numpy as np
from datetime import datetime
import image

# Setup camera
cap = cv2.VideoCapture(0)


# initial image
ret, init_frame = cap.read()
init_img = image.transform(init_frame)
prev_transformed_frame = init_img

# initialise params
param_store = {
    'motion_detected':False,
    'motion_frame':init_frame,
    'motion_percent':0,
    'motion_start_time': datetime.now().strftime("%Y-%m-%d %H:%M")
}

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # converting image from color to grayscale
    incoming_transformed_frame = image.transform(frame)

    # detecting motion
    diff_percent = image.detect_difference(prev_transformed_frame, incoming_transformed_frame)
    new_motion_detected = diff_percent > 5
    alr_in_motion = param_store['motion_detected']

    if new_motion_detected & alr_in_motion:
        if param_store['motion_percent'] < diff_percent:
            param_store['motion_frame'] = frame
            param_store['motion_percent'] = diff_percent
    elif (not new_motion_detected) & alr_in_motion:
        motion_end_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        motion_start_time = param_store['motion_start_time']
        motion_frame = param_store['motion_frame']
        file_name = f'{motion_start_time}'
        cv2.imwrite('color_img.jpg', motion_frame)
    elif (new_motion_detected) & (not alr_in_motion):
        param_store['motion_start_time'] = datetime.now()
        param_store['motion_frame'] = frame
        param_store['motion_percent'] = diff_percent
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
