# import the necessary packages
import PySimpleGUI as sg  

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import win32api
import win32con
import math

def animate(x_old,y_old,x_new,y_new):
	x_r = 0.1 if (x_new >= x_old) else (-0.1)
	y_r = 0.1 if (y_new >= y_old) else (-0.1)
	for x,y in zip(np.arange(x_old,x_new,x_r),np.arange(y_old,y_new,y_r)):
		win32api.SetCursorPos((int(remap(x,0,640,0,1920)),int(remap(y,70,480,0,1080))))


def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

layout = [[sg.Canvas(background_color="white",size=(640,480),visible=True,key='canv')]]
window = sg.Window('Window Title', layout)  
#window = sg.Window('CAL', callayout)  

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
 
vs = VideoStream(src=0).start()

 
# allow the camera or video file to warm up
#time.sleep(2.0)

# keep looping
while True:
	# grab the current frame
	frame = vs.read()
	#print(frame.shape[0],frame.shape[1])
	frame = cv2.flip( frame, 1 )
 
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
 
	# resize the frame, blur it, and convert it to the HSV
	# color space
	#frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,	cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
 
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
		c = cnts[0]
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)


		#print(M)
		#print("NEXT")
		if not(M["m00"] == 0 or M["m00"] == 0): center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			#print(str(x) + "," + str(y))
			win32api.SetCursorPos((int(remap(x,0,640,0,1920)),int(remap(y,70,480,0,1080))))

			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2) 
			#print(x,y)
	
	# show the frame to our screen
	#cv2.imshow("Frame", frame)
	coloredmask = frame
	coloredmask[mask>0] = (0,255,0)
	cv2.imshow("Mask", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# if we are not using a video file, stop the camera video stream
vs.stop()

 
# close all windows
cv2.destroyAllWindows()