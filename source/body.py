from vector2 import *

class Body:
    def __init__(self, name, m, r, color = "white"):
        self.name = name
        self.m = m
        self.r = r
        self.color = color
        
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        
    def desc(self):
        body = {
            "name": self.name,
            "m": self.m,
            "r": self.r,
            "color": self.color,
            "position": self.position.desc(),
            "velocity": self.velocity.desc()
        }
    
        return body
