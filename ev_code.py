#!/usr/bin/env python3
from time import sleep
import random
from math import *
import sys, os

from ev3dev.ev3 import *

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

# ts1 = TouchSensor(INPUT_1)
# ts4 = TouchSensor(INPUT_4)
us = UltrasonicSensor()
# gs = GyroSensor()

# gs.mode = "GYRO-ANG"

btn = Button()

def ram():
    rightMotor.run_direct(duty_cycle_sp=100)
    leftMotor.run_direct(duty_cycle_sp =100)

def turn(dir):
    rightMotor.run_direct(duty_cycle_sp=dir*-50)
    leftMotor.run_direct(duty_cycle_sp=dir*50)

while not btn.any():
    if us.value() < 100:
        ram()
    else:
        turn(1)
