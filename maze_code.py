#!/usr/bin/env python3
from time import sleep
import random
from math import *
import sys, os

from ev3dev.ev3 import *
# from robot import *

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

# ts1 = TouchSensor(INPUT_1)
# ts4 = TouchSensor(INPUT_4)
cs = ColorSensor()
usf = UltrasonicSensor(INPUT_2)
usl = UltrasonicSensor(INPUT_3)
gs = GyroSensor()

gs.mode = "GYRO-ANG"
cs.mode = "RGB-RAW"

btn = Button()

def go_forward(time = None, dir = 1):
    rightMotor.run_direct(duty_cycle_sp=dir * 50)
    leftMotor.run_direct(duty_cycle_sp =dir * 50)
    if time: sleep(time)

def spin_right(time):
    leftMotor.run_direct(duty_cycle_sp=25)
    rightMotor.run_direct(duty_cycle_sp=-25)
    sleep(time)

def turn_left(dir = 1):
    initial = gs.value()
    leftMotor.run_direct(duty_cycle_sp=dir*-25)
    rightMotor.run_direct(duty_cycle_sp=dir*25)
    while abs(gs.value() - initial) < 76:
        sleep(0.05)

CLOSE = 30

def stop():
    leftMotor.stop()
    rightMotor.stop()

Sound.tone(440, 300)

left_turns = 0
right_turns= 0

while True:
    #col = cs.value()
    if cs.value(0) > 20 and cs.value(2) < 20:
        stop()
        Sound.tone(440, 300)
        sleep(0.2)
        Sound.tone(440*4/3, 300)
        sleep(0.2)
        Sound.tone(660, 300)
        sleep(0.2)
        Sound.tone(880, 300)
        break

    if usf.value() <= 200:
        Sound.tone(440, 300)
        if usl.value() <= 25:
            go_forward(0.2, -1)
            turn_left(-1)

        else:
            go_forward(0.2, -1)
            turn_left(1)

    elif usl.value() <= 20 and usf.value() > 200:
       #spin_right(0.3) 53029775
       go_forward(0.2)
    elif usl.value() <= CLOSE and usf.value() > 300:
        go_forward()
        sleep(0.2)
    elif usl.value() > CLOSE + 10:
        go_forward(0.4)
        turn_left(1)

        go_forward(2.5)
    else:
        pass
