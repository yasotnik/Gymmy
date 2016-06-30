import RPi.GPIO as GPIO
import time
import sys
sys.path.insert(0, '../libs')
import db_actions

GPIO.setmode(GPIO.BOARD)

pinLDRA = 29
pinLEDA = 40
pinLDRB = 16
pinLEDB = 7
pinLDRC = 38
pinLEDC = 32
pinLDRD = 13
pinLEDD = 11
pinLDRE = 15
pinLEDE = 37
LDR_now = [0, 0, 0, 0, 0]
LDR_old = [0, 0, 0, 0, 0]
count_LDR = 0
i = 0
touched = ""
detouched = ""
pushed = ""
start_time = 0
stopped_by_user = 0
stopped_by_end = 0
map_name = ""
new_map_str = ""
new_map_wrote = 1
    
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
        
def touchedF(LDR_now):
    global touched
    global pushed
    global new_map_str
    global LDR_old
    global a
    if((LDR_now[0] > (LDR_old[0] + 2000)) and (pushed == "")):
        touched = "A"
        pushed = "A"
        new_map_str = new_map_str + "A,"
        #print "Touched: A"
    if((LDR_now[1] > (LDR_old[1] + 2000)) and (pushed == "")):
        touched = "B"
        pushed = "B"
        new_map_str = new_map_str + "B,"
        #print "Touched: B"
    if((LDR_now[2] > (LDR_old[2] + 2000)) and (pushed == "")):
        touched = "C"
        pushed = "C"
        new_map_str = new_map_str + "C,"
    if((LDR_now[3] > (LDR_old[3] + 2000)) and (pushed == "")):
        touched = "D"
        pushed = "D"
        new_map_str = new_map_str + "D,"
    if((LDR_now[4] > (LDR_old[4] + 2000)) and (pushed == "")):
        touched = "E"
        pushed = "E"
        new_map_str = new_map_str + "E,"

def detouchedF(LDR_now):
    global detouched
    global pushed
    global LDR_old
    if ((pushed == "A") and (LDR_now[0] < (LDR_old[0] + 2000))):
        detouched = "A"
        pushed = ""
        #print "Detouched: A"
    if ((pushed == "B") and (LDR_now[1] < (LDR_old[1] + 2000))):
        detouched = "B"
        pushed = ""
        #print "Detouched: B"
    if ((pushed == "C") and (LDR_now[2] < (LDR_old[2] + 2000))):
        detouched = "C"
        pushed = ""
    if ((pushed == "D") and (LDR_now[3] < (LDR_old[3] + 2000))):
        detouched = "D"
        pushed = ""
    if ((pushed == "E") and (LDR_now[4] < (LDR_old[4] + 2000))):
        detouched = "E"
        pushed = ""
        
def changeLED(dataArr):
    global i
    global start_time
    if(dataArr[i] == "A"):
        led(1, pinLEDA)
        led(0, pinLEDB)
        led(0, pinLEDC)
        led(0, pinLEDD)
        led(0, pinLEDE)
    if(dataArr[i] == "B"):
        led(0, pinLEDA)
        led(1, pinLEDB)
        led(0, pinLEDC)
        led(0, pinLEDD)
        led(0, pinLEDE)
    if(dataArr[i] == "C"):
        led(0, pinLEDA)
        led(0, pinLEDB)
        led(1, pinLEDC)
        led(0, pinLEDD)
        led(0, pinLEDE)
    if(dataArr[i] == "D"):
        led(0, pinLEDA)
        led(0, pinLEDB)
        led(0, pinLEDC)
        led(1, pinLEDD)
        led(0, pinLEDE)
    if(dataArr[i] == "E"):
        led(0, pinLEDA)
        led(0, pinLEDB)
        led(0, pinLEDC)
        led(0, pinLEDD)
        led(1, pinLEDE)
    if(dataArr[i] == ";"):
        led(0, pinLEDA)
        led(0, pinLEDB)
        led(0, pinLEDC)
        led(0, pinLEDD)
        led(0, pinLEDE)
        stopped_by_end = 1
        print ("Track ended")
        db_actions.add_time(int(time.time() - start_time))
        db_actions.insert_stop()
    

def checkLDR(track):
    data = str(db_actions.get_map(str(track)))
    dataArr = data.split(",")
    global i
    global start_time
    if i == 0:
        changeLED(dataArr)
    if (touched == dataArr[i]):
        if (i == 0):
            start_time = time.time()
            stopped_by_end = 0
        i = i+1
        changeLED(dataArr)
        

LDR_now[0] = rc_time(pinLDRA)
LDR_now[1] = rc_time(pinLDRB)
LDR_now[2] = rc_time(pinLDRC)
LDR_now[3] = rc_time(pinLDRD)
LDR_now[4] = rc_time(pinLDRE)


try:
    while True:
        #time.sleep(0.3)
        #print ("0: " + str(rc_time(pinLDRA)) + "   1: " + str(rc_time(pinLDRB)))
        data_start = db_actions.get_status("start")
        data_stop = db_actions.get_status("stop")
        data_map = db_actions.get_new_name()

        LDR_old[0] = LDR_now[0]
        LDR_old[1] = LDR_now[1]
        LDR_old[2] = LDR_now[2]
        LDR_old[3] = LDR_now[3]
        LDR_old[4] = LDR_now[4]
        
        LDR_now[0] = rc_time(pinLDRA)
        LDR_now[1] = rc_time(pinLDRB)
        LDR_now[2] = rc_time(pinLDRC)
        LDR_now[3] = rc_time(pinLDRD)
        LDR_now[4] = rc_time(pinLDRE)
        
            
        
        #print ("previous:  " + str(LDR_old[0]) + "  " + str(LDR_old[1]) + "  " + str(LDR_old[2]) + "  " + str(LDR_old[3]) + "  " + str(LDR_old[4]))
        #print ("NOW:  " + str(LDR_now[0]) + "  " + str(LDR_now[1]) + "  " + str(LDR_now[2]) + "  " + str(LDR_now[3]) + "  " + str(LDR_now[4]))
    
        #print str(data_start) + str(data_stop)
        if ((str(data_map) != "NULL") and (str(data_stop) == "stop")):
            if new_map_wrote == 1:
                new_map_str = ""
            new_map_wrote = 0
            map_name = str(data_map)
            touched = ""
            detouched = ""
            detouchedF(LDR_now)
            touchedF(LDR_now)
            print new_map_str
        if ((str(data_map) == "NULL") and (new_map_wrote == 0) and (str(data_stop) == "stop")):
            new_map_str = new_map_str + ";"
            print new_map_str
            db_actions.add_new_path(map_name, new_map_str)
            new_map_wrote = 1
        if (str(data_start) == "start"):
            track = db_actions.get_map_status("huec")
            touched = ""
            detouched = ""
            detouchedF(LDR_now)
            touchedF(LDR_now)
            checkLDR(track)            
        if (str(data_stop) == "stop"):                
            led(0, pinLEDA)
            led(0, pinLEDB)
            led(0, pinLEDC)
            led(0, pinLEDD)
            led(0, pinLEDE)
            i = 0
            pass
except KeyboardInterrupt:
    i = 0
    pass
finally:
    i = 0
    GPIO.cleanup()
