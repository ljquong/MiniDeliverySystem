from machine import Pin
from time import sleep

reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)

while True:
    if reed_switch.value() == 1:
        led.on()
    else:
        led.off()
    sleep(0.5)