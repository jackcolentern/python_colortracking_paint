# import the necessary packages
import PySimpleGUI as sg  

from collections import deque
from imutils.video import VideoStream
import numpy as np

import numpy.random.common
import numpy.random.bounded_integers
import numpy.random.entropy

#import argparse
import cv2
import imutils
import time
import math
import subprocess
import sys
import pyautogui
import pygame
from pygame.locals import *
from threading import Thread


imageno = 0
spacemode = 0
calmode = 0

if (len(sys.argv) >= 2 and sys.argv[1] == "cal"):
	print("cal mode")
	calmode = 1

if (len(sys.argv) >= 2 and sys.argv[1] == "calspace"):
	print("cal space mode")
	calmode = 1
	spacemode = 1

current_cal = 'g'
clicked = 0
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
		sg.Radio(text= 'White',group_id = "color", key = "white", enable_events=True),
		sg.Button(button_text="Save",key="save",enable_events=True)]
		
		
		]

locked = True

image = pygame.image.load('./images/' + str(0) + '.png')

resw = 1920
resh = 1080
#res = subprocess.check_output("wmic path Win32_VideoController get VideoModeDescription").decode("utf-8").splitlines()
#res = res[2].split("x")
#resw = int(res[0])
#resh = int(res[1])
if (len(sys.argv) == 4):
	resw = int(sys.argv[2])
	resh = int(sys.argv[3])

siz = 10

if (len(sys.argv) == 5):
	siz = int(sys.argv[4])

print(resw,resh)

window = sg.Window('Window Title', layout)  
#window = sg.Window('CAL', callayout)  

f=open("col.cfg", "r")
greenLower = (int(f.readline()), int(f.readline()), int(f.readline()))
greenUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
redLower = (int(f.readline()), int(f.readline()), int(f.readline()))
redUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
blueLower = (int(f.readline()), int(f.readline()), int(f.readline()))
blueUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
whiteLower = (int(f.readline()), int(f.readline()), int(f.readline()))
whiteUpper = (int(f.readline()), int(f.readline()), int(f.readline()))
f.close()

#yellowLower = (0, 0, 0)
#yellowUpper = (0, 0, 0)
vs = VideoStream(src=0).start()

juststart = True
 

pygame.init()
screen=pygame.display.set_mode((resw,resh), pygame.FULLSCREEN)
pygame.display.set_caption('Let\'s Paint')
pygame.display.set_mode((0, 0))

background=pygame.Surface(screen.get_size())
canvas=pygame.Surface(screen.get_size())

background=background.convert()
color=(0,0,0)
startPos=(0,0)
clock=pygame.time.Clock()
background.fill((255,255,255))
font=pygame.font.SysFont('arial',20)
colorName="Black"
welcomeFont=pygame.font.SysFont('arial',30)
colorConfigFont=pygame.font.SysFont('arial',20)

#pygame.draw.rect(background,(0,0,255) ,pygame.Rect(0, 0, resw, resh))

