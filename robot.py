from math import *
from lines import *

import draw

#Globals
INPUT_1 = (1,1,0)
INPUT_2 = (0,0,0)
INPUT_3 = (0,0,0)
INPUT_4 = (-1,1,0)

OUTPUT_A = (-1,0)
OUTPUT_B = None
OUTPUT_C = None
OUTPUT_D = (1,0)


#Motors
class LargeMotor():
    def __init__(self, pos):
        self.offx, self.offy = pos

        self.speed = 0
        self.run_time = 0
        self.state = False

        self.radius = 5
        self.position = 0

        robot.addMotor(self)

    def getX(self):
        return self.getPos()[0]

    def getY(self):
        return self.getPos()[1]

    def getPos(self):
        cx = robot.x + self.offx * robot.size
        cy = robot.y + self.offy * robot.size

        x = cos(-robot.angle) * (cx - robot.x) - sin(-robot.angle) * (cy - robot.y) + robot.x
        y = sin(-robot.angle) * (cx - robot.x) + cos(-robot.angle) * (cy - robot.y) + robot.y

        return x, y

    def getRelativePos(self):
        return sub(robot.pos, self.pos)

    def getSpeed(self, duty_cycle):
        duty_cycle = max(0, min(100, duty_cycle))
        self.speed = 10 * duty_cycle
        return self.speed

    def run_timed(self, speed_sp = 0, time_sp = 0, duty_cycle_sp = 0):
        self.speed = speed_sp
        self.run_time = time_sp
        if duty_cycle_sp:
            self.speed = self.getSpeed(duty_cycle_sp)
        self.state = "timed"

    def run_direct(self, speed_sp = 0, duty_cycle_sp = 0):
        self.speed = speed_sp
        if duty_cycle_sp:
            self.speed = self.getSpeed(duty_cycle_sp)
        self.state = "running"

    def stop(self, stop_command = "brake"):
        self.run_time = 0
        self.state = False

    def run(self, time):
        if self.state == "timed":
            self.run_time -= time
            if self.run_time <= 0:
                self.state = False
                self.speed = 0

    duty_cycle_sp = property(None, getSpeed)

    x = property(getX, None)
    y = property(getY, None)

    pos = property(getPos, None)

#Sensors
class Sensor():
    def __init__(self, pos=(0,0,0)):
        robot.addSensor(self)

    def getX(self):
        return self.getPos()[0]

    def getY(self):
        return self.getPos()[1]

    def getPos(self):
        cx = robot.x + self.offx * robot.size
        cy = robot.y + self.offy * robot.size

        x = cos(-robot.angle) * (cx - robot.x) - sin(-robot.angle) * (cy - robot.y) + robot.x
        y = sin(-robot.angle) * (cx - robot.x) + cos(-robot.angle) * (cy - robot.y) + robot.y

        return x, y

    def value(self):
        return None

    def draw(self):
        pass

    x = property(getX, None)
    y = property(getY, None)

    pos = property(getPos, None)

class LineSensor(Sensor):
    def __init__(self, pos=(0,0,0)):
        self.offx, self.offy, self.angle = pos
        self.length = 160

        robot.addSensor(self)

    def getLine(self):
        x,y = self.pos
        return (x, y), (sin(robot.angle + self.angle) * self.length + x, cos(robot.angle + self.angle) * self.length + y)

    def draw(self):
        poi = self.poi()
        if poi: draw.line(self.pos, self.poi(), "red")

    def poi(self):
        line = self.getLine()
        points = []
        for l in robot.walls:
            if distance(line[0], l[0]) < self.length + distance(*l):
                poi = intersection(line, l)
                if poi:
                    points.append(poi)
        #if not points:
        #    print('problem')
        return sorted(points, key = lambda x: distance(self.pos, x))[0] if points else False


class TouchSensor(LineSensor):
    def __init__(self, pos=(0,0,0)):
        super().__init__(pos)
        self.length = 5

    def draw(self):
        draw.line(*self.getLine())

    def value(self):
        poi = self.poi()
        if poi: return True
        else:   return False

class UltrasonicSensor(LineSensor):
    def draw(self):
        poi = self.poi()
        if poi:
            draw.line(self.pos, poi, "red")
        else:
            draw.line(*self.getLine())


    def value(self):
        poi = self.poi()
        if poi:
            return distance(self.pos, poi)
        else:
            return self.length

class GyroSensor(Sensor):
    def __init__(self, pos=(0,0,0)):
        super().__init__(pos)
        self.prevAng = 0
    def value(self):
        #a = robot.angle - self.prevAng
        #self.prevAng = robot.angle
        return robot.angle % (2 * pi)


class Button():
    def any(self):
        return False

#Dummies
class Sound():
    def tone(self, *args):
        pass

Sound = Sound()

class Leds():
    def __init__(self):
        self.RED = self.GREEN = self.RIGHT = self.LEFT = None
    def set_color(self, *args):
        pass

Leds = Leds()

