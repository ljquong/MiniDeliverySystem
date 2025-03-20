from machine import Pin
from time import sleep

button = Pin(10, Pin.IN, Pin.PULL_DOWN)
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
led = Pin('LED', Pin.OUT)

# when limit switch detects an object, reed switch checks if it is a payload
# if it is, the built in LED will turn on

while True:
    if button.value() == 1:
        print("Button pressed, OBJECT detected")
        if reed_switch.value() == 1:
            print("Reed switch activated, PAYLOAD detected")
            led.on()
        else:
            print("Object is not payload")
            led.off()
    else:
        print("No object detected")
        led.off()
    time.sleep(1)