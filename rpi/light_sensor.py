import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, '../libs')
import db_actions

GPIO.setmode(GPIO.BOARD)

pinLDRA = 7
pinLEDA = 11
pinLDRB = 16
pinLEDB = 18
LDR = [0, 0]
i = 0
touched = ""
detouched = ""
pushed = ""
d = locals()
touch0 = False
touch1 = False
    
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
        
def touchedF(LDR):
    global touched
    global pushed
    if((LDR[0] > 3000) and (pushed == "")):
        touched = "A"
        pushed = "A"
        print "Touched: A"
    if((LDR[1] > 3000) and (pushed == "")):
        touched = "B"
        pushed = "B"
        print "Touched: B"

def detouchedF(LDR):
    global detouched
    global pushed
    if ((pushed == "A") and (LDR[0] < 3000)):
        detouched = "A"
        pushed = ""
        print "Detouched: A"
    if ((pushed == "B") and (LDR[1] < 3000)):
        detouched = "B"
        pushed = ""
        print "Detouched: B"
        
def changeLED(dataArr):
    global i
    if(dataArr[i] == "A"):
        led(1, pinLEDA)
        led(0, pinLEDB)
    if(dataArr[i] == "B"):
        led(1, pinLEDB)
        led(0, pinLEDA)
    if(dataArr[i] == ";"):
        led(0, pinLEDB)
        led(0, pinLEDA)
        db_actions.insert_stop()
    

def checkLDR():
    data = str(db_actions.get_map("Easy"))
    dataArr = data.split(",")
    global i
    #print dataArr
    #print "touched: " + str(touched) + "  detouched: " + str(detouched)
    if i == 0:
        changeLED(dataArr)
    if (touched == dataArr[i]):
        i = i+1
        changeLED(dataArr)
        

try:
    while True:
        time.sleep(0.5)
        #print ("0: " + str(rc_time(pinLDRA)) + "   1: " + str(rc_time(pinLDRB)))
       
        data_start = db_actions.get_status("start")
        data_stop = db_actions.get_status("stop")
        print "START: " + (str(data_start)) + "  STOP: " + (str(data_stop))
        if str(data_start) == "start":
            LDR[0] = rc_time(pinLDRA)
            LDR[1] = rc_time(pinLDRB)
            touched = ""
            detouched = ""
            detouchedF(LDR)
            touchedF(LDR)
            checkLDR()            
        elif str(data_stop) == "stop":
            led(0, pinLEDA)
            led(0, pinLEDB)
            i = 0
            pass
except KeyboardInterrupt:
    i = 0
    pass
finally:
    i = 0
    GPIO.cleanup()
# A A B B A B A B;
