from machine import Pin, PWM, ADC
from time import sleep
from hcsr04 import HCSR04

motor_a_in1 = Pin(14, Pin.OUT)
motor_a_in2 = Pin(13, Pin.OUT)
motor_a_en = PWM(Pin(15))
motor_a_en.freq(1000)
motor_a_correction = 1.02

motor_b_in3 = Pin(4, Pin.OUT)
motor_b_in4 = Pin(3, Pin.OUT)
motor_b_en = PWM(Pin(2))
motor_b_en.freq(1000)
motor_b_correction = 0.92

led = Pin('LED', Pin.OUT)

# front sensor
sensor_a = HCSR04(trigger_pin=1, echo_pin=5)
# back sensor
sensor_b = HCSR04(trigger_pin=12, echo_pin=11)
# left sensor
sensor_c = HCSR04(trigger_pin=8, echo_pin=9)

def motor_a(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_a_correction)
    if direction == "forward":
        motor_a_in1.value(0)
        motor_a_in2.value(1)
    elif direction == "backward":
        motor_a_in1.value(1)
        motor_a_in2.value(0)
    else:
        motor_a_in1.value(0)
        motor_a_in2.value(0)
    motor_a_en.duty_u16(int(adjusted_speed * 65535 / 100))

def motor_b(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_b_correction)
    if direction == "forward":
        motor_b_in3.value(1)
        motor_b_in4.value(0)
    elif direction == "backward":
        motor_b_in3.value(0)
        motor_b_in4.value(1)
    else:
        motor_b_in3.value(0)
        motor_b_in4.value(0)
    motor_b_en.duty_u16(int(adjusted_speed * 65535 / 100))
    
def stop():
    motor_a()
    motor_b()
    sleep(1)
    
while True:
    motor_a("forward", 50)
    motor_b("backward", 51)
    sleep(0.1)
    if sensor_a.distance_cm() < 18: #obstacle detected
        stop()
        # turn right
        motor_a("forward", 50) # right turn
        motor_b("forward", 50)
        sleep(0.44)
        stop()
        break
while True:
    motor_a("forward", 50)
    motor_b("backward", 51)
    sleep(0.1)
    if sensor_c.distance_cm() > 100: #obstacle passed
        motor_a("forward", 50)
        motor_b("backward", 51)
        sleep(0.7)
        stop()
        # turn right
        motor_a("backward", 50) # left turn
        motor_b("backward", 50)
        sleep(0.409)
        stop()
        motor_a("forward", 50)
        motor_b("backward", 51)
        sleep(1)
        break
while True:
    motor_a("forward", 50)
    motor_b("backward", 51)
    sleep(0.1)
    if sensor_c.distance_cm() > 100: #obstacle passed
        motor_a("forward", 50)
        motor_b("backward", 51)
        sleep(0.7)
        stop()
        # turn right
        motor_a("backward", 50) # left turn
        motor_b("backward", 50)
        sleep(0.409)
        stop()
        break

led.on()
sleep(60)
