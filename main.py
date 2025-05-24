import time
import socket

import machine
from machine import Pin
from machine import I2C
from machine import PWM

import network

ssid = "ssid"
passwd = "password"

p2 = Pin(2, Pin.OUT)  # create output pin on GPIO0

wf = network.WLAN(network.STA_IF)
wf.active(True)
i2c = I2C(scl=Pin(5), sda=Pin(4))
servo = PWM(machine.Pin(14), freq=50)
servo_status=2

def wifi_connect():
    p2.off()
    time.sleep_ms(50)
    p2.on()
    wf.connect(ssid, passwd)
    time.sleep(3)

    if not wf.isconnected():
        wifi_connect()
    else:
        print()


wifi_connect()

html = '''<!DOCTYPE html>
<html>
<head><meta charset='UTF-8'><title>网络servo开关服务器</title></head>
<center><h2>网络servo开关服务器</h2></center>
<center><form>
<button name="servo" value='ON' type='submit'> servo ON </button>
<button name="servo" value='OFF' type='submit'> servo OFF </button>
</form>
</center></html>
'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    p2.off()
    time.sleep_ms(50)
    p2.on()
    conn, addr = s.accept()
    time.sleep_ms(200)
    request = conn.recv(2024)
    request = str(request)
    servo_on = request.find('/?servo=ON')
    servo_off = request.find('/?servo=OFF')
    servo_keepon = request.find('/?servo=keepon')

    if (servo_on == 6):
        servo.duty(125)
        servo_status=1

        time.sleep(3)

        servo.duty(25)
        servo_status = 0
    if (servo_off == 6):
        servo.duty(25)
        servo_status=0
    if (servo_keepon == 6):
        servo.duty(125)
        servo_status=0
    servo_status = 2
    # conn.send(b"HTTP/1.1 200 OK\r\n")
    conn.send(html)
    conn.close()
    machine.reset()