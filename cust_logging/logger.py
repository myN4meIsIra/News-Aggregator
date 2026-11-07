# logger
'''
    logger script for cust_logging
'''

import time

class Log():

    def __init__(self, file):
        self.file = file
        pass


    def time_now(self):
        return time.ctime()

    def log(self, text):
        print(f"{text} -- {self.file} -- {self.time_now()}")


    def error(self, text):
        print(f"***ERROR*** {text} -- {self.file} -- {self.time_now()}")
        quit()