from machine import Pin
import utime
import network
import BlynkLib

led = Pin("LED", Pin.OUT)
light = Pin(16, Pin.OUT)
pir = Pin(28, Pin.IN, Pin.PULL_UP)
led.low()

# WiFi credentials
WIFI_SSID = "IoTHomeSafety"
WIFI_PASSWORD = "HomeSafety"
 
# Blynk authentication token
BLYNK_AUTH = "SCNSgPO1K_aE7nXpzN3bw-BoV8In47Dv"


red = network.WLAN(network.STA_IF)
red.active(True)
red.connect(WIFI_SSID, WIFI_PASSWORD)
while red.isconnected() == False:
    print('connecting ...')
    utime.sleep(1)
ip = red.ifconfig()[0]
print(f'Connected with IP: {ip}')


'''# Connect to WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# Wait for the connection to be established
while not wifi.isconnected():
    utime.sleep(1)
    print("Not Connected")
'''

blynk = BlynkLib.Blynk(BLYNK_AUTH)


led_state = False
previous_state=0
current_state=0
wait_time=0


utime.sleep(0.1)
while True:
    current_state=pir.value()
    if(pir.value()==True):
        print("yes")
        if(current_state!=previous_state):
            print("raised")
            led_state= not led_state
        led.value(True)

    else:
        print("no")
        if(current_state!=previous_state):
            print("fallen")
        led.value(False)
        
    print(wait_time)
    wait_time=wait_time+1
    if(wait_time>60):
        led_state=False
        wait_time=0
    
    print(led_state)
    light.value(led_state)
    blynk.virtual_write(0, led_state)
    
    previous_state=current_state
    utime.sleep(1)
