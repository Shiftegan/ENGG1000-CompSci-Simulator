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
grabMotor = MediumMotor(OUTPUT_D)
actions = Action_Thread(rightMotor,leftMotor)
actions.start()

cs = ColorSensor()
# centimetres
ussr = UltrasonicSensor(INPUT_4)
# millimetres
ussl = UltrasonicSensor(INPUT_3)
# gs = GyroSensor()

# gs.mode = "GYRO-ANG"
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
    print('area', area)
    opp = sqrt(a*a + b*b - 2 * a * b * cos(delta*3.1415927/180))
    h = 2*area/opp
    print('h', h)
    error_angle = acos(h/b) * 180/3.1415927
    print('e', error_angle)
    return error_angle

def realign():
    sla = avg([ussl.value() for i in range(30)])
    print(sla)
    #sra = avg([ussr.value() for i in range(10)])
    delta = 16
    turn_by(delta)
    #stop()
    slb = avg([ussl.value() for i in range(30)])
    print(slb)
    #srb = avg([ussr.value() for i in range(10)])
    alpha1 = get_alpha(delta, sla, slb)
    #alpha2 = get_alpha(delta, sra, srb)
    #l = [i for i in [alpha1, alpha2] if abs(i) < 10]
    l = [alpha1]
    angle = avg(l)
    turn_by(-angle)

def sgn(x):
    return 1 if x > 0 else -1

def turn_by(angle):
    leftMotor.run_direct(duty_cycle_sp=-sgn(angle)*27)
    rightMotor.run_direct(duty_cycle_sp=sgn(angle)*27)
    phi = 0.018
    sleep(abs(angle)*phi)
    stop()


# def turn_left(dir = 1):
#     global way
#     way += dir
#     if way < 0:
#         way += 4
#     way = way%4
#     initial = gs.value()
#     # motors are backwards
#     leftMotor.run_direct(duty_cycle_sp=dir*25)
#     rightMotor.run_direct(duty_cycle_sp=dir*-25)
#     while abs(gs.value() - initial) < 80:
#         sleep(0.05)

def stop():
    leftMotor.stop()
    rightMotor.stop()

def setMotors(l, r):
    leftMotor.run_direct(duty_cycle_sp=-l)
    rightMotor.run_direct(duty_cycle_sp=-r)

def grab():
    grabMotor.run_direct(duty_cycle_sp=50)
    turn_by(180)
    setMotors(-40, -40)
    sleep(0.5)
    stop()
    grabMotor.run_direct(duty_cycle_sp=-50)
    sleep(0.4)
    grabMotor.stop(stop_action="hold")
    sleep(1)
    setMotors(40, 40)
    sleep(0.5)
    stop()
    turn_by(-180)
    #actions.add_action('grabbing', 0, 0, 2)
    #Sound.play('./Megalovania.wav')
    #raise ZeroDivisionError

#rightMotor.run_direct(duty_cycle_sp=100)

Sound.tone(110, 300)

def sees_red(cs_v=None):
    if (cs_v):
        return cs_v[0] > 18 and cs_v[2] < 22
    return cs.value(0) > 18 and cs.value(2) < 22

while True:
    if btn.any():
        for i in range(8):
            turn_by(90)
            Sound.tone(220, 100)
            sleep(1)
    if sees_red():
        grab()
