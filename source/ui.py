import json
import pygame
import event

pygame.font.init()

font = pygame.font.Font(None, 36)

class Element:
    def __init__(self, etype, x, y):
        self.x = x
        self.y = y
        self.type = etype


class Button(Element):
    def __init__(self, event, x, y, images):
        Element.__init__(self, "button", x, y)
        self.event = event
        self.images = images
        self.w = self.images["active"].get_width()
        self.h = self.images["active"].get_height()
        
        self.state = "inactive"

class Text(Element):
    def __init__(self, x, y):
        Element.__init__(self, "text", x, y)

    def setText(self, text):
        self.text = font.render(text, 1, (200, 200, 200))
        


class UI:
    def __init__(self):
        self.elements = {}
        
    def addElement(self, e, eid):
        self.elements[eid] = e
        
    def load(self, string, path):
        """Loads a suite of UI elements described in a json string."""
        ui = json.loads(string)
        
        for e in ui.itervalues():
            if e["type"] == "button":
                imagei = pygame.image.load(path + e["inactive"]).convert()
                imagea = pygame.image.load(path + e["active"]).convert()

                self.addElement(Button(e["event"], e["x"], e["y"], {"inactive": imagei, "active": imagea}), e["id"])

    def down(self, pos):
        for e in self.elements.itervalues():
            if (pos[0] > e.x and pos[0] < e.x + e.w and pos[1] > e.y and pos[1] < e.y + e.h):
                e.state = "active"
        
    def up(self, pos):
        for e in self.elements.itervalues():
            e.state = "inactive"

            if (pos[0] > e.x and pos[0] < e.x + e.w and pos[1] > e.y and pos[1] < e.y + e.h):
                event.pub(e.event)                

