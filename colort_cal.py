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

current_cal = 'g'

def remap(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

layout = [
		[sg.Text('H Low'), sg.Slider(range=(0,255), default_value=0, size=(20,15), orientation='horizontal',key="hl")],
		[sg.Text('S Low'), sg.Slider(range=(0,255), default_value=0, size=(20,15), orientation='horizontal',key="sl")],
		[sg.Text('V Low'), sg.Slider(range=(0,255), default_value=0, size=(20,15), orientation='horizontal',key="vl")],
		[sg.Text('H High'), sg.Slider(range=(0,255), default_value=255, size=(20,15), orientation='horizontal',key="hh")],
		[sg.Text('S High'), sg.Slider(range=(0,255), default_value=255, size=(20,15), orientation='horizontal',key="sh")],
		[sg.Text('V High'), sg.Slider(range=(0,255), default_value=255, size=(20,15), orientation='horizontal',key="vh")],
		
		[sg.Radio(text= 'Green',group_id = "color", key = "green", default=True, enable_events=True),
		sg.Radio(text= 'Red',group_id = "color", key ="red", enable_events=True),
		sg.Radio(text= 'Blue',group_id = "color", key = "blue", enable_events=True),
		
		sg.Button(button_text="Save",key="save",enable_events=True)]
		
		
		]
window = sg.Window('Window Title', layout)  
#window = sg.Window('CAL', callayout)  

f=open("col.cfg", "r")
greenLower = (int(f.readline()), int(f.readline()), int(f.readline()))
greenUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
redLower = (int(f.readline()), int(f.readline()), int(f.readline()))
redUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
blueLower = (int(f.readline()), int(f.readline()), int(f.readline()))
blueUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
f.close()

#yellowLower = (0, 0, 0)
#yellowUpper = (0, 0, 0)
vs = VideoStream(src=0).start()

juststart = True
 
# keep looping
while True:
	event, values = window.Read(timeout=1)

	if event == "green" or juststart == True:
		window.Element('hl').Update(value=greenLower[0])  
		window.Element('sl').Update(value=greenLower[1])  
		window.Element('vl').Update(value=greenLower[2])  		
		window.Element('hh').Update(value=greenUpper[0])  		
		window.Element('sh').Update(value=greenUpper[1])  		
		window.Element('vh').Update(value=greenUpper[2])
		current_cal = 'g'
		
	if event == "red":
		window.Element('hl').Update(value=redLower[0])  
		window.Element('sl').Update(value=redLower[1])  
		window.Element('vl').Update(value=redLower[2])  		
		window.Element('hh').Update(value=redUpper[0])  		
		window.Element('sh').Update(value=redUpper[1])  		
		window.Element('vh').Update(value=redUpper[2])  
		current_cal = 'r'
		
	if event == "blue":
		window.Element('hl').Update(value=blueLower[0])  
		window.Element('sl').Update(value=blueLower[1])  
		window.Element('vl').Update(value=blueLower[2])  		
		window.Element('hh').Update(value=blueUpper[0])  		
		window.Element('sh').Update(value=blueUpper[1])  		
		window.Element('vh').Update(value=blueUpper[2])  
		current_cal = 'b'
		
	if event == "save":
		f= open("col.cfg","w+");
		f.write(str(round(greenLower[0])))
		f.write("\n")  
		f.write(str(round(greenLower[1])))
		f.write("\n")  
		f.write(str(round(greenLower[2])))
		f.write("\n")  		
		f.write(str(round(greenUpper[0])))
		f.write("\n")  		
		f.write(str(round(greenUpper[1])))
		f.write("\n")  		
		f.write(str(round(greenUpper[2])))
		f.write("\n")
		f.write(str(round(redLower[0])))
		f.write("\n")  
		f.write(str(round(redLower[1])))
		f.write("\n")  
		f.write(str(round(redLower[2])))
		f.write("\n")  
		f.write(str(round(redUpper[0])))
		f.write("\n")  
		f.write(str(round(redUpper[1])))
		f.write("\n")  
		f.write(str(round(redUpper[2])))
		f.write("\n")  
		f.write(str(round(blueLower[0])))
		f.write("\n")  
		f.write(str(round(blueLower[1])))
		f.write("\n")  
		f.write(str(round(blueLower[2])))
		f.write("\n")  
		f.write(str(round(blueUpper[0])))
		f.write("\n")  
		f.write(str(round(blueUpper[1])))
		f.write("\n")  
		f.write(str(round(blueUpper[2])))
		f.write("\nEND")
		f.close()
		
	juststart = False


	if values['green']:
		greenLower=(values['hl'], values['sl'], values['vl'])
		greenUpper=(values['hh'], values['sh'], values['vh'])

	if values['red']:
		redLower=(values['hl'], values['sl'], values['vl'])
		redUpper=(values['hh'], values['sh'], values['vh'])
		
	if values['blue']:
		blueLower=(values['hl'], values['sl'], values['vl'])
		blueUpper=(values['hh'], values['sh'], values['vh'])
		
	frame = vs.read()
	#print(frame.shape[0],frame.shape[1])
	frame = cv2.flip( frame, 1 )
 

	if frame is None:
		break
 
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
 
	maskg = cv2.inRange(hsv, greenLower, greenUpper)
	maskg = cv2.erode(maskg, None, iterations=2)
	maskg = cv2.dilate(maskg, None, iterations=2)

	maskr = cv2.inRange(hsv, redLower, redUpper)
	maskr = cv2.erode(maskr, None, iterations=2)
	maskr = cv2.dilate(maskr, None, iterations=2)

	maskb = cv2.inRange(hsv, blueLower, blueUpper)
	maskb = cv2.erode(maskb, None, iterations=2)
	maskb = cv2.dilate(maskb, None, iterations=2)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cntsg = cv2.findContours(maskg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cntsg = imutils.grab_contours(cntsg)
	centerg = None

	cntsr = cv2.findContours(maskr.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cntsr = imutils.grab_contours(cntsr)
	centerr = None

	cntsb = cv2.findContours(maskb.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cntsb = imutils.grab_contours(cntsb)
	centerb = None
 
 
	# only proceed if at least one contour was found
	if len(cntsg) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cntsg = sorted(cntsg, key=cv2.contourArea, reverse=True)
		cg = cntsg[0]
		((xg, yg), radiusg) = cv2.minEnclosingCircle(cg)
		Mg = cv2.moments(cg)

		if not(Mg["m00"] == 0 or Mg["m00"] == 0): centerg = (int(Mg["m10"] / Mg["m00"]), int(Mg["m01"] / Mg["m00"]))

		# only proceed if the radius meets a minimum size
		if radiusg > 10:
			#print(str(x) + "," + str(y))
			#win32api.SetCursorPos((int(remap(x,0,640,0,1920)),int(remap(y,70,480,0,1080))))

			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(xg), int(yg)), int(radiusg), (0, 255, 0), 2) 
			#print(x,y)

	if len(cntsr) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cntsr = sorted(cntsr, key=cv2.contourArea, reverse=True)
		cr = cntsr[0]
		((xr, yr), radiusr) = cv2.minEnclosingCircle(cr)
		Mr = cv2.moments(cr)

		if not(Mr["m00"] == 0 or Mr["m00"] == 0): centerr = (int(Mr["m10"] / Mr["m00"]), int(Mr["m01"] / Mr["m00"]))

		# only proceed if the radius meets a minimum size
		if radiusr > 10:
			#print(str(x) + "," + str(y))
			#win32api.SetCursorPos((int(remap(x,0,640,0,1920)),int(remap(y,70,480,0,1080))))

			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(xr), int(yr)), int(radiusr), (0, 0, 255), 2) 
			
	if len(cntsb) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cntsb = sorted(cntsb, key=cv2.contourArea, reverse=True)
		cb = cntsb[0]
		((xb, yb), radiusb) = cv2.minEnclosingCircle(cb)
		Mb = cv2.moments(cb)


		if not(Mb["m00"] == 0 or Mb["m00"] == 0): centerr = (int(Mb["m10"] / Mb["m00"]), int(Mb["m01"] / Mb["m00"]))

		# only proceed if the radius meets a minimum size
		if radiusb > 10:
			#print(str(x) + "," + str(y))
			#win32api.SetCursorPos((int(remap(x,0,640,0,1920)),int(remap(y,70,480,0,1080))))

			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(xb), int(yb)), int(radiusb), (255, 0, 0), 2) 
	
	# show the frame to our screen
	#cv2.imshow("Frame", frame)
	coloredmask = frame
	if (current_cal == 'g'): coloredmask[maskg>0] = (0,255,0)
	if (current_cal == 'r'): coloredmask[maskr>0] = (0,0,255)
	if (current_cal == 'b'): coloredmask[maskb>0] = (255,0,0)
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# if we are not using a video file, stop the camera video stream
vs.stop()

 
# close all windows
cv2.destroyAllWindows()