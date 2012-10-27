import vector2 as v

class Camera:
    def __init__(self, x = 0, y = 0):
        self.position = v.Vector2(x, y)
        self.zoom = 1
        self.centered = False
        
    def center(self, body):
        self.centered = body

    def release(self):
        self.centered = False


class Renderer:
    def __init__(self, screen, pygame, camera, scale, width = 1300, height = 700):
        self.screen = screen
        self.pygame = pygame
        self.camera = camera
        self.scale = scale
        self.width = width
        self.height = height
        
        self.colors = {
            "black": self.pygame.Color(0, 0, 0),
            "white": self.pygame.Color(255, 255, 255),
            "red": self.pygame.Color(255, 0, 0),
            "green": self.pygame.Color(0, 255, 0),
            "earth": self.pygame.Color(45, 102, 73)
        }
        
    def toScreen(self, vector):
        np = [vector.x, vector.y]

        np[0] -= self.camera.position.x
        np[1] -= self.camera.position.y

        np[0] *= self.scale*self.camera.zoom
        np[1] *= self.scale*self.camera.zoom
        
        np[0] += self.width/2
        np[1] += self.height/2
        
        np[0] = int(np[0])
        np[1] = int(np[1])
         
        return np
        
    def getPos(self, body):
        return 
        
    def render(self, uni, ui):
        if self.camera.centered:
            self.camera.position.x = self.camera.centered.position.x
            self.camera.position.y = self.camera.centered.position.y

        self.screen.fill(self.colors["black"])
        
        for body in uni.bodies.itervalues():
            self.pygame.draw.circle(self.screen, self.colors[body.color], self.toScreen(body.position), int(body.r*self.scale*self.camera.zoom))    
        
        self.pygame.display.flip()
        
