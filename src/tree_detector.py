import cv2

LOWER_G_HSV = (25, 25, 25)
UPPER_G_HSV = (70, 255, 255)

def get_tree_mask(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_image, LOWER_G_HSV, UPPER_G_HSV)
    return cv2.bitwise_not(mask)
