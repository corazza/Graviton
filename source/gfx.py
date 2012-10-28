import pygame

import vector2 as v
import ui as uim

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
    def __init__(self, screen, pygame, camera, width = 1300, height = 700):
        self.screen = screen
        pygame = pygame
        self.camera = camera
        self.width = width
        self.height = height
        
        self.scale = 1
        self.colors = {
            "black": pygame.Color(0, 0, 0),
            "white": pygame.Color(255, 255, 255),
            "red": pygame.Color(255, 0, 0),
            "green": pygame.Color(0, 255, 0),
            "earth": pygame.Color("#98cbfe"),
            "moon": pygame.Color(100, 100, 100),
            "mars": pygame.Color("#b22400")
        }
        
    def toScreen(self, vector):
        np = [vector.x, vector.y]

        np[0] -= self.camera.position.x
        np[1] -= self.camera.position.y

        np[0] *= self.camera.zoom
        np[1] *= self.camera.zoom
        
        np[0] += self.width/2
        np[1] += self.height/2
        
        np[0] = int(np[0])
        np[1] = int(np[1])
        
        return np
                
    def render(self, uni, ui):
        if self.camera.centered:
            self.camera.position.x = self.camera.centered.position.x
            self.camera.position.y = self.camera.centered.position.y

        self.screen.fill(self.colors["black"])
        
        for body in uni.bodies.itervalues():
            pygame.draw.circle(self.screen, self.colors[body.color], self.toScreen(body.position), int(body.r*self.scale*self.camera.zoom))    
        
        for e in ui.elements.itervalues():
            if isinstance(e, uim.Button):
                self.screen.blit(e.images[e.state], (e.x, e.y))
            elif isinstance(e, uim.Text):
                self.screen.blit(e.text, (e.x, e.y))
            
            
                    
        pygame.display.flip()
        
