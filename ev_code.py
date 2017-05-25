#!/usr/bin/env python3
from time import sleep
from time import time as get_time
import threading
from random import choice
# from action_thread import Action_Thread
# from math import *

from ev3dev.ev3 import *
# from robot import *
Sound.tone(110, 50)

rightMotor = LargeMotor(OUTPUT_B)
leftMotor = LargeMotor(OUTPUT_A)
grabMotor = MediumMotor(OUTPUT_D)


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




class Action_Thread(threading.Thread):
    def __init__(self, right, left, grab):
        super().__init__()
        self.actions = []
        self.right = right
        self.left = left
        self.grab = grab
        self.paused_actions = []
        self.paused = False

    def current(self):
        return False if not self.actions else self.actions[0]

    def check_sensors(self):
        global cs_v
        if sees_red(cs_v):
            self.pause()
            return True
        return False

    def pause(self):
        self.paused_actions = self.actions
        self.actions = []
        self.paused = True

    def resume(self):
        self.actions = self.paused_actions
        self.paused_actions = []
        self.paused = False

    def add_action(self, name, l, r, t, override = False, ignore_pause = False):
        if ignore_pause or not self.paused:
            if override:
                self.actions = []
            self.actions.append([name, l, r, t])
        else:
            if override:
                self.paused_actions = []
            self.paused_actions.append([name, l, r, t])


    def execute_action(self, action):
        initial = get_time()
        name, rspeed, lspeed, time = action
        self.right.run_direct(duty_cycle_sp = -rspeed)
        self.left.run_direct(duty_cycle_sp = -lspeed)
        while initial + time > get_time():
            if self.check_sensors():
                action[3] = get_time() - initial
                return
        if self.actions[0] == action:
            self.actions.pop(0)

    def run(self):
        while True:
            if self.actions: self.execute_action(self.actions[0])

actions = Action_Thread(rightMotor,leftMotor, grabMotor)
actions.start()

def sgn(x):
    return 1 if x > 0 else -1

def turn_by(angle, override=False, ignore_pause=False):
#    setMotors(-sgn(angle)*27, sgn(angle)*27)
#    leftMotor.run_direct(duty_cycle_sp=-sgn(angle)*27)
#    rightMotor.run_direct(duty_cycle_sp=sgn(angle)*27)
    phi = 0.0183
    actions.add_action('turning', -sgn(angle)*27, sgn(angle)*27, abs(angle)*phi, override, ignore_pause)
    return abs(angle) * phi

def turn_left(dir = 1):
    stop()
    actions.add_action('backup', -40, -40, 0.8, True)
    turn_by(90*dir)

def setMotors(l, r):
    leftMotor.run_direct(duty_cycle_sp=-l)
    rightMotor.run_direct(duty_cycle_sp=-r)

def stop():
    leftMotor.stop()
    rightMotor.stop()

def grab():
    print("starting grab...")
    grabMotor.run_direct(duty_cycle_sp=50)
    sleep(turn_by(180, True, True) + 0.5)
    actions.add_action('backup', -40, -40, 1, False, True)
    actions.add_action('stop', 0, 0, 1.5, False, True)
    sleep(3)
    print("grabbing...")
    grabMotor.run_direct(duty_cycle_sp=-50)
    sleep(1)
    grabMotor.stop(stop_action="hold")
    print("reversing...")
    actions.add_action('un-backup', 40, 40, 0.5, False, True)
    actions.add_action('stop', 0, 0, 0.5, False, True)
    sleep(1)
    sleep(turn_by(-180, False, True) + 0.5)
    print("grab complete...")

#rightMotor.run_direct(duty_cycle_sp=100)

Sound.tone(440, 100)
sleep(0.1)
Sound.tone(880, 100)

#Sound.play('./Megalovania.wav')

# x = 0`
# y = 0
# way = 0
# last_time` = get_time()
last_choice = get_time()

# ways = [
#     lambda x, y, move: (x, y + move),
#     lambda x, y, move: (x + move, y),
#     lambda x, y, move: (x, y - move),
#     lambda x, y, move: (x - move, y)
# ]
#
# intersections = []

def add_intersection(x, y, w):
    i = (x, y, w)
    intersections.append(i)

def near_intersection(x, y):
    return len([i for i in intersections if ((x - i[0])**2 + (y - i[1])**2)**0.5 < 15])



