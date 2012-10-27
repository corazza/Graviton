class Element:
    def __init__(self, f, rect):
        self.f = f
        self.rect = []        

class UI:
    def __init__(self):
        self.elements = []
        
    def addElement(self, e):
        self.elements.append(e)
        
