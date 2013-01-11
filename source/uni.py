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
        

    def update (self, dt):
        """Pushes the uni 'dt' seconds forward in time."""
    
        self.time += dt
        
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
            ax = b.force.x/b.m
            ay = b.force.y/b.m

            b.position.x += b.velocity.x*dt
            b.position.y += b.velocity.y*dt
            
            nvx = ax*dt
            nvy = ay*dt
            
            b.position.x += 0.5*nvx*dt
            b.position.y += 0.5*nvy*dt
            
            b.velocity.x += nvx
            b.velocity.y += nvy

            b.force.x = 0
            b.force.y = 0
            
