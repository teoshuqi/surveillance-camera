# importing the libraries
import camera
import scripts.motion as motion

# Setup camera
webcam = camera.Camera(0)
webcam.start(10, (400, 600))

# motion detector
motion_detector = motion.Detector(webcam)

motion_detector.detect(0.1)

webcam.end()
