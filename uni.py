import body

class Uni:
    def __init__(self, name, G):
        self.name = name
        self.G = G
        
        self.cid = 0
        self.time = 0
        self.bodies = []
       
    def addBody (self, body):
        self.cid += 1
        body.id = self.cid
        self.bodies.append(body)

        return self.cid
        
    def removeBody (self, bid):
        pl = len(self.bodies)
        self.bodies = [body for body in self.bodies if body.id != bid]
        
        if pl != len(self.bodies):
            return True
        else:
            return False

    def update (self, dt):
        
        self.time += dt
        
