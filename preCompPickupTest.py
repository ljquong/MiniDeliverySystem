from machine import Pin, PWM
from time import sleep
from servo import Servo

# right servo
# closed position = 110
servo_a = Servo(Pin(22))

# left servo
# closed position = 10
servo_b = Servo(Pin(21))

# lift servo
# resting delivery (carrying) position = 90 degrees
# resting retrieval (lower) postion = 130
servo_c = Servo(Pin(20))

reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)

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
    sleep(0.5)

while True:
    motor_a("forward", 50)
    motor_b("backward", 51)
    sleep(0.1)
    if reed_switch.value() == 1:
        stop()
        # close servos
        servo_a.move(110)
        servo_b.move(10)
        sleep(0.5)
        servo_c.move(90)
        motor_a("forward", 50)
        motor_b("backward", 51)
        sleep(1)
        break
    
sleep(60)