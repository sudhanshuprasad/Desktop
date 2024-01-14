from machine import Pin, I2C        #importing relevant modules & classes
import bme280        #importing BME280 library
import network
import time
import BlynkLib
import random
 
#i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)    #initializing the I2C method 
 
# WiFi credentials
WIFI_SSID = "Hello"
WIFI_PASSWORD = "hello123"
 
# Blynk authentication token
BLYNK_AUTH = "Gd2aLkg28vyur1wTjSQh6ghA6qS1CDtI"
 
 
# Connect to WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
 
# Wait for the connection to be established
while not wifi.isconnected():
    time.sleep(1)
 
# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)
 
# Run the main loop
while True:
    # Read BME280 sensor data
    #bme = bme280.BME280(i2c=i2c)
    #temperature, pressure, humidity = bme.read_compensated_data()
    temperature=24.33+random.randint(1,3)
    humidity=45.69+random.randint(0,10)
    pressure=980+random.randint(0,20)
 
    # Print sensor data to console
    print('Temperature: {:.1f} C'.format(temperature))
    print('Humidity: {:.1f} %'.format(humidity))
    print('Pressure: {:.1f} hPa'.format(pressure))
 
    # Send sensor data to Blynk
    blynk.virtual_write(0, temperature)  # virtual pin 1 for temperature
    blynk.virtual_write(1, humidity)    # virtual pin 2 for humidity
    blynk.virtual_write(2, pressure)   # virtual pin 3 for pressure
 
    # Run Blynk
    blynk.run()
 
    # Delay for 10 seconds
    time.sleep(5)