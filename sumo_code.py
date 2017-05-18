#!/usr/bin/env python3
from time import sleep
import random
from math import *
import sys, os

from ev3dev.ev3 import *

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

liftMotor = LargeMotor(OUTPUT_B)

# ts1 = TouchSensor(INPUT_1)
# ts4 = TouchSensor(INPUT_4)
us = UltrasonicSensor()
# gs = GyroSensor()

# gs.mode = "GYRO-ANG"

btn = Button()

lifted = False

def ram():
    rightMotor.run_direct(duty_cycle_sp=100)
    leftMotor.run_direct(duty_cycle_sp =100)

def turn(dir):
    rightMotor.run_direct(duty_cycle_sp=dir*-50)
    leftMotor.run_direct(duty_cycle_sp=dir*50)

def lift(time):
    liftMotor.run_direct(duty_cycle_sp=-50)
    lifted = True
    sleep(0.2)
    liftMotor.stop(stop_action="brake")

def wait_for_button():
    while not btn.any():
        pass

def run_code():
    while not btn.any():
        if us.value() < 700:
            ram()
        else:
            turn(1)


        if us.value() < 70 and not lifted:
            lift(500)
        else:
            liftMotor.stop(stop_action="coast")
            lifted = False

def shutdown():
    leftMotor.stop(stop_action="coast")
    rightMotor.stop(stop_action="coast")
    liftMotor.stop(stop_action="coast")

Sound.tone([(1000, 500, 500)])

while not btn.backspace:
    wait_for_button()
    Sound.tone([(1000, 500, 500)])
    sleep(3)
    run_code()
    shutdown()
