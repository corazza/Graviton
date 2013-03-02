import pygame
import math

import vector2 as v
import ui as uim
import util

class Camera:
    def __init__(self, x = 0, y = 0):
        self.position = v.Vector2(x, y)

        self.direction = 0
        self.zoom = 1
        self.zooming = 1
        self.centered = False

    def determineDirection(self, w, a, s, d):
        self.direction = 0
        moving = True

        if w:
            self.direction = 0

            if a:
                self.direction = -45

            elif d:
                self.direction = -315

        elif a:
            self.direction = -90

            if s:
                self.direction = -135

        elif s:
            self.direction = -180

            if d:
                self.direction = -225

        elif d:
            self.direction = -270

        else:
            moving = False

        self.direction += 360 - 90

        self.direction = 2 * math.pi * self.direction / 360

        return moving

    def center(self, body):
        self.centered = body

    def release(self):
        self.centered = False


class Renderer:
    def __init__(self, screen, pygame, camera, orbit_buffer, width = 1300, height = 700):
        self.screen = screen
        pygame = pygame
        self.camera = camera
        self.width = width
        self.height = height
        self.orbit_buffer = orbit_buffer

        self.scale = 1
        self.colors = {
            "black": pygame.Color(0, 0, 0),
            "white": pygame.Color(255, 255, 255),
            "red": pygame.Color(255, 0, 0),
            "blue": pygame.Color(50, 50, 255),
            "green": pygame.Color(0, 255, 0),
            "earth": pygame.Color("#98cbfe"),
            "moon": pygame.Color(100, 100, 100),
            "mars": pygame.Color("#b22400"),
            "orange": pygame.Color("#FF9900")
        }

        self.fonts = {
            "names": pygame.font.Font(None, 20)
        }

    def take_pos(self, uni):
        """Record the positions of objects for drawing orbits"""
        for body in uni.bodies.itervalues():
            body.previous_positions.append([body.position.x, body.position.y])

            diff = len(body.previous_positions) - self.orbit_buffer

            if diff > 0:
                body.previous_positions = body.previous_positions[diff:]

    def render(self, uni, ui):
        if self.camera.centered:
            self.camera.position.x = self.camera.centered.position.x
            self.camera.position.y = self.camera.centered.position.y

        self.screen.fill(self.colors["black"])

        for body in uni.bodies.itervalues():
            pygame.draw.circle(self.screen, self.colors[body.color], util.toScreen(body.position, self.camera), int(body.r*self.scale*self.camera.zoom))

        if ui.enabled:
            for body in uni.bodies.itervalues():
                if not len(body.previous_positions):
                    break

                positions = []

                for pos in body.previous_positions:
                    sp = util.toScreenXy([pos[0], pos[1]], self.camera)
                    positions.append(sp)

                while len(positions) < 2:
                    positions.append(util.toScreenXy([body.previous_positions[-1][0], body.previous_positions[-1][1]], self.camera))

                pygame.draw.lines(self.screen, self.colors["white"], False, positions)

            for e in ui.elements.itervalues():
                if not e.display:
                    continue

                if isinstance(e, uim.Button):
                    self.screen.blit(e.images[e.state], (e.x, e.y))
                elif isinstance(e, uim.Text):
                    self.screen.blit(e.text, (e.x, e.y))


            if ui.namesEnabled:
                for body in uni.bodies.itervalues():
                    name = self.fonts["names"].render(body.name, 1, (240, 240, 240))
                    pos = util.toScreen(body.position, self.camera)
                    size = self.fonts["names"].size(body.name)
                    pos[0] -= size[0]/2
                    pos[1] -= size[1] + body.r*self.camera.zoom*2
                    self.screen.blit(name, pos)

            if ui.vectorsEnabled:
                for body in uni.bodies.itervalues():
                    pos = util.toScreen(body.position, self.camera)
                    vel = body.velocity.tl()

                    r = 0.005

                    end = [int(pos[0] + vel[0]*r), int(pos[1] + vel[1]*r)]

                    pygame.draw.line(self.screen, self.colors["white"], pos, end)
                    pygame.draw.circle(self.screen, self.colors["white"], end, 1)

                    text = "v = " + str(int(body.velocity.l())) + "m/s"
                    v = self.fonts["names"].render((text), 1, (240, 240, 240))
                    pos = [(pos[0] + end[0])/2 + 10, (pos[1] + end[1])/2 + 10]
                    self.screen.blit(v, pos)


        pygame.display.flip()