# keep looping
while True:
	if (calmode == 1) :
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

		if event == "white":
			window.Element('hl').Update(value=whiteLower[0])  
			window.Element('sl').Update(value=whiteLower[1])  
			window.Element('vl').Update(value=whiteLower[2])  		
			window.Element('hh').Update(value=whiteUpper[0])  		
			window.Element('sh').Update(value=whiteUpper[1])  		
			window.Element('vh').Update(value=whiteUpper[2])  
			current_cal = 'w'
			
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
			f.write("\n")  
			f.write(str(round(whiteLower[0])))
			f.write("\n")  
			f.write(str(round(whiteLower[1])))
			f.write("\n")  
			f.write(str(round(whiteLower[2])))
			f.write("\n")  
			f.write(str(round(whiteUpper[0])))
			f.write("\n")  
			f.write(str(round(whiteUpper[1])))
			f.write("\n")  
			f.write(str(round(whiteUpper[2])))
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

		if values['white']:
			whiteLower=(values['hl'], values['sl'], values['vl'])
			whiteUpper=(values['hh'], values['sh'], values['vh'])
		
	frame = vs.read()

	frame = cv2.flip( frame, 1 )

	frame_processed = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame_processed = frame_processed.swapaxes(0,1)
	frame_processed = cv2.resize(frame_processed,(resh,resw))
	bg_camera = pygame.surfarray.make_surface(frame_processed)


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

	maskw = cv2.inRange(hsv, whiteLower, whiteUpper)
	maskw = cv2.erode(maskw, None, iterations=2)
	maskw = cv2.dilate(maskw, None, iterations=2)

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

	cntsw = cv2.findContours(maskw.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cntsw = imutils.grab_contours(cntsw)
	centerw = None
 	
	pressed=pygame.key.get_pressed()

	# only proceed if at least one contour was found
	if len(cntsg) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cntsg = sorted(cntsg, key=cv2.contourArea, reverse=True)
		cg = cntsg[0]
		((xg, yg), radiusg) = cv2.minEnclosingCircle(cg)
		Mg = cv2.moments(cg)

		#if not(Mg["m00"] == 0): centerg = (int(Mg["m10"] / Mg["m00"]), int(Mg["m01"] / Mg["m00"]))

		# only proceed if the radius meets a minimum size
		if radiusg > siz:
			color =(0,255,0)
			#print(str(x) + "," + str(y))
			endPos=(int(remap(xg,0,640,0,resw)),int(remap(yg,0,480,0,resh)))
			if clicked == 0: startPos=endPos
			clicked = 1
			if(spacemode == 0 or (spacemode == 1 and pressed[K_SPACE])): pygame.draw.line(background,color,startPos,endPos,int(radiusg))
			startPos=endPos
			#win32api.SetCursorPos((int(remap(xg,0,640,0,resw)),int(remap(yg,70,480,0,resh))))
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
        
		#if not(Mr["m00"] == 0): centerr = (int(Mr["m10"] / Mr["m00"]), int(Mr["m01"] / Mr["m00"]))
		# only proceed if the radius meets a minimum size
		if radiusr > siz:
			color =(255,0,0)
			#print(str(x) + "," + str(y))
			endPos=(int(remap(xr,0,640,0,resw)),int(remap(yr,0,480,0,resh)))
			if clicked == 0: startPos=endPos
			clicked = 1
			if(spacemode == 0 or (spacemode == 1 and pressed[K_SPACE])): pygame.draw.line(background,color,startPos,endPos,int(radiusr))
			startPos=endPos

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


		#if not(Mb["m00"] == 0): centerb = (int(Mb["m10"] / Mb["m00"]), int(Mb["m01"] / Mb["m00"]))

		# only proceed if the radius meets a minimum size
		if radiusb > siz:
			color =(0,0,255)
			#print(str(x) + "," + str(y))
			#win32api.SetCursorPos((int(remap(x,0,640,0,1920)),int(remap(y,70,480,0,1080))))
			endPos=(int(remap(xb,0,640,0,resw)),int(remap(yb,0,480,0,resh)))
			if clicked == 0: startPos=endPos
			clicked = 1
			if(spacemode == 0 or (spacemode == 1 and pressed[K_SPACE])): pygame.draw.line(background,color,startPos,endPos,int(radiusb))
			startPos=endPos

			cv2.circle(frame, (int(xb), int(yb)), int(radiusb), (255, 0, 0), 2) 

	if len(cntsw) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		cntsw = sorted(cntsw, key=cv2.contourArea, reverse=True)
		cw = cntsw[0]
		((xw, yw), radiusw) = cv2.minEnclosingCircle(cw)
		Mw = cv2.moments(cw)


		#if not(Mw["m00"] == 0): centerw = (int(Mw["m10"] / Mw["m00"]), int(Mw["m01"] / Mw["m00"]))

		# only proceed if the radius meets a minimum size
		if radiusw > siz:
			color =(255,255,255)
			#print(str(x) + "," + str(y))
			endPos=(int(remap(xw,0,640,0,resw)),int(remap(yw,0,480,0,resh)))
			if clicked == 0: startPos=endPos
			clicked = 1
			if(spacemode == 0 or (spacemode == 1 and pressed[K_SPACE])): pygame.draw.line(background,color,startPos,endPos,int(radiusw))
			startPos=endPos
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(xw), int(yw)), int(radiusw), (255, 255, 255), 2) 
	
	if not (len(cntsr) > 0 or len(cntsg) > 0 or len(cntsb) > 0 or len(cntsw) > 0):
		clicked = 0
	# show the frame to our screen
	#cv2.imshow("Frame", frame)
	coloredmask = frame
	if (current_cal == 'g'): coloredmask[maskg>0] = (0,255,0)
	if (current_cal == 'r'): coloredmask[maskr>0] = (0,0,255)
	if (current_cal == 'b'): coloredmask[maskb>0] = (255,0,0)
	if (current_cal == 'w'): coloredmask[maskw>0] = (0,255,255)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	canvas.blit(bg_camera,(0,0))
	background.set_alpha(128) 

	canvas.blit(background,(0,0))

	canvas.blit(image,(0,0))


	screen.blit(canvas,(0,0))

	pygame.display.flip()


	if pressed[K_c]:
		pygame.draw.rect(background,(255,255,255) ,pygame.Rect(0, 0, resw, resh))

	if pressed[K_r]:
		pygame.draw.rect(background,(255,0,0) ,pygame.Rect(0, 0, resw, resh))

	if pressed[K_g]:
		pygame.draw.rect(background,(0,255,0) ,pygame.Rect(0, 0, resw, resh))

	if pressed[K_b]:
		pygame.draw.rect(background,(0,0,255) ,pygame.Rect(0, 0, resw, resh))

	if locked == False and pressed[K_e] :
		if(imageno == 5): imageno = 0
		else: imageno = imageno + 1
		locked = True
		image = pygame.image.load('./images/' + str(imageno) + '.png')

	if locked == False and pressed[K_w] and locked == False:
		if(imageno == 0): imageno = 5
		else: imageno = imageno - 1
		locked = True
		image = pygame.image.load('./images/' + str(imageno) + '.png')


	if not (pressed[K_e] or pressed[K_w]): 
		locked = False


	if pressed[K_q]:
		exit()
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# if we are not using a video file, stop the camera video stream
vs.stop()

 
# close all windows
cv2.destroyAllWindows()