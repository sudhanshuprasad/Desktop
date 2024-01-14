from machine import Pin, ADC
import utime
import BlynkLib
import network


# WiFi credentials
WIFI_SSID = "hello123"
WIFI_PASSWORD = "hello1234"
 
# Blynk authentication token
BLYNK_AUTH = "c1fdAvTuDF74F2Cr-KY3_TXUEIA9aKek"

# Connect to WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
 
# Wait for the connection to be established
while not wifi.isconnected():
    utime.sleep(1)
    print("Not Connected")

#blynk initialisation
blynk = BlynkLib.Blynk(BLYNK_AUTH)


led = Pin(25, Pin.OUT)
buz = Pin(5, Pin.OUT)
adc = ADC(26)

pir = Pin(4, Pin.IN, Pin.PULL_UP)

trigger = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)

def ultra():
    trigger.low()
    utime.sleep_us(2)
    trigger.high()
    utime.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = utime.ticks_us()
    while echo.value() == 1:
        signalon = utime.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    return distance

while True:
    distance = ultra()
    blynk.virtual_write(0, distance)
    
    if(distance<100 or pir.value()==0):
        led.value(1)
        buz.on()
        #print("on ho jaa")
    else:
        led.value(0)
        buz.off()
        #print("off ho jaa")
        
    print("The distance from object is ",distance,"cm")
    print(adc.read_u16())
    utime.sleep(2)