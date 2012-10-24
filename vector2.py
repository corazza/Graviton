class Vector2:
    def __init__(self, x, y):
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
    
    def rotate (self, rad):
        pass
    
    
    
