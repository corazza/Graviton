import body

class Uni:
    def __init__(self, name, G, time=0):
        self.name = name
        self.G = G
        self.time = time
        
        self.bodies = {}
       
    def addBody (self, body, bid):
        body.id = bid
        self.bodies[bid] = body
        
    def removeBody (self, bid):
        pl = len(self.bodies)
        self.bodies = {bid: body for bid, body in self.bodies.iteritems() if body.id != bid}
        
        if pl != len(self.bodies):
            return True
        else:
            return False

    def desc (self):
        uni = {
            "name": self.name,
            "G": self.G,
            "time": self.time,
            "bodies": {bid: body.desc() for bid, body in self.bodies.iteritems()}
        }
        
        return uni

    def update (self, dt):
        self.time += dt
        
