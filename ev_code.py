#!/usr/bin/env python3
import random
from time import sleep
from action_thread import Action_Thread
from math import *
import sys, os

from ev3dev.ev3 import *
# from robot import *

rightMotor = LargeMotor(OUTPUT_B)
leftMotor = LargeMotor(OUTPUT_A)
actions = Action_Thread(rightMotor,leftMotor)
actions.start()

cs = ColorSensor()
# centimetres
ussr = UltrasonicSensor(INPUT_4)
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

def turn_left(dir = 1):
    global way
    way += dir
    if way < 0:
        way += 4
    way = way%4
    initial = gs.value()
    # motors are backwards
    leftMotor.run_direct(duty_cycle_sp=dir*25)
    rightMotor.run_direct(duty_cycle_sp=dir*-25)
    while abs(gs.value() - initial) < 80:
        sleep(0.05)

def stop():
    leftMotor.stop()
    rightMotor.stop()

def grab():
    actions.add_action('grabbing', 0, 0, 2)
    Sound.play('./Megalovania.wav')
    raise ZeroDivisionError

#rightMotor.run_direct(duty_cycle_sp=100)

Sound.tone(440, 300)

sleep(4)

#Sound.play('./Megalovania.wav')

x = 0
y = 0
way = 0
last_left = 0
last_right = 0

ways = [
    lambda x, y, move: (x, y + move),
    lambda x, y, move: (x + move, y),
    lambda x, y, move: (x, y - move),
    lambda x, y, move: (x - move, y)
]

intersections = []

def add_intersection(x, y, w):
    i = (x, y, w)
    intersections.append(i)

def near_intersection(x, y):
    return len([i for i in intersections if ((x - i[0])**2 + (y - i[1])**2)**0.5 < 20])

def sensor_state():
    return tuple(cs.value(i) for i in range(3))

def sees_white(cs_v=None):
    if (cs_v):
        return cs_v[0] > 18 and cs_v[1] > 18 and cs_v[2] > 18
    return cs.value(0) > 18 and cs.value(1) > 18 and cs.value(2) > 18

def sees_red(cs_v=None):
    if (cs_v):
        return cs_v[0] > 18 and cs_v[2] < 22
    return cs.value(0) > 18 and cs.value(2) < 22

while True:
    # GET MOVING-NESS
    cs_v = sensor_state()
    #print(cs_v)
    if sees_red(cs_v):
        grab()
    action = actions.current()
    if action:
        if action[1] == action[2]:
            left = leftMotor._full_travel_count
            right = rightMotor._full_travel_count
            if left and right:
                dleft, last_left = left - last_left, left
                dright, last_right = right - last_right, right
                move = dleft/2 + dright/2
                (x, y) = ways[way](x, y, move)
                Sound.tone(800, 100)
    # BORED STATE
    if not action:
        cs_v = sensor_state()
        if sees_red(cs_v):
            grab()
        elif not sees_white(cs_v):
            actions.add_action('forward', 40, 40, 0.2)
        else:
            if ussl.value() >= 200:
                turn_left(1)

            elif ussr.value() >= 20:
                turn_left(-1)

            else:
                turn_left(1)
                turn_left(1)
    # INTERSECTION STUFF
    s_l = ussl.value() / 10
    s_r = ussr.value()
    if s_l >= 20 or s_r >= 20:
        w = [0 for i in range(4)]
        w[way] = 1
        w[way-2] = 1
        if s_l >= 20:
            w[way-1] = 1
        elif s_r >= 20:
            w[way-3] = 1
        if not near_intersection(x, y):
            add_intersection(x, y, w)
            Sound.tone(220, 200)
            Sound.tone(220 * (2)**(1/12), 200)
            Sound.tone(220, 200)
            Sound.tone(220 * (2)**(1/12), 200)
    # WALL BUMP
    if sees_white():
        if s_l >= 20:
            turn_left(1)

        elif s_r >= 20:
            turn_left(-1)

        else:
            turn_left(1)
            turn_left(1)
