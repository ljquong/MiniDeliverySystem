from machine import Pin, ADC
from time import sleep

ir = ADC(28)
led = Pin('LED', Pin.OUT)

while True:
    if ir.read_u16() > 2300:
        led.on()
    else:
        led.off()
    sleep(0.1)
