from machine import Pin
from time import sleep
from servo import Servo 

button = Pin(10, Pin.IN, Pin.PULL_DOWN)
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)

servo1 = Servo(Pin(22))
servo2 = Servo(Pin(21))

led = Pin('LED', Pin.OUT)

servo1.move(0)
servo2.move(180)

while True:
    
    if button.value() == 1: 
        print("Button pressed, OBJECT detected\n")
        if reed_switch.value() == 1:
            print("Reed switch activated, PAYLOAD detected\n")
            servo1.move(90) # move to 90 degree position ('closed' position)
            servo2.move(90)
            sleep(2)
            #led.on()
        else:
            print("Object is not payload\n")
            #led.off()
    else:
        print("No object detected\n")
        led.off()
    
    servo1.move(0) # 'open' position
    servo2.move(180)
    sleep(1) # Short delay
    
# button does not need to be pressed all the way
