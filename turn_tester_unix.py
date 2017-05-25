#!/usr/bin/env python3
import random
from time import sleep, time
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

def avg(x):
    return sum(x)/len(x)

def get_alpha(delta, a, b):
    area = 1/2 * a * b * sin(delta* 3.1415927/180)
    opp = sqrt(a*a + b*b - 2 * a * b * cos(delta*3.1415927/180))
    h = 2*area/opp
    return acos(h/b)

def realign():
    sla = avg([ussl.value() for i in range(10)])
    sra = avg([ussr.value() for i in range(10)])
    leftMotor.run_direct(duty_cycle_sp=15)
    rightMotor.run_direct(duty_cycle_sp=-15)
    sleep(0.05)
    stop()
    slb = avg([ussl.value() for i in range(10)])
    srb = avg([ussr.value() for i in range(10)])
    delta = 4
    alpha1, alpha2 = get_alpha(delta, sla, slb), get_alpha(delta, sra, srb)
    l = [i for i in [alpha1, alpha2] if abs(i) < 10]
    angle = avg(l)
    turn_by(angle)

def sgn(x):
    return 1 if x > 0 else -1

def turn_by(angle):
    leftMotor.run_direct(duty_cycle_sp=-sgn(x)*20)
    rightMotor.run_direct(duty_cycle_sp=sgn(x)*20)
    sleep(angle/40)
    stop()

def turn_left_trig(dir = 1):
    turn_by(dir*90)
    realign()

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


while True:
    if btn.any():
        turn_by(90)
        Sound.tone(220, 100)