def sensor_state():
    return tuple(cs.value(i) for i in range(3))

def sees_white(cs_v=None):
    if (cs_v):
        return cs_v[0] > 30 and cs_v[1] > 30 and cs_v[2] > 30
    return cs.value(0) > 30 and cs.value(1) > 30 and cs.value(2) > 30

def sees_red(cs_v=None):
    if (cs_v):
        return cs_v[0] > 50 and cs_v[2] < 22
    return cs.value(0) > 50 and cs.value(2) < 22

# add_intersection(0, 0, [1, 1 if ussr.value() >= 20 else 0, 2, 1 if ussl.value()/10 >= 20 else 0])
# last_time = get_time()
# gs_prev = gs.value()
cs_v = sensor_state()

class Sensor_Update(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        global cs_v, sensor_state
        while True:
            cs_v = sensor_state()

sensor = Sensor_Update()
sensor.start()



while True:
    # GET MOVING-NESS
    # cs_v = sensor_state()
    # if sees_red(cs_v):
    #     grab()

    if actions.paused:
        grab()
        actions.resume()
    # cs_v = sensor_state()
    action = actions.current()
    s_l = ussl.value() / 10
    s_r = ussr.value()
    # if action: print(action[0], s_l, s_r)
    # else: print("no action")
    # Leds.set_color(Leds.LEFT, Leds.RED if s_l <= 13 else (Leds.AMBER if s_l <= 30 else Leds.GREEN))
    # Leds.set_color(Leds.RIGHT, Leds.RED if s_r <= 13 else (Leds.AMBER if s_r <= 30 else Leds.GREEN))
    if action and action[0] == 'forward':
            # move = dt * (left/2+right/2)
            # (x, y) = ways[way](x, y, move)

        if s_r <= 13:
            actions.add_action('us-correct', 50, 30, 0.1, True)
            #actions.add_action('forward', 35, 40, 0.1)
        elif s_l <= 13:
            actions.add_action('us-correct', 30, 50, 0.1, True)
            #actions.add_action('forward', 40, 35, 0.1)
            # print('correcting')
            # else:s("Didn't correct as values are {} and {}".format(s_l, s_r))


            #gs_curr = gs.value()
            #if abs(gs_curr - gs_prev) > 5 and n != "us-correct":
            #    actions.add_action('gyro-correct', 40 - 5*sgn(gs_curr - gs_prev), 40 + 5*sgn(gs_curr - gs_prev), 0.2, True)

            # print(abs(gs_curr - gs_prev))

        # else:
        #     print('Couldn\'t correct as name of action is:', n)

    # BORED STATE
    elif not action:

        if not sees_white(cs_v):
            actions.add_action('forward', 40, 40, 3)
    # INTERSECTION STUFF
    action = actions.current()
    # if action: print(action[0])
    if s_l >= 30 or s_r >= 30:
        # if not near_intersection(x, y):
        #     w = [0 for i in range(4)]
        #     w[way] = 1
        #     w[way-2] = 1
        #     if s_l >= 20:
        #         w[way-1] = 1
        #     elif s_r >= 20:
        #         w[way-3] = 1
        #     add_intersection(x, y, w)
        if (action and action[0] in ['forward', 'us-correct', 'gyro-correct']) and (get_time() - last_choice > 5):
            my_ways = ['forward']
            if s_l >= 30:
                my_ways.append('left')
            if s_r >= 30:
                my_ways.append('right')
            my_way = choice(my_ways)
            print('chose to go:', my_way)
            if my_way == 'forward':
                actions.add_action('crossing', 40, 40, 1.5, True)
            elif my_way == 'left' or my_way == 'right':
                actions.add_action('turn-prepping', 30, 30, 0.8, True)
                turn_by(-90 if my_way == 'left' else 90)
                actions.add_action('crossing', 40, 40, 0.5)
            Sound.tone(880, 20)
            last_choice = get_time()


    # WALL BUMP
    action = actions.current()
    print(cs_v, sees_white(cs_v))
    if sees_white(cs_v) and action and action[0] in ['forward', 'us-correct', 'gyro-correct', 'crossing', 'turn-prepping']:
        Sound.tone(110, 50)

        if s_l >= 20:
            turn_left(-1)

        elif s_r >= 20:
            turn_left(1)

        else:
            turn_left(2)
            # turn_left(1)
        last_choice = get_time()
