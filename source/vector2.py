import math

class Vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y
        
    def add (self, v2):
        self.x += v2.x
        self.y += vy.y
        
    def sub (self, v2):
        self.x -= v2.x
        self.y -= vy.y
    
    def set (self, v2):
        self.x = v2.x
        self.y = v2.y
    
    def normalize (self):
        tmp = self.x + self.y
        self.x /= tmp
        self.y /= tmp

    def n_normalize (self):
        tmp = math.sqrt(self.x**2 + self.y**2)
        return Vector2(self.x/tmp, self.y/tmp)

    def tl(self):
        return [self.x, self.y]
        
    def l(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    def rotate (self, rad):
        pass
    
    def desc(self):
        return {"x": self.x, "y": self.y}
    
