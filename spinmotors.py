#!/usr/bin/env python3
import random
from ev3dev.ev3 import *
from time import sleep

rightMotor = LargeMotor(OUTPUT_A)
leftMotor = LargeMotor(OUTPUT_D)
btn = Button()
while not btn.any():
    Sound.speak(" ".join([chr(64+random.randint(1, 26)) for i in range(20)]))
    sleep(5)
