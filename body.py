from vector2 import *

class Body:
    def __init__(self, m, r):
        self.m = m
        self.r = r
        
        self.id = ""
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        
