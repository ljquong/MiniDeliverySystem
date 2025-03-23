from machine import Pin, PWM
from time import sleep
from hcsr04 import HCSR04
from servo import Servo 

# motor a, LEFT motor
motor_a_in1 = Pin(6, Pin.OUT)
motor_a_in2 = Pin(7, Pin.OUT)
motor_a_en = PWM(Pin(8))
motor_a_en.freq(1000)
motor_a_correction = 1.0 # Adjust so both motors have same speed

# motor b, RIGHT motor
motor_b_in3 = Pin(4, Pin.OUT)
motor_b_in4 = Pin(3, Pin.OUT)
motor_b_en = PWM(Pin(2))
motor_b_en.freq(1000)
motor_b_correction = 1.0 # Adjust so both motors have same speed

line_sen = Pin(16, Pin.IN)

# front sensor
sensor_a = HCSR04(trigger_pin=21, echo_pin=20)
# back sensor
sensor_b = HCSR04(trigger_pin=19, echo_pin=18)

button = Pin(10, Pin.IN, Pin.PULL_DOWN)
reed_switch = Pin(0, Pin.IN, Pin.PULL_DOWN)

# LEFT servo
servo_a = Servo(Pin(22))
# RIGHT servo
servo_b = Servo(Pin(21))

# MUST TEST IR READ VALUES
ir = ADC(28)

# Function to control Motor A
def motor_a(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_a_correction)  # Apply correction
    if direction == "forward":
        motor_a_in1.value(0)
        motor_a_in2.value(1)
    elif direction == "backward":
        motor_a_in1.value(1)
        motor_a_in2.value(0)
    else:  # Stop
        motor_a_in1.value(0)
        motor_a_in2.value(0)
    motor_a_en.duty_u16(int(adjusted_speed * 65535 / 100))  # Speed: 0-100%

# Function to control Motor B
def motor_b(direction = "stop", speed = 0):
    adjusted_speed = int(speed * motor_b_correction)  # Apply correction
    if direction == "forward":
        motor_b_in3.value(1)
        motor_b_in4.value(0)
    elif direction == "backward":
        motor_b_in3.value(0)
        motor_b_in4.value(1)
    else:  # Stop
        motor_b_in3.value(0)
        motor_b_in4.value(0)
    motor_b_en.duty_u16(int(adjusted_speed * 65535 / 100))  # Speed: 0-100%
    
# robot starts in start-up area, facing black line, no obstacles
# move forward until black line is found, then turn to the right, begin while True

def find_black_line():
    # moves forward until black line is detected, then stop
    while True:
        motor_a("forward", 35)
        motor_b("backward", 35)
        sleep(0.1)
        if line_sen.value() == 0:
            motor_a()
            motor_b()
            break  
        # if black line is missed/if ultrasonic sensors detect obstacle, turn back around and look again?

def obstacle_maneuver():
    pass     

def obstacle_detection(direction = "front"):
    object_detected = False
    try:
        if direction == "front":
            distance = sensor_a.distance_cm()
        else:
            distance = sensor_b.distance_cm()
        #print(distance)
        if distance <= 15:
            object_detected = True
    except OSError as ex:
        print("ERROR getting distance:", ex)
    return object_detected

def payload_detection():
    object_detected = ""
    if button.value() == 1: 
        if reed_switch.value() == 1:
            object_detected = "payload"
        else:
            object_detected = "obstacle"
    return object_detected

def payload_pickup():
    while True:
        # move stepper down
        servo_a.move(90) # move to 90 degree position ('closed' position)
        servo_b.move(90)
        # move stepper up
        if reed_switch.value() == 1:
            # if reed switch still detects magnet, payload has successfully been picked up
            # end loop
            sleep(0.78)
            break
        else:
            # if payload has not successfully been picked up
            # identify most likely reasons for this, correct position
            # i.e. move forward slightly
            motor_a("forward", 35)
            motor_a("forward", 35)
            sleep(0.2)
            # loop continues until payload has been successfully picked up

def payload_retrieval():
    while True:
        motor_a("forward", 35)
        motor_b("forward", 35)
        sleep(0.5) #move forward ~13cm each time
        if obstacle_detection():
            motor_a("forward", 35)
            motor_b("forward", 35)
            sleep(0.5) #move forward ~14.75cm, more testing required
            if payload_detection() == "payload":
                payload_pickup()
                break
            else:
                obstacle_maneuver()
                break

def payload_delivery():
    while True:
        motor_a("forward", 35)
        motor_b("backward", 35)
        sleep (0.5)
        if ir.read_u16() == 1: # ARBITARY VALUE, MUST CHANGE
            # drop off area has been reached, turn 180 degrees and deposit payload
            motor_a("forward", 35)
            motor_b("backward", 35)
            sleep(0.78)
            # lower stepper platform, 'open' servo arms
            servo_a.move(0)
            servo_b.move(180)
            # raise stepper platform
            break
        if obstacle_detection(direction="back"):
            obstacle_maneuver()
            # must continue loop as drop off area has not yet been reached
        # turn back around 180 degrees to continue loop
        motor_a("forward", 35)
        motor_b("backward", 35)
        sleep(0.78)
            
# set servos to 'open' position
servo_a.move(0)
servo_b.move(180)

find_black_line()

# turn 180 degrees to the right
motor_a("forward", 35)
motor_b("backward", 35)
sleep(0.39)
# now on black line, facing retrieval area

while True:
    payload_retrieval()
    payload_delivery()
    
# moves approx 13cm at speed 35 for 0.5 seconds
# 90 degree turn at speed 35 for 0.39
# TO DO: obstacle maneuvering & going back to black line; stepper operation; making sure to stay on the black line