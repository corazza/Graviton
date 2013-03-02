from vector2 import *

class RK4Data:
    def __init__(self):
        self.px = [0,0,0,0]
        self.py = [0,0,0,0]
        self.vx = [0,0,0,0]
        self.vy = [0,0,0,0]
        self.ax = [0,0,0,0]
        self.ay = [0,0,0,0]


class Body:
    def __init__(self, name, m, r, color = "white"):
        self.name = name
        self.m = m
        self.r = r
        self.color = color

        self.rk4data = RK4Data()
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.force = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.previous_positions = []

    def desc(self):
        body = {
            "name": self.name,
            "m": self.m,
            "r": self.r,
            "color": self.color,
            "position": self.position.desc(),
            "velocity": self.velocity.desc(),
        }

        return body
