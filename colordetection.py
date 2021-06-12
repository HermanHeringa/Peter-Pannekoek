# Python code for Multiple Color Detection


import numpy as np
import cv2
import time

# Capturing video through webcam
webcam = cv2.VideoCapture(0)
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



def tatat(mask, quadrant):
	pass

# Start a while loop
while(1):
	
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
	green_upper = np.array([100, 255, 255], np.uint8)
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
	res_red = cv2.bitwise_and(imageFrame, imageFrame,
							mask = red_mask)
	
	# For green color
	green_mask = cv2.dilate(green_mask, kernal)
	res_green = cv2.bitwise_and(imageFrame, imageFrame,
								mask = green_mask)
	
	# For blue color
	blue_mask = cv2.dilate(blue_mask, kernal)
	res_blue = cv2.bitwise_and(imageFrame, imageFrame,
							mask = blue_mask)

	# Creating contour to track red color
	contours, hierarchy = cv2.findContours(red_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 1000):
			x, y, w, h = cv2.boundingRect(contour)
			M = cv2.moments(contour)
			rotatedRect = cv2.minAreaRect(contour)

			(cx, cy), (width, height), r_angle = rotatedRect
		
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(0, 0,255), 2)

			cv2.putText(imageFrame, "Red Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (0, 0, 255))

			#Check if the difference is bigger than the threshold
			#If it is a quadrant has been crossed
			if r_difference > dif_threshold:
				red_quadrant -= 1
			elif r_difference < -1 * dif_threshold:
				red_quadrant += 1

			r_difference = r_prevAngle - r_angle
			r_prevAngle = r_angle
			r_heading = r_heading + r_difference + (90 * red_quadrant)

			print(f"R: {r_heading % 360}")
			

	# Creating contour to track green color
	contours, hierarchy = cv2.findContours(green_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
						
	#print(contours)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 1000):
			x, y, w, h = cv2.boundingRect(contour)
			rotatedRect = cv2.minAreaRect(contour)

			(cx, cy), (width, height), g_angle = rotatedRect

			M = cv2.moments(contour)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
	
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(0, 255, 0), 2)
            
			cv2.putText(imageFrame, "Green Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (0, 255, 0))

			#Check if the difference is bigger than the threshold
			#If it is a quadrant has been crossed
			if g_difference > dif_threshold:
				green_quadrant -= 1
			elif g_difference < -1 * dif_threshold:
				green_quadrant += 1

			g_difference = g_prevAngle - g_angle
			g_prevAngle = g_angle
			g_heading = g_heading + g_difference + (90 * green_quadrant)

			print(f"G: {g_heading % 360}")

	# Creating contour to track blue color
	contours, hierarchy = cv2.findContours(blue_mask,
										cv2.RETR_TREE,
										cv2.CHAIN_APPROX_SIMPLE)
	for pic, contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if(area > 1000):
			x, y, w, h = cv2.boundingRect(contour)
			M = cv2.moments(contour)
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])

			rotatedRect = cv2.minAreaRect(contour)

			(cx, cy), (width, height), b_angle = rotatedRect
			
			imageFrame = cv2.rectangle(imageFrame, (x, y),
									(x + w, y + h),
									(255, 0, 0), 2)
			
			cv2.putText(imageFrame, "Blue Colour", (x, y),
						cv2.FONT_HERSHEY_SIMPLEX,
						1.0, (255, 0, 0))
			
			#Check if the difference is bigger than the threshold
			#If it is a quadrant has been crossed
			if b_difference > dif_threshold:
				blue_quadrant -= 1
			elif b_difference < -1 * dif_threshold:
				blue_quadrant += 1

			b_difference = b_prevAngle - b_angle
			b_prevAngle = b_angle
			b_heading = b_heading + b_difference + (90 * blue_quadrant)

			print(f"B: {b_heading % 360}")
	
	# Program Termination
	cv2.imshow("Multiple Color Detection in Real-TIme", imageFrame)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyAllWindows()
		break	
