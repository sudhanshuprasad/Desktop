import RPi.GPIO as GPIO
from picamera import PiCamera
import time
import sys
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()

try:
    while True:
        
        if(GPIO.input(37)==False):
            print("jor se daba diya madharchod")
            #camera.start_preview()
            time.sleep(0.5)
            current_dateTime = datetime.now()
            print(current_dateTime)
            #camera.capture("/home/raspberry/Desktop/images/photo"+str(current_dateTime)+".jpg")
            try:
                camera.capture("/home/raspberry/Desktop/images/photo"+str(current_dateTime)+".jpg")
            except:
                print("something bad happend... very very bad...")
                
            try:
                camera.capture("/media/raspberry/CDC0-52C7/photo"+str(current_dateTime)+".jpg")
            except:
                print("no usb found")
            #camera.stop_preview()
        else:
            print("button daba madharchod")
        time.sleep(0.05)

except KeyboardInterrupt:
    camera.close()
    sys.exit(0)

GPIO.cleanup()
