#!/usr/bin/env python3
import random
from time import sleep
from action_thread import Action_Thread
from math import *
import sys, os

from ev3dev.ev3 import *
# from robot import *

actions = Action_Thread().start()
rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)

cs = ColorSensor()
# centimetres
ussr = UltrasonicSensor(INPUT_2)
# millimetres
ussl = UltrasonicSensor(INPUT_3)
gs = GyroSensor()

gs.mode = "GYRO-ANG"
cs.mode = "RGB-RAW"

btn = Button()
#
# def go_forward(time = None, dir = 1):
#     rightMotor.run_direct(duty_cycle_sp=dir * 50)
#     leftMotor.run_direct(duty_cycle_sp =dir * 50)
#     if time: sleep(time)
#
# def spin_right(time):
#     leftMotor.run_direct(duty_cycle_sp=25)
#     rightMotor.run_direct(duty_cycle_sp=-25)
#     sleep(time)
#
# def turn_left(dir = 1):
#     initial = gs.value()
#     leftMotor.run_direct(duty_cycle_sp=dir*-25)
#     rightMotor.run_direct(duty_cycle_sp=dir*25)
#     while abs(gs.value() - initial) < 76:
#         sleep(0.05)
#
# def stop():
#     leftMotor.stop()
#     rightMotor.stop()

def grab():
    actions.add_action('grabbing', 0, 0, 2)
    pass

Sound.tone(440, 300)

sleep(4)

Sound.play('./Megalovania.wav')

x = 0
y = 0
way = 0
last_left = 0
last_right = 0

ways = [
    lambda move: y += move,
    lambda move: x += move,
    lambda move: y -= move,
    lambda move: x -= move
]

intersections = []

def add_intersection(x, y, w):
    i = (x, y, w)
    intersections.append(i)

def near_intersection(x, y):
    return len([i for i in intersections if ((x - i[0])**2 + (y - i[1])**2)**0.5 < 20])

while True:
    action = actions.current
    if action[1] == action[2]:
        left = leftMotor.full_travel_count
        right = rightMotor.full_travel_count
        dleft, last_left = left - last_left, left
        dright, last_right = right - last_right, right
        move = dleft/2 + dright/2
        ways[way](move)
    if not action:
        if cs.value(0) > 20 and cs.value(2) < 20:
            grab()
        elif not (if cs.value(0) > 30 and cs.value(1) > 30 and cs.value > 30):
            actions.add_action('forward', 20, 20, 0.2)
    if ussl.value() >= 200 or ussr.value() >= 20:
        w = [0 for i in range(4)]
        w[way] = 1
        w[way-2] = 1
        if ussl.value() >= 200:
            w[way-1] = 1
        elif ussr.value() >= 20:
            w[way-3] = 1
    if cs.value(0) > 30 and cs.value(1) > 30 and cs.value > 30:
        if ussl.value() >= 200:
            # space on our left
            # ROTATE LEFT IN PLACE

        elif ussr.value() >= 20:
            # space on our right
            # ROTATE RIGHT IN PLACE
