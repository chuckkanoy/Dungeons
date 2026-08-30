import time

class Timer:
    # time is in seconds
    def __init__(self, timer_length):
        self.start_time = time.time()
        self.timer_length = timer_length

    def reset(self):
        self.start_time = time.time()
    
    def set_length(self, length):
        self.timer_length = length
    
    def is_expired(self):
        return time.time() - self.start_time >= self.timer_length