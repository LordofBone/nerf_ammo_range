#!/usr/bin/env python
#imports
import sys,os
import colorsys
import time

import rainbowhat

import time

import Adafruit_VCNL40xx

vcnl = Adafruit_VCNL40xx.VCNL4010()

#the class used for counting the shots up/down and resetting
class adjustShots(object):
	
	def __init__(self, shotsN):
		self.shotsN = shotsN
	
	def changeAmmo(self, shotsN):
		self.shotsN = shotsN
		return self.shotsN
		
	def showAmmo(self):
		return self.shotsN
	
	def plusShots(self):
		if self.shotsN < 20:
			self.shotsN = self.shotsN + 1
		else:
			self.shotsN = (-0)
		return self.shotsN
		
	def minusShots(self):
		if not self.shotsN < 0:
			self.shotsN = self.shotsN - 1
		return self.shotsN

#here we set the number of shots that are currently in the magazine (0 is -1 here as the counter works by 0 indexing)		
shotsMag = adjustShots(-1)
#here we set the default number of shots per magazine that will be used (as above 11 will count as 12 due to 0 indexing)
shotsPerMag = adjustShots(11)

#display function for the leds
def display_message(message):
    rainbowhat.display.print_str(message)
    rainbowhat.display.show()

#this is the code that handles showing the number of leds at the top, first 7 being red, next 7 orange and final 7 green for a total of-
#21 possible shots, the code here also sets the colour 'below' it for empty shots, so you will see orange shots remaining below green shots etc.
#(check the youtube video linked in the guide on my site for how this works)    
def display_shots(shot_count):
	if shot_count <= 6:
		for x in range(7):
			if x <= shot_count:
				rainbowhat.rainbow.set_pixel(x, 50, 0, 0, brightness=0.1)
				rainbowhat.rainbow.show()
			else:
				rainbowhat.rainbow.set_pixel(x, 0, 0, 0, brightness=0.1)
				rainbowhat.rainbow.show()

	if shot_count > 6 and shot_count < 14:
		for x in range(7):
			shot_count_2 = shot_count - 7
			if x <= shot_count_2:
				rainbowhat.rainbow.set_pixel(x, 200, 50, 0, brightness=0.1)
				rainbowhat.rainbow.show()
			else:
				rainbowhat.rainbow.set_pixel(x, 50, 0, 0, brightness=0.1)
				rainbowhat.rainbow.show()					

	if shot_count > 13:
		for x in range(7):
			shot_count_3 = shot_count - 14
			if x <= shot_count_3:
				rainbowhat.rainbow.set_pixel(x, 0, 50, 0, brightness=0.1)
				rainbowhat.rainbow.show()
			else:
				rainbowhat.rainbow.set_pixel(x, 200, 50, 0, brightness=0.1)
				rainbowhat.rainbow.show()
			
display_shots(shotsMag.showAmmo())

#the 'A' button will cleanly shut the device down
@rainbowhat.touch.A.press()
def press_a(channel):
	os.system("sudo shutdown now")
	pass

#the 'B' button will count the number of shots per mag up +1, looping back around to 1 once it reaches 21
@rainbowhat.touch.B.press()
def press_b(channel):
	shotsPerMag.plusShots()
	display_shots(shotsPerMag.showAmmo())
	time.sleep(1)
	display_shots(shotsMag.showAmmo())
	pass

#the 'C' button initiates a 'reload', so when you put a mag in or reload it will reset the leds to show remaining ammo in the current mag
@rainbowhat.touch.C.press()
def press_c(channel):
	shotsMag.changeAmmo(shotsPerMag.showAmmo())
	print (shotsMag.showAmmo())
	display_shots(shotsMag.showAmmo())
	pass

#loop for detecting proximity - proximity decreasing when a shot passes the sensor indicating a shot and calling the class-
#for the current magazine to minus one shot
try:
	while True:

		proximity = vcnl.read_proximity()

		if proximity > 2540:
			display_shots(shotsMag.minusShots())
			print (shotsMag.showAmmo())
			time.sleep(1)
		
except KeyboardInterrupt:
    pass
