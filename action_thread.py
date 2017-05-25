import threading
from time import sleep

class Action_Thread(threading.Thread):
    def __init__(self, right, left, grab):
        super().__init__()
        self.actions = []
        self.right = right
        self.left = left
        self.grab = grab

    def current(self):
        return False if not self.actions else self.actions[0]

    def check_sensors(self):
        cs_v = sensor_state()
        if sees_red(cs_v):
            self.grab_can()

    def grab_can(self):
        old_actions = self.actions
        self.actions = []
        self.grab.run_direct(duty_cycle_sp=50)
        sleep(turn_by(180, True) + 0.5)
        self.add_action('backup', -40, -40, 1)
        self.add_action('stop', 0, 0, 1.5)
        sleep(3)
        self.grab.run_direct(duty_cycle_sp=-50)
        sleep(1)
        self.grab.stop(stop_action="hold")
        self.add_action('un-backup', 40, 40, 0.5)
        self.add_action('stop', 0, 0, 0.5)
        turn_by(-180)
        self.actions = old_actions

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
        global rightMotor, leftMotor
        self.right.run_direct(duty_cycle_sp = -rspeed)
        self.left.run_direct(duty_cycle_sp = -lspeed*1.03)
        while initial + time < get_time():
            self.check_sensors()


    def run(self):
        while True:
            if self.actions: self.execute_action(self.actions.pop(0))
