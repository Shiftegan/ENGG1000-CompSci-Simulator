#!/usr/bin/env python3
from time import sleep
import random
from math import *
import sys, os

from robot import *

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

ts1 = TouchSensor(INPUT_1)
ts4 = TouchSensor(INPUT_4)
us = UltrasonicSensor()
gs = GyroSensor()

gs.mode = "GYRO-ANG"

btn = Button()

def start():
    rightMotor.run_direct(duty_cycle_sp=75)
    leftMotor.run_direct(duty_cycle_sp =75)

def backup():
    Sound.tone([(1000, 500, 500)] * 3)
    Leds.set_color(Leds.RIGHT, Leds.RED)
    Leds.set_color(Leds.LEFT,  Leds.RED)

    rightMotor.stop(stop_command="brake")
    leftMotor.stop(stop_command="brake")

    rightMotor.run_timed(speed_sp = -500, time_sp=1500)
    leftMotor.run_timed(speed_sp  = -500, time_sp=1500)

    while any(m.state for m in (leftMotor, rightMotor)):
        sleep(0.1)

    Leds.set_color(Leds.RIGHT, Leds.GREEN)
    Leds.set_color(Leds.LEFT,  Leds.GREEN)

def turn(dir):
    rightMotor.run_timed(speed_sp=dir*-750, time_sp=1250)
    leftMotor.run_timed(speed_sp=dir*750,   time_sp=1250)

    while any(m.state for m in (leftMotor, rightMotor)):
        sleep(0.1)

start()
while not btn.any():
    if ts1.value():
        backup()
        turn(1)
        start()

    if ts4.value():
        backup()
        turn(1)
        start()

    direction = gs.value() + random.random() * 0.4 - 0.2

    if direction > 2 + 0.1:
        rightMotor.duty_cycle_sp = 55
        leftMotor.duty_cycle_sp = 25
    elif direction < 2 -0.1:
        rightMotor.duty_cycle_sp = 25
        leftMotor.duty_cycle_sp = 55
    else:
        rightMotor.duty_cycle_sp = 75
        leftMotor.duty_cycle_sp = 75

    #distance = us.value();
    #if distance > 30:
    #    dc = 75
    #else:
    #    dc = 30

    #for m in (leftMotor, rightMotor):
    #    m.duty_cycle_sp = dc

    #print(rightMotor.position, leftMotor.position)
    sleep(0.001)

    rightMotor.stop()
    leftMotor.stop()
