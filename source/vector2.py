import math
from decimal import *

class Vector2:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    #<operations>
    def iadd (self, v2):
        self.x += v2.x
        self.y += v2.y
        self.z += v2.z

    def add (self, v2):
        x = self.x + v2.x
        y = self.y + v2.y
        z = self.z + v2.z
        return Vector2(x, y, z)


    def isub (self, v2):
        self.x -= v2.x
        self.y -= v2.y
        self.z -= v2.z

    def sub (self, v2):
        x = self.x - v2.x
        y = self.y - v2.y
        z = self.z - v2.z
        return Vector2(x, y, z)


    def inormalize (self):
        tmp = self.length()
        self.x /= tmp
        self.y /= tmp
        self.z /= tmp

    def normalize (self):
        tmp = self.length()
        return Vector2(self.x/tmp, self.y/tmp)


    def ineg(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def neg(self):
        return Vector2(-self.x, -self.y, -self.z)


    def set (self, v2):
        self.x = v2.x
        self.y = v2.y
        self.z = v2.z


    def null(self):
        self.x = 0
        self.y = 0
        self.z = 0
    #</operations>


    def tl(self):
        return [self.x, self.y]

    def desc(self):
        return {"x": self.x, "y": self.y, "z": self.z}

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    #legacy:
    def l(self):
        return math.sqrt(self.x**2 + self.y**2)
