import cv2
import numpy as np

cam = cv2.VideoCapture(1)
img = cam.read()

#img = cv2.imread("aa.png")

hsv = cv2.cvtColor(img[1], cv2.COLOR_BGR2HSV)

#purple
#lower_range = np.array([40, 70, 70])
#upper_range = np.array([180,255,255])

#grey
#lower_range = np.array([110,50,50])
#upper_range = np.array([130,255,255])

#orange
#lower_range = np.array([10,100,20])
#upper_range = np.array([25,255,255])

#yellow
#lower_range = np.array([20,100,100])
#upper_range = np.array([30,255,255])

mask = cv2.inRange(hsv, lower_range, upper_range)

cv2.imshow("Image", img[1])
cv2.imshow("Mask", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()