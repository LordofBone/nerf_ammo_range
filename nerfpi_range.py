#!/usr/bin/env python

#general imports
import time
import colorsys

import rainbowhat

import RPi.GPIO as GPIO
import time

#setup for the GPIO
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

#loop for measuring distance, this fires out a pulse and measures time to return, it then converts to an int to remove decimals and-
#finally to a string to be sent to the led readout on the lower part of the rainbow hat
try:
    while True:
		
		#print "Distance Measurement In Progress"



		GPIO.output(TRIG, False)
		#print "Waiting For Sensor To Settle"
		time.sleep(2)

		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO)==0:
		  pulse_start = time.time()

		while GPIO.input(ECHO)==1:
		  pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150

		distance = int(distance)
		
		distance = str(distance)

		print "Distance:",distance,"cm"

		rainbowhat.display.clear()
		rainbowhat.display.print_str(distance)
		rainbowhat.display.show()

		#time.sleep(1)

except KeyboardInterrupt:
    pass

#cleanup code for exiting
rainbowhat.display.clear()
rainbowhat.display.show()

GPIO.cleanup()
