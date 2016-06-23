import RPi.GPIO as GPIO
import time
import socket
import db_actions
import os

GPIO.setmode(GPIO.BOARD)

pinLDR0 = 7
pinLED0 = 11
pinLDR1 = 16
pinLED1 = 18
d = locals()
touch0 = False
touch1 = False
sock = socket.socket()
sock.connect(('192.168.1.67', 9092))
pathDBactions = os.path.abspath("../libs/db_actions.py")
    
def rc_time (pinLDR):
    count = 0
  
    GPIO.setup(pinLDR, GPIO.OUT)
    GPIO.output(pinLDR, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(pinLDR, GPIO.IN)

    while (GPIO.input(pinLDR) == GPIO.LOW):
        count += 1

    return count

def led(lh, pinLED):
    GPIO.setup(pinLED, GPIO.OUT)
    if lh == 1:
        GPIO.output(pinLED, GPIO.HIGH)
    else:
        GPIO.output(pinLED, GPIO.LOW)

def touched(id, touch, pin1, data):
    if touch == False:
        led(0, pin1)
        if (str(data) = "B"):
            led(1, pinLED1)
        if (str(data) = ";"):
            led(0, pinLED0)
            led(0, pinLED1)
        if (str(data) = "A"):
            led(1, pinLED0)
        touch = True
        
def detouched(touch):
    if touch == True:
        touch = False

def parse(id):
    data = str(pathDBactions.get_map(easy))
    dataArr = data.split(str=",")
    return dataArr[id]

def checkLDR():
    if rc_time(pinLDR0) > 5000:
        touched(0, touch0, pinLED0, parse(1))
    else:
        detouched(touch0)
        if rc_time(pinLDR1) > 5000:
            touched(1, touch1, pinLED1, parse(2))
        else:
            detouched(touch1)

try:
    while True:
        time.sleep(0.5)
        print ("0: " + str(rc_time(pinLDR0)) + "   1: " + str(rc_time(pinLDR1)))
        data_start = pathDBactions.get_status("start")
        data_stop = pathDBactions.get_status("stop")
        if str(data_start) == "start":
            checkLDR()            
        elif str(data_stop) == "stop":
            led(0, pinLED0)
            led(0, pinLED1)
            pass
except KeyboardInterrupt:
    sock.close()
    pass
finally:
    GPIO.cleanup()
    sock.close()
