import RPi.GPIO as GPIO		#import RPi.GPIO module

LED = 32
gas_sensor = 31			#pin no. as per BOARD, GPIO18 as per BCM
Switch_input = 29		#pin no. as per BOARD, GPIO27 as per BCM
GPIO.setwarnings(False) 	#disable warnings
GPIO.setmode(GPIO.BOARD)	#set pin numbering format
GPIO.setup(LED, GPIO.OUT)	#set GPIO as output
GPIO.setup(gas_sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Switch_input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    print("switch "+ str(GPIO.input(Switch_input))+"    gas "+ str(GPIO.input(gas_sensor)))
    print( int(GPIO.input(Switch_input)) or int(GPIO.input(gas_sensor)) )

    if( int(GPIO.input(Switch_input)) and int(GPIO.input(gas_sensor)) ):
        GPIO.output(LED,GPIO.LOW)
        print("led off")
    else:
        GPIO.output(LED,GPIO.HIGH)

