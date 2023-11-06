import time


class Timer:
    def __init__(self, sec=1, auto_reboot=True):
        self.sec = sec
        self.auto_reboot = auto_reboot
        self.start_time = None
        self.active = False

    def __call__(self, *args, **kwargs):
        if time.time() - self.start_time > self.sec:
            self.active = True
            if self.auto_reboot:
                self.reboot()
                return True
        return self.active

    def run(self):
        self.start_time = time.time()
        return self

    def reboot(self, sec=None):
        if sec:
            self.sec = sec
        self.active = False
        self.run()


class FuncTimer(Timer):
    def __init__(self, func, sec=1, auto_reboot=True):
        super().__init__(sec, auto_reboot)
        self.func = func

    def __call__(self, *args, **kwargs):
        result = super().__call__( *args, **kwargs)
        if result:
            self.func()
        return result
