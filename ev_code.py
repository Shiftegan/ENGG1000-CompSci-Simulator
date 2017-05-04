#!/usr/bin/env python3
from time import sleep
import random
from math import *
import sys, os

# from ev3dev.ev3 import *
from robot import *

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

ts1 = TouchSensor(INPUT_1)
ts4 = TouchSensor(INPUT_4)
us = UltrasonicSensor()
gs = GyroSensor()

# gs.mode = "GYRO-ANG"

btn = Button()

def go_forward(time = None, dir = 1):
    rightMotor.run_direct(duty_cycle_sp=dir * 50)
    leftMotor.run_direct(duty_cycle_sp =dir * 50)
    if time: sleep(time)

def turn_left(dir = 1):
    gs.value()
    total = 0
    rightMotor.run_direct(duty_cycle_sp=dir*-10)
    leftMotor.run_direct(duty_cycle_sp=dir*10)
    while total <= 3.1415/2:
        sleep(0.05)
        total += abs(gs.value())

def stop():
    leftMotor.stop()
    rightMotor.stop()

def go_in_maze():
    time_going_forwards = 0
    while not (ts1.value() or ts4.value()):
        if us.value() >= 40:
            print("turning")
            stop()
            go_forward(0.1)
            turn_left()
            go_forward(0.3)
            go_in_maze()
            go_forward(0.3, -1)
            turn_left(-1)
        go_forward()
        sleep(0.1)
        time_going_forwards += 0.1
    print("sensor hit", time_going_forwards)
    go_forward(0.1, -1)
    turn_left(-1)

while True:
    go_in_maze()
