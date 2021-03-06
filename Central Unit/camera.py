# Python code for Multiple Color Detection


import numpy as np
import cv2
import time
import socket


# Capturing video through webcam
webcam = cv2.VideoCapture(1)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
print("Starting...")

red_quadrant = 0
green_quadrant = 0
blue_quadrant = 0

r_difference = 0
g_difference = 0
b_difference = 0

r_prevAngle = 0
g_prevAngle = 0
b_prevAngle = 0

r_heading = 0
g_heading = 0
b_heading = 0

dif_threshold = 80

UDP_IP = "192.168.137.1"
UDP_HOSTPORT = 1337

HOSTADDR = (UDP_IP, UDP_HOSTPORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0)


def send_msg(message):
	print(message)
	sock.sendto(str(message).encode(), HOSTADDR)


def get_coords(xy):
	coords = [xy[0] / 960.0, xy[1] / 1080.0]
	return coords


def start():
	# Start a while loop
	while True:

		# Reading the video from the
		# webcam in image frames
		_, imageFrame = webcam.read()

		# Convert the imageFrame in
		# BGR(RGB color space) to
		# HSV(hue-saturation-value)
		# color space
		hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

		# Set range for red color and
		# define mask
		red_lower = np.array([136, 87, 111], np.uint8)
		red_upper = np.array([180, 255, 255], np.uint8)
		red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

		# Set range for green color and
		# define mask
		green_lower = np.array([25, 150, 72], np.uint8)
		green_upper = np.array([100, 255, 170], np.uint8)
		green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

		# Set range for blue color and
		# define mask
		blue_lower = np.array([4, 175, 218], np.uint8)
		blue_upper = np.array([130, 255, 255], np.uint8)
		blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

		# Morphological Transform, Dilation
		# for each color and bitwise_and operator
		# between imageFrame and mask determines
		# to detect only that particular color
		kernal = np.ones((5, 5), "uint8")

		# For red color
		red_mask = cv2.dilate(red_mask, kernal)
		res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

		# For green color
		green_mask = cv2.dilate(green_mask, kernal)
		res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)

		# For blue color
		blue_mask = cv2.dilate(blue_mask, kernal)
		res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

		# Creating contour to track red color
		contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 1000:
				x, y, w, h = cv2.boundingRect(contour)
				M = cv2.moments(contour)
				rotatedRect = cv2.minAreaRect(contour)

				(rcx, rcy), (width, height), r_angle = rotatedRect

				rcx = int(M['m10']/M['m00'])
				rcy = int(M['m01']/M['m00'])

				imageFrame = cv2.rectangle(imageFrame, (x, y),
										(x + w, y + h),
										(0, 0, 255), 2)

				cv2.putText(imageFrame, "Red Colour", (x, y),
							cv2.FONT_HERSHEY_SIMPLEX,
							1.0, (0, 0, 255))

				send_msg(f"pos#red#{get_coords([rcx,rcy])}")

		# Creating contour to track green color
		contours, hierarchy = cv2.findContours(green_mask,
											cv2.RETR_TREE,
											cv2.CHAIN_APPROX_SIMPLE)

		# print(contours)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 1000:
				x, y, w, h = cv2.boundingRect(contour)
				rotatedRect = cv2.minAreaRect(contour)

				(gcx, gcy), (width, height), g_angle = rotatedRect

				M = cv2.moments(contour)
				gcx = int(M['m10']/M['m00'])
				gcy = int(M['m01']/M['m00'])

				imageFrame = cv2.rectangle(imageFrame, (x, y),
										(x + w, y + h),
										(0, 255, 0), 2)

				cv2.putText(imageFrame, "Green Colour", (x, y),
							cv2.FONT_HERSHEY_SIMPLEX,
							1.0, (0, 255, 0))

				send_msg(f"pos#green#{get_coords([gcx,gcy])}")

		# Creating contour to track blue color
		contours, hierarchy = cv2.findContours(blue_mask,
											cv2.RETR_TREE,
											cv2.CHAIN_APPROX_SIMPLE)
		for pic, contour in enumerate(contours):
			area = cv2.contourArea(contour)
			if area > 1000:
				x, y, w, h = cv2.boundingRect(contour)
				M = cv2.moments(contour)
				bcx = int(M['m10']/M['m00'])
				bcy = int(M['m01']/M['m00'])

				rotatedRect = cv2.minAreaRect(contour)

				(bcx, bcy), (width, height), b_angle = rotatedRect

				imageFrame = cv2.rectangle(imageFrame, (x, y),
										(x + w, y + h),
										(255, 0, 0), 2)

				cv2.putText(imageFrame, "Blue Colour", (x, y),
							cv2.FONT_HERSHEY_SIMPLEX,
							1.0, (255, 0, 0))

				send_msg(f"pos#blue#{get_coords([bcx,bcy])}")

		# Program Termination
		cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
		if cv2.waitKey(10) & 0xFF == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			break


# Setup
send_msg("wake#camera")
start()
