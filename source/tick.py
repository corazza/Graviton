"""
repo: https://github.com/Yannbane/tick

Started on 09.05.2012. by Bane

This is a very simple Python module that gives the same functionality as the Javascript's setInterval and setTimeout functions. It offers both a realtime version, and a simulated time version.
"""

import time


#SIMULATION:

sim_timeouts = []
sim_intervals = []

class sim_Timeout:
    def __init__(self, f, after, start):
        self.after = after
        self.f = f
        self.startTime = start
        
        sim_timeouts.append(self)        

    def check(self, current):
        
        if (current - self.startTime >= self.after):
            self.f()
            sim_timeouts.pop(sim_timeouts.index(self))
            
    def reset(self, current):
        self.startTime = current


class sim_Interval:
    def __init__(self, f, i, start):
        self.i = i
        self.f = f
        
        self.startTime = start
        
        sim_intervals.append(self)        
        
    def check(self, current):
        if (current - self.startTime >= self.i):
            self.f()
            self.startTime = current + 1
            
    def reset(self, current):
        self.startTime = current


def sim_removeTimeout(i):
    if isinstance(i, simTimeout):
        sim_timeouts.pop(sim_timeouts.index(i))
    elif isinstance(i, int):
        sim_timeouts.pop(i)


def sim_removeInterval(i):
    if isinstance(i, sim_Interval):
        sim_intervals.pop(sim_intervals.index(i))
    elif isinstance(i, int):
        sim_intervals.pop(i)
        
def sim_checkIntervals(current):
    for i in sim_intervals:
        i.check(current)
            
def sim_checkTimeouts(current):
    for t in sim_timeouts:
        t.check(current)
            
def sim_check(current):
    sim_checkTimeouts(current)
    sim_checkIntervals(current)





#REALTIME:

timeouts = []
intervals = []

class Timeout:
    def __init__(self, f, after):
        self.after = after
        self.f = f
        
        self.startTime = time.time()
        
        timeouts.append(self)        
        
    def check(self):
        if (time.time() - self.startTime > self.after):
            self.f()
            timeouts.pop(timeouts.index(self))

    def reset(self):
        self.startTime = time.time()


class Interval:
    def __init__(self, f, i):
        self.i = i
        self.f = f
        
        self.startTime = time.time()
        
        intervals.append(self)        
        
    def check(self):
        if (time.time() - self.startTime > self.i):
            self.f()
            self.startTime = time.time()

    def reset(self):
        self.startTime = time.time()


def removeTimeout(i):
    if isinstance(i, Timeout):
        timeouts.pop(timeouts.index(i))
    elif isinstance(i, int):
        timeouts.pop(i)


def removeInterval(i):
    if isinstance(i, Interval):
        intervals.pop(intervals.index(i))
    elif isinstance(i, int):
        intervals.pop(i)


def checkIntervals():
    for i in intervals:
        i.check()
            
def checkTimeouts():
    for t in timeouts:
        t.check()
            
def check():
    checkTimeouts()
    checkIntervals()

