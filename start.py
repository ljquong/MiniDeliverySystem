from machine import Pin, PWM, ADC
from time import sleep
from hcsr04 import HCSR04
from servo import Servo

servo_a = Servo(Pin(22))
servo_b = Servo(Pin(21))
servo_c = Servo(Pin(20))

reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)
line_sen = Pin(26, Pin.IN)
ir = ADC(28)

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
    sleep(1)
    
def turn_right():
    motor_a("forward", 50) # right turn
    motor_b("forward", 50)
    sleep(0.3)
    stop()

def turn_left():
    motor_a("backward", 50) # left turn
    motor_b("backward", 50)
    sleep(0.32)
    stop()

def front_obstacle_maneuver():
    motor_a("backward", 45)
    motor_a("backward", 45)
    sleep(1)
    stop()
    turn_right()
    motor_a("forward", 45)
    motor_b("backward", 45)
    sleep(0.8)
    while True:
        motor_a("forward", 45)
        motor_b("backward", 45)
        sleep(0.1)
        if sensor_c.distance_cm() > 35: #obstacle passed
            motor_a("forward", 45)
            motor_b("backward", 45)
            sleep(0.4)
            stop()
            turn_left()
            break
    motor_a("forward", 45)
    motor_b("backward", 45)
    sleep(0.8)
    while True:
        motor_a("forward", 45)
        motor_b("backward", 45)
        sleep(0.1)
        if sensor_c.distance_cm() > 35: #obstacle passed
            motor_a("forward", 45)
            motor_b("backward", 45)
            sleep(0.4)
            stop()
            turn_left()
            break
    while True:
        motor_a("forward", 40)
        motor_b("backward", 40)
        sleep(0.1)
        if line_sen.value() == 0:
            stop()
            turn_right()
            break

def back_obstacle_maneuver():
    motor_a("forward", 45)
    motor_a("forward", 45)
    sleep(1)
    stop()
    turn_left()
    motor_a("forward", 45)
    motor_b("backward", 45)
    sleep(0.8)
    while True:
        motor_a("forward", 45)
        motor_b("backward", 45)
        sleep(0.1)
        if sensor_c.distance_cm() > 35: #obstacle passed
            motor_a("forward", 45)
            motor_b("backward", 45)
            sleep(0.4)
            stop()
            turn_left()
            break
    motor_a("forward", 45)
    motor_b("backward", 45)
    sleep(0.8)
    while True:
        motor_a("forward", 45)
        motor_b("backward", 45)
        sleep(0.1)
        if sensor_c.distance_cm() > 35: #obstacle passed
            motor_a("forward", 45)
            motor_b("backward", 45)
            sleep(0.4)
            stop()
            turn_left()
            break
    while True:
        motor_a("forward", 40)
        motor_b("backward", 40)
        sleep(0.1)
        if line_sen.value() == 0:
            stop()
            turn_left()
            break

# reset servos to lower, open position
servo_c.move(0)
servo_a.move(70)
servo_b.move(50)

while True:
    motor_a("forward", 45)
    motor_b("backward", 45)
    sleep(0.1)
    if line_sen.value() == 0:
        stop()
        turn_right()
        break

while True:
    motor_a("forward", 45)
    motor_b("backward", 45)
    sleep(0.1)
    if sensor_a.distance_cm() < 15: #object detected
        stop()
        motor_a("forward", 45)
        motor_b("backward", 45)
        sleep(0.5)
        stop()
        if reed_switch.value() == 1:
            # yay payload detected
            servo_a.move(110)
            servo_b.move(10)
            sleep(0.5)
            servo_c.move(120)
            break
        else:
            front_obstacle_maneuver
    # by the end of this loop the robot should have picked up the payload

while True:
    motor_a("backward", 45)
    motor_b("forward", 45)
    sleep(0.1)
    if sensor_b.distance_cm() < 15: #OBSTACLE detected
        stop()
        back_obstacle_maneuver()
        break
    # by the end of this loop the robot should be past the obstacle, wherever it is

while True:
    motor_a("backward", 45)
    motor_b("forward", 45)
    sleep(0.1)
    if ir.read_u16() > 2300: #DROP OFF AREA detected
        stop()
        turn_right()
        turn_right()
        # move forward slightly to ensure payload is fully in drop of area
        motor_a("forward", 45)
        motor_b("backward", 45)
        sleep(1)
        stop()
        sleep(0.5)
        servo_c.move(0)
        servo_a.move(70)
        servo_b.move(50)
        sleep(0.5)
        break
        # payload should be dropped off!
# for continuous course run put everything after start up to black line find in while true
