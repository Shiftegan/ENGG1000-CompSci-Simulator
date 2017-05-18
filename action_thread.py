import threading
from time import sleep

class CanDetected(NameError):
    pass

class VeryCloseFront(NameError):
    pass

class Action_Thread(threading.Thread):
    def __init__(self):
        super.__init__()
        self.actions = []

    def _get_current_action(self):
        return False if not self.actions else self.actions[0]

    def check_sensors(self):
        # Add sensor conditions here
        pass

    def add_action(self, name, l, r, t, override = False):
        if override:
            self.actions = []
        self.actions.append((name, l, r, t))


    def execute_action(self, action):
        elapsed = 0
        name, rspeed, lspeed, time = action
        rightMotor.run_direct(duty_cycle_sp = rspeed)
        leftMotor.run_direct(duty_cycle_sp = lspeed)
        while elapsed < time:
            self.check_sensors()
            sleep(0.1)
            elapsed += 0.1

    def run(self):
        while True:
            try:
                if self.actions: self.execute_action(self.actions.pop(0))
            except CanDetected:
                pass
            except VeryCloseFront:
                pass

    currrent = property(_get_current_action, None)
