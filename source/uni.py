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
        self.name   = name
        self.G      = G
        self.time   = time

        self.nupdates       = 0
        self.description    = "Universe."
        self.bodies         = {}

    def addBody (self, body, bid):
        """Adds a body to the universe."""
        body.id             = bid
        self.bodies[bid]    = body

    def removeBody (self, bid):
        """Removes a body with body id 'bid' from the universe."""
        pl          = len(self.bodies)
        self.bodies = {bid: body for bid, body in self.bodies.iteritems() if body.id != bid}

        if pl != len(self.bodies):
            return True
        else:
            return False

    def getDate(self, dt=0):
        if self.datatime != "N/A" and not isinstance(dt, str):
            return time.asctime(time.localtime(self.datatime + self.time + dt))
        else:
            return "unknown"

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

    def fg(self, b1, b2):
        """Returns the gravitational force acting between two bodies as a Vector2."""

        difference  = b1.position.sub(b2.position)
        distance    = difference.length()
        fg          = (self.G * b1.m * b2.m) / (distance*distance)

        return Vector2(difference.x/distance * fg, difference.y/distance * fg, difference.z/distance * fg)

    def updateAccel(self):
        for b1, b2 in combinations(self.bodies.values(), 2):
            fg = self.fg(b1, b2) #Force vector.

            b1.force.iadd(fg.neg())
            b2.force.iadd(fg)

        for b in self.bodies.itervalues():
            b.acceleration.x = b.force.x/b.m
            b.acceleration.y = b.force.y/b.m
            b.acceleration.z = b.force.z/b.m
            b.force.null()

    def RK4(self, dt, stage):
        self.updateAccel()

        for b in self.bodies.itervalues():
            rd = b.rk4data

            if stage == 1:
                rd.px[0] = b.position.x
                rd.py[0] = b.position.y
                rd.pz[0] = b.position.z

                rd.vx[0] = b.velocity.x
                rd.vy[0] = b.velocity.y
                rd.vz[0] = b.velocity.z

                rd.ax[0] = b.acceleration.x
                rd.ay[0] = b.acceleration.y
                rd.az[0] = b.acceleration.z

            if stage == 2:
                rd.px[1] = rd.px[0] + 0.5*rd.vx[0]*dt
                rd.py[1] = rd.py[0] + 0.5*rd.vy[0]*dt
                rd.pz[1] = rd.pz[0] + 0.5*rd.vz[0]*dt

                rd.vx[1] = rd.vx[0] + 0.5*rd.ax[0]*dt
                rd.vy[1] = rd.vy[0] + 0.5*rd.ay[0]*dt
                rd.vz[1] = rd.vz[0] + 0.5*rd.az[0]*dt

                rd.ax[1] = b.acceleration.x
                rd.ay[1] = b.acceleration.y
                rd.az[1] = b.acceleration.z

            if stage == 3:
                rd.px[2] = rd.px[0] + 0.5*rd.vx[1]*dt
                rd.py[2] = rd.py[0] + 0.5*rd.vy[1]*dt
                rd.pz[2] = rd.pz[0] + 0.5*rd.vz[1]*dt

                rd.vx[2] = rd.vx[0] + 0.5*rd.ax[1]*dt
                rd.vy[2] = rd.vy[0] + 0.5*rd.ay[1]*dt
                rd.vz[2] = rd.vz[0] + 0.5*rd.az[1]*dt

                rd.ax[2] = b.acceleration.x
                rd.ay[2] = b.acceleration.y
                rd.az[2] = b.acceleration.z

            if stage == 4:
                rd.px[3] = rd.px[0] + rd.vx[2]*dt
                rd.py[3] = rd.py[0] + rd.vy[2]*dt
                rd.pz[3] = rd.pz[0] + rd.vz[2]*dt

                rd.vx[3] = rd.vx[0] + rd.ax[2]*dt
                rd.vy[3] = rd.vy[0] + rd.ay[2]*dt
                rd.vz[3] = rd.vz[0] + rd.az[2]*dt

                rd.ax[3] = b.acceleration.x
                rd.ay[3] = b.acceleration.y
                rd.az[3] = b.acceleration.z

            #Update the body's position for acceleration calculations:
            b.position.x = rd.px[stage-1]
            b.position.y = rd.py[stage-1]
            b.position.z = rd.pz[stage-1]

    def update (self, dt):
        """Pushes the uni 'dt' seconds forward in time."""

        for i in range(1, 5, 1):
            self.RK4(dt, i)

        for b in self.bodies.itervalues():
            rd = b.rk4data

            b.position.x = b.rk4data.px[0] + dt * (rd.vx[0] + 2*rd.vx[1] + 2*rd.vx[2] + rd.vx[3]) / 6.0
            b.position.y = b.rk4data.py[0] + dt * (rd.vy[0] + 2*rd.vy[1] + 2*rd.vy[2] + rd.vy[3]) / 6.0
            b.position.z = b.rk4data.pz[0] + dt * (rd.vz[0] + 2*rd.vz[1] + 2*rd.vz[2] + rd.vz[3]) / 6.0

            b.velocity.x = b.rk4data.vx[0] + dt * (rd.ax[0] + 2*rd.ax[1] + 2*rd.ax[2] + rd.ax[3]) / 6.0
            b.velocity.y = b.rk4data.vy[0] + dt * (rd.ay[0] + 2*rd.ay[1] + 2*rd.ay[2] + rd.ay[3]) / 6.0
            b.velocity.z = b.rk4data.vz[0] + dt * (rd.az[0] + 2*rd.az[1] + 2*rd.az[2] + rd.az[3]) / 6.0

        #Finish the update:
        self.time       += dt
        self.nupdates   += 1
        event.pub("update_done", self)
