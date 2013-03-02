"""
Simulates a universe.

Measurement units:

[time] = s
[distance] = m
[mass] = kg
[velocity] = ms^-1
[acceleration] = ms^-2
"""

import math
import time
import random
from itertools import combinations

import body
from vector2 import *
import event

class Uni:
    def __init__(self, name, G, time=0):
        self.name = name
        self.G = G
        self.time = time

        self.description = "Universe."
        self.bodies = {}

    def addBody (self, body, bid):
        """Adds a body to the universe."""
        body.id = bid
        body.ax = 0
        body.ay = 0
        self.bodies[bid] = body

    def removeBody (self, bid):
        """Removes a body with body id 'bid' from the universe."""
        pl = len(self.bodies)
        self.bodies = {bid: body for bid, body in self.bodies.iteritems() if body.id != bid}

        if pl != len(self.bodies):
            return True
        else:
            return False

    def getDate(self):
        if self.datatime != "N/A":
            return time.asctime(time.localtime(self.datatime + self.time))
        else:
            return "When did I start?" + str(random.random())

    def desc (self):
        """Describes the universe (in a dictionary format) so that it can be saved to a JSON file."""
        uni = {
            "name": self.name,
            "G": self.G,
            "time": self.time,
            "bodies": {bid: body.desc() for bid, body in self.bodies.iteritems()},
            "description": self.description,
            "datatime": self.datatime
        }

        return uni

    def Fg(self, b1, b2):
        """Returns the gravitational force acting between two bodies as a Vector2."""

        a = abs(b1.position.x - b2.position.x)
        b = abs(b1.position.y - b2.position.y)

        r = math.sqrt(a*a + b*b)

        fg = (self.G * b1.m * b2.m) / pow(r, 2)

        return Vector2(a/r * fg, b/r * fg)

    def updateAccel(self):
        for b1, b2 in combinations(self.bodies.values(), 2):
            fg = self.Fg(b1, b2)

            if b1.position.x > b2.position.x:
                b1.force.x -= fg.x
                b2.force.x += fg.x
            else:
                b1.force.x += fg.x
                b2.force.x -= fg.x


            if b1.position.y > b2.position.y:
                b1.force.y -= fg.y
                b2.force.y += fg.y
            else:
                b1.force.y += fg.y
                b2.force.y -= fg.y

        for b in self.bodies.itervalues():
            b.acceleration.x = b.force.x/b.m
            b.acceleration.y = b.force.y/b.m
            b.force.null()

    def RK4(self, dt, stage):
        self.updateAccel()

        for b in self.bodies.itervalues():
            rd = b.rk4data

            if stage == 1:
                rd.px[0] = b.position.x
                rd.py[0] = b.position.y
                rd.vx[0] = b.velocity.x
                rd.vy[0] = b.velocity.y
                rd.ax[0] = b.acceleration.x
                rd.ay[0] = b.acceleration.y

            if stage == 2:
                rd.px[1] = rd.px[0] + 0.5*rd.vx[0]*dt
                rd.py[1] = rd.py[0] + 0.5*rd.vy[0]*dt
                rd.vx[1] = rd.vx[0] + 0.5*rd.ax[0]*dt
                rd.vy[1] = rd.vy[0] + 0.5*rd.ay[0]*dt
                rd.ax[1] = b.acceleration.x
                rd.ay[1] = b.acceleration.y

            if stage == 3:
                rd.px[2] = rd.px[0] + 0.5*rd.vx[1]*dt
                rd.py[2] = rd.py[0] + 0.5*rd.vy[1]*dt
                rd.vx[2] = rd.vx[0] + 0.5*rd.ax[1]*dt
                rd.vy[2] = rd.vy[0] + 0.5*rd.ay[1]*dt
                rd.ax[2] = b.acceleration.x
                rd.ay[2] = b.acceleration.y

            if stage == 4:
                rd.px[3] = rd.px[0] + rd.vx[2]*dt
                rd.py[3] = rd.py[0] + rd.vy[2]*dt
                rd.vx[3] = rd.vx[0] + rd.ax[2]*dt
                rd.vy[3] = rd.vy[0] + rd.ay[2]*dt
                rd.ax[3] = b.acceleration.x
                rd.ay[3] = b.acceleration.y

            b.position.x = rd.px[stage-1]
            b.position.y = rd.py[stage-1]

    def update (self, dt):
        """Pushes the uni 'dt' seconds forward in time."""

        for i in range(1, 5, 1):
            self.RK4(dt, i)

        for b in self.bodies.itervalues():
            rd = b.rk4data
            b.position.x = b.rk4data.px[0] + (dt/6.0)*(rd.vx[0] + 2*rd.vx[1] + 2*rd.vx[2] + rd.vx[3])
            b.position.y = b.rk4data.py[0] + (dt/6.0)*(rd.vy[0] + 2*rd.vy[1] + 2*rd.vy[2] + rd.vy[3])

            b.velocity.x = b.rk4data.vx[0] + (dt/6.0)*(rd.ax[0] + 2*rd.ax[1] + 2*rd.ax[2] + rd.ax[3])
            b.velocity.y = b.rk4data.vy[0] + (dt/6.0)*(rd.ay[0] + 2*rd.ay[1] + 2*rd.ay[2] + rd.ay[3])

        self.time += dt
        event.pub("update_done", self)
