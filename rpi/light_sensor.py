#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time

__author__ = 'Lev'
__license__ = "Polito"

GPIO.setmode(GPIO.BOARD)

#define the pin that goes to the circuit
pinLDR = 7
pinLED = 11
touch = False 

def rc_time ():
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pinLDR, GPIO.OUT)
    GPIO.output(pinLDR, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pinLDR, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pinLDR) == GPIO.LOW):
        count += 1

    return count

def led(lh):
    GPIO.setup(pinLED, GPIO.OUT)
    if lh == 1:
        GPIO.output(pinLED, GPIO.HIGH)
    else:
        GPIO.output(pinLED, GPIO.LOW)

#Catch when script is interupted, cleanup correctly
try:
    # Main loop
    while True:
        if rc_time() > 10000:
            if touch == False:
                print "Touched"
                led(1)
                touch = True
        else:
            if touch == True:
                print "Untouched"
                led(0)
                touch = False 
            
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