#Robot
class Robot():
    def __init__(self, x, y, walls):
        self.x = x
        self.y = y

        self.walls = walls

        self.sensors = []
        self.motors = {"left": None, "right": None}

        self.angle = 0
        self.size = 8

    def draw(self):
        draw.circle((self.x, self.y), self.size)
        for sensor in self.sensors:
            sensor.draw()

    def move(self, d):
        self.x += sin(self.angle) * d
        self.y += cos(self.angle) * d

    def turn(self, a):
        self.angle += a

    def update(self):
        if self.motors["left"] and self.motors["right"]:
            left = self.motors["left"]
            right = self.motors["right"]

            if left.speed != right.speed:
                radius = (left.speed + right.speed)/(right.speed - left.speed)

                vector_to_wheel = sub(left.pos, self.pos)
                vector_to_center = mul(unit_vector(vector_to_wheel), radius*self.size)

                cx, cy = add(vector_to_center, self.pos)

                theta = (-1 if left.speed > right.speed else 1)*(abs(left.speed) + abs(right.speed))/16000 * pi

                self.turn(theta)
                self.x = cos(theta) * (robot.x - cx) - sin(theta) * (robot.y - cy) + cx
                self.y = sin(theta) * (robot.x - cx) + cos(theta) * (robot.y - cy) + cy
            else:
                self.move(left.speed/250)
            left.run(100)
            right.run(100)


    def addMotor(self, motor):
        if self.motors["left"]: self.motors["right"] = motor
        else: self.motors["left"] = motor

    def addSensor(self, sensor):
        self.sensors.append(sensor)

    def getPos(self):
        return (self.x, self.y)

    pos = property(getPos, None)

def setup(x, y, walls):
    global robot
    robot = Robot(x, y, walls)
    return robot


    # def turn(self, left, right, radius):`
    #     mid = midpoint(left.pos, right.pos)
    #     vector = mul(unit_vector(sub(right.pos, mid)), radius)
    #     point = add(mid, vector)
    #
    #     x = cos(pi/12) * (mid[0] - point[0]) - sin(pi/12) * (mid[1] - point[1]) + robot.x
    #     y = sin(pi/12) * (mid[0] - point[0]) + cos(pi/12) * (mid[1] - point[1]) + robot.y
    #
    #     robot.angle += pi/12
    #
    #     self.x = x + (mid[0] - robot.x)
    #     self.y = y + (mid[1] - robot.y)
    #
    #
    # def update(self):
    #     if self.motors:
    #         left = self.motors[0]
    #         right = self.motors[1]
    #
    #         leftpos = sqrt(left.offx ** 2 + left.offy ** 2)
    #         rightpos = sqrt(right.offx ** 2 + right.offy ** 2)
    #
    #         speed = right.speed + left.speed
    #         print(leftpos, rightpos, speed)
    #
    #         if speed:
    #             radius = (-leftpos * left.speed + rightpos * right.speed) / (speed)
    #             if radius == 0:
    #                 robot.move(speed/300)
    #             else:
    #                 robot.turn(left, right, radius)
    #         else:
    #             robot.turn(left, right, 0)
    #
    #         left.run(100)
    #         right.run(100)

    # def update(self):
    #     rotation = 0
    #     movement = 0
    #     for motor in self.motors:
    #         print(motor.state)
    #         if motor.state:
    #             print(motor.speed)
    #             rotation += distance((self.x, self.y), motor.pos) * sin(atan2(motor.y - self.y, motor.x - self.x) + self.angle + pi/2) * motor.speed/100000
    #             movement += motor.speed/500
    #             motor.run(100)
    #
    #     self.angle += rotation
    #     if rotation > 0.1:
    #         self.move(movement/rotation)
    #     else:
    #         self.move(movement)

    # def avg_point_force(*forces):
    #     magnitudes = 0
    #     avgpos = (0,0)
    #     avgforce = (0,0)
    #     for force in forces:
    #         avgpos = add(avgpos, mul(force["pos"], force["magnitude"]))
    #         avgforce = add(avgforce, force["direction"])
    #         magnitudes += force["magnitude"]
    #
    #     if magnitudes: pos = mul(avgpos, 1/(magnitudes * len(forces)))
    #     else: pos = (0,0)
    #     direction = mul(avgforce, 1/len(forces))
    #     magnitude = sqrt(direction[0]**2 + direction[1]**2)
    #     return {"pos": pos, "direction": direction, "magnitude": magnitude}

    # def update(self):
    #     # calculate vector of average force
    #     forces = []
    #     for motor in self.motors:
    #         forces.append(motor.getPointForce())
    #         motor.run(100)
    #     print(forces)
    #     if forces:
    #         final_force = avg_point_force(*forces)
    #         print(final_force)
    #         ratio = 250
    #         # apply vector force
    #         self.x += final_force["magnitude"] * cos(atan2(*final_force["direction"][::-1]))/ratio
    #         self.y += final_force["magnitude"] * sin(atan2(*final_force["direction"][::-1]))/ratio
    #
    #         torque = distance((0,0), final_force["pos"]) * final_force["magnitude"]/ratio
    #         print(torque)
    #         self.turn(torque)
