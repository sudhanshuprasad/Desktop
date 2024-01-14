from machine import Pin, I2C
import network
import urequests as requests
import BlynkLib
import utime
import math
from mpu6050 import init_mpu6050, get_mpu6050_data

left_led = Pin(15, Pin.OUT)
right_led = Pin(16, Pin.OUT)
front_led = Pin(17, Pin.OUT)
rear_led = Pin(14, Pin.OUT)

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
init_mpu6050(i2c)

# WiFi credentials
WIFI_SSID = "Hello"
WIFI_PASSWORD = "hello123"
 
# Blynk authentication token
BLYNK_AUTH = "lG0gWmmgkRVz0xde6nhMPcym9qy8vyBi"
 
 
# Connect to WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)
 
# Wait for the connection to be established
#while not wifi.isconnected():
    #sleep(1)
 
# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)
 
def calculate_tilt_angles(accel_data):
    x, y, z = accel_data['x'], accel_data['y'], accel_data['z']
 
    tilt_x = math.atan2(y, math.sqrt(x * x + z * z)) * 180 / math.pi
    tilt_y = math.atan2(-x, math.sqrt(y * y + z * z)) * 180 / math.pi
    tilt_z = math.atan2(z, math.sqrt(x * x + y * y)) * 180 / math.pi
 
    return tilt_x, tilt_y, tilt_z
 
def complementary_filter(pitch, roll, gyro_data, dt, alpha=0.98):
    pitch += gyro_data['x'] * dt
    roll -= gyro_data['y'] * dt
 
    pitch = alpha * pitch + (1 - alpha) * math.atan2(gyro_data['y'], math.sqrt(gyro_data['x'] * gyro_data['x'] + gyro_data['z'] * gyro_data['z'])) * 180 / math.pi
    roll = alpha * roll + (1 - alpha) * math.atan2(-gyro_data['x'], math.sqrt(gyro_data['y'] * gyro_data['y'] + gyro_data['z'] * gyro_data['z'])) * 180 / math.pi
 
    return pitch, roll
 
pitch = 0
roll = 0
prev_time = utime.ticks_ms()
 
while True:
    data = get_mpu6050_data(i2c)
    curr_time = utime.ticks_ms()
    dt = (curr_time - prev_time) / 1000
 
    tilt_x, tilt_y, tilt_z = calculate_tilt_angles(data['accel'])
    pitch, roll = complementary_filter(pitch, roll, data['gyro'], dt)
 
    prev_time = curr_time
 
    #gpio alert
    #y axis
    if tilt_y>45:
        left_led.on()
    else:
        left_led.off()

    if tilt_y<-45:
        right_led.on()
    else:
        right_led.off()

    #x axis
    if tilt_x>45:
        front_led.on()
    else:
        front_led.off()

    if tilt_x<-45:
        rear_led.on()
        requests.post("https://ntfy.sh/sleeping_driver",
            data="Movement detected by sensor",
            headers={
            "Title": "ALERT: Driver is sleepy",
            "Priority": "5",
            "Tags": "rotating_light",
            })
        print("Sleepy driver detected, notification sent")
        
    else:
        rear_led.off()

    print("Temperature: {:.2f} °C".format(data['temp']))
    print("Tilt angles: X: {:.2f}, Y: {:.2f}, Z: {:.2f} degrees".format(tilt_x, tilt_y, tilt_z))
    print("Pitch: {:.2f}, Roll: {:.2f} degrees".format(pitch, roll))
    print("Acceleration: X: {:.2f}, Y: {:.2f}, Z: {:.2f} g".format(data['accel']['x'], data['accel']['y'], data['accel']['z']))
    print("Gyroscope: X: {:.2f}, Y: {:.2f}, Z: {:.2f} °/s".format(data['gyro']['x'], data['gyro']['y'], data['gyro']['z']))
    
	# Send sensor data to Blynk
    blynk.virtual_write(0, (data['temp']))     # virtual pin 0 for temperature
    blynk.virtual_write(1, tilt_x)   # virtual pin 1 for Tilt angles X-axis
    blynk.virtual_write(2, tilt_y)   # virtual pin 2 for Tilt angles Y-axis
    blynk.virtual_write(3, tilt_z)   # virtual pin 3 for Tilt angles Z-axis
	# Run Blynk
    blynk.run()
	# Delay for 1 seconds
    utime.sleep(1)

