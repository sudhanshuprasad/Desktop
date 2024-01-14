import socket
from time import sleep
import network
import machine
from machine import Pin

# Set up the SSID and password for the WiFi network
ssid = 'IoTProject01'
password = 'PicoCar05122023'

# Initialize pins for controlling the motor
Motor_A_Forward = Pin(18, Pin.OUT)
Motor_A_Backward = Pin(19, Pin.OUT)
Motor_B_Forward = Pin(20, Pin.OUT)
Motor_B_Backward = Pin(21, Pin.OUT)

# Define functions for moving the motor in different directions
def Forward():
    Motor_A_Forward.value(1)
    Motor_B_Forward.value(0)
    Motor_A_Backward.value(0)
    Motor_B_Backward.value(1)
    
def Backward():
    Motor_A_Forward.value(0)
    Motor_B_Forward.value(1)
    Motor_A_Backward.value(1)
    Motor_B_Backward.value(0)

def Stop():
    Motor_A_Forward.value(0)
    Motor_B_Forward.value(0)
    Motor_A_Backward.value(0)
    Motor_B_Backward.value(0)

def Left():
    Motor_A_Forward.value(1)
    Motor_B_Forward.value(0)
    Motor_A_Backward.value(0)
    Motor_B_Backward.value(0)

def Right():
    Motor_A_Forward.value(0)
    Motor_B_Forward.value(0)
    Motor_A_Backward.value(0)
    Motor_B_Backward.value(1)

# Stop the motor initially
Stop()
    
def Connect():
    # Connect to the WiFi network
    red = network.WLAN(network.STA_IF)
    red.active(True)
    red.connect(ssid, password)
    while red.isconnected() == False:
        print('connecting ...')
        sleep(1)
    ip = red.ifconfig()[0]
    print(f'Connected with IP: {ip}')
    return ip
    
def open_socket(ip):
    # Create a socket for the web server to listen on
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def pagina_web():
    html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        
        
        </head>
        <body>
         
              <h1 style="text-align: center;">Raspberry Pi Pico W Wireless Car
              </body>
              <h6 style="text-align: center;">DIY Projects Lab
        <center>
        <form action="./Forward">
        <input type="submit" value="Forward" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"  />
        </form>
        <table><tr>
        <td><form action="./Left">
        <input type="submit" value="Left" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
        </form></td>
        <td><form action="./Stop">
        <input type="submit" value="Stop" style="background-color: #FF0000; border-radius: 50px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px" />
        </form></td>
        <td><form action="./Right">
        <input type="submit" value="Right" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
        </form></td>
        </tr></table>
        <form action="./Backward">
        <input type="submit" value="Backward" style="background-color: #04AA6D; border-radius: 15px; height:120px; width:120px; border: none; color: white; padding: 16px 24px; margin: 4px 2px"/>
        </form>
        </body>
        </html>
    """
    return str(html)
def serve(connection):
    while True:
        cliente = connection.accept()[0]
        peticion = cliente.recv(1024)
        peticion = str(peticion)
        try:
            peticion = peticion.split()[1]
        except IndexError:
            pass
        if peticion == '/Forward?':
            Forward()
        elif peticion =='/Left?':
            Left()
        elif peticion =='/Stop?':
            Stop()
        elif peticion =='/Right?':
            Right()
        elif peticion =='/Backward?':
            Backward()
        html = pagina_web()
        cliente.send(html)
        cliente.close()

try:
    ip = Connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()