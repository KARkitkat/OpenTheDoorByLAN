import time
import socket

import machine
from machine import Pin
from machine import I2C
from machine import PWM
from ssd1306 import SSD1306_I2C

import network

ssid = "ssid"
passwd = "passwd"

p2 = Pin(2, Pin.OUT)  # create output pin on GPIO0

wf = network.WLAN(network.STA_IF)
wf.active(True)
i2c = I2C(scl=Pin(5), sda=Pin(4))
oled = SSD1306_I2C(128, 64, i2c)
servo = PWM(machine.Pin(14), freq=50)
servo_status=2


def show_status():
    oled.fill(0)
    oled.text("SSID:" + wf.config("essid"), 0, 0)
    oled.text("Status:" + str(wf.isconnected()), 0, 10)
    if servo_status ==1:
        oled.text("Servo On", 0, 20)
    elif servo_status==0:
        oled.text("Servo Off", 0, 20)
    oled.show()


def wifi_connect():
    p2.off()
    time.sleep_ms(50)
    p2.on()
    wf.connect(ssid, passwd)
    oled.fill(0)
    oled.text("wifi connecting", 0, 0)
    oled.show()
    time.sleep(3)

    if not wf.isconnected():
        wifi_connect()
    else:
        show_status()


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
    print("GOT a connection from %s" % str(addr))
    time.sleep_ms(200)
    request = conn.recv(2024)
    print("Content %s" % str(request))
    request = str(request)
    servo_on = request.find('/?servo=ON')
    servo_off = request.find('/?servo=OFF')
    print(servo_on,servo_off)

    if (servo_on == 6):
        servo.duty(125)
        servo_status=1
        show_status()

        time.sleep(2)

        servo.duty(25)
        servo_status = 0
        show_status()
    if (servo_off == 6):
        servo.duty(25)
        servo_status=0
        show_status()
    servo_status = 2
    show_status()
    # conn.send(b"HTTP/1.1 200 OK\r\n")
    conn.send(html)
    conn.close()
    machine.reset()




