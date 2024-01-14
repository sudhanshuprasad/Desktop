'''
  Send '/picam3' to your Telegram bot to request photo
  Devices:
  - Raspberry Pi Zero W
    https://my.cytron.io/p-raspberry-pi-zero-w-and-bundles
  - Raspberry Pi Camera Module 3
    https://my.cytron.io/p-raspberry-pi-camera-module-3-12mp-with-auto-focus-lens
  
  Install Telepot
  - sudo pip3 install telepot
'''

import time
import sys
import telepot
import RPi.GPIO as GPIO

from lcd_api import LcdApi
from i2c_lcd import I2cLcd

from picamera import PiCamera
from libcamera import controls
from libcamera import Transform

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Button to GPIO40
GPIO.setup(40, GPIO.OUT) #Button to GPIO40
GPIO.setup(38, GPIO.OUT) #Button to GPIO38

lcd = I2cLcd(1, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
lcd.clear()
camera = PiCamera()
#picam2 = Picamera2()
#capture_config = picam2.create_still_configuration(transform = Transform(hflip=True, vflip=True))
#picam2.start()

#picam2.set_controls({"AfMetering": controls.AfMeteringEnum.Auto})
#picam2.set_controls({"AfMode": controls.AfModeEnum.Auto})

def handle(msg):
    global telegramText
    global chat_id
    global receiveTelegramMessage

    chat_id = msg['chat']['id']
    telegramText = msg['text']

    print("Message received from " + str(chat_id))
    
    if telegramText == "/start":
        bot.sendMessage(chat_id, "Welcome to Alcohol Detector Bot \n type /picam3 to start")
    else:
        receiveTelegramMessage = True

def capture():
    print("Capturing photo...")
    camera.start_preview()
    time.sleep(5)

    #picam2.autofocus_cycle()
    #image = picam2.switch_mode_and_capture_file(capture_config, "photo.jpg")
    camera.capture("./photo.jpg")
    camera.stop_preview()

    print("Sending photo to " + str(chat_id))
    bot.sendPhoto(chat_id, photo = open('./photo.jpg', 'rb'))

bot = telepot.Bot('6743718320:AAGlFplz4UOOLrozaPrcVTcCY2bjWSKSc9I')
bot.message_loop(handle)

receiveTelegramMessage = False
sendTelegramMessage = False
cameraEnable = True
sendPhoto = False

print("Telegram bot is ready")

try:
    while True:

        lcd.move_to(0,0)
        lcd.putstr(" Everything OK  ")
        lcd.move_to(0,1)
        lcd.putstr("   Driver OK    ")
        time.sleep(0.4)


        if receiveTelegramMessage == True:
            receiveTelegramMessage = False

            statusText = ""
            
            #if(GPIO.input(37)==False):
                #bot.sendMessage(chat_id, "alcoholic")
                #capture()

            if telegramText == "/picam3":
                sendPhoto = True
                statusText = "Capturing photo..."
            else:
                statusText = "Command is not valid"

            sendTelegramMessage = True

        if sendTelegramMessage == True:
            sendTelegramMessage = False
            bot.sendMessage(chat_id, statusText)

        if sendPhoto == True:
            sendPhoto = False
            capture()

        if(GPIO.input(37)==False):
            lcd.clear()
            lcd.putstr("Alcoholic Driver")
            lcd.move_to(1,1)
            lcd.putstr("Sending Photo")
            bot.sendMessage(chat_id, "alcoholic driver detected")
            GPIO.output(40, GPIO.HIGH)
            GPIO.output(38, GPIO.HIGH)
            capture()
            lcd.clear()
        else:
            GPIO.output(40, GPIO.LOW)
            GPIO.output(38, GPIO.LOW)


except KeyboardInterrupt:
    camera.close()
    sys.exit(0)


GPIO.cleanup()
