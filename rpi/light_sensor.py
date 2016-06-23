import RPi.GPIO as GPIO
import time
import socket
import db_actions

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
        pin = d[str(data)]
        led(1, pin)
        touch = True
        
def detouched(touch):
    if touch == True:
        touch = False    

try:
    while True:
        time.sleep(1)
        data = db_actions.get_status("start")[0]
        if str(data) == "start":
            #print ("0: " + str(rc_time(pinLDR0)) + "   1: " + str(rc_time(pinLDR1)))
            if rc_time(pinLDR0) > 5000:
                sock.send('0')
                touched(0, touch0, pinLED0, sock.recv(256))
            else:
                detouched(touch0)
            if rc_time(pinLDR1) > 5000:
                sock.send('1')
                touched(1, touch1, pinLED1, sock.recv(256))
            else:
                detouched(touch1)
                
except KeyboardInterrupt:
    sock.close()
    pass
finally:
    GPIO.cleanup()
    sock.close()
