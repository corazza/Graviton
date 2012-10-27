import sys, os
import ConfigParser

import pygame
from pygame.locals import *

import gfx
import fileManager
import ui

if len(sys.argv) < 2:
    raise Exception("World name not given!")

#<settings>
print "Graviton: Reading settings..."
config = ConfigParser.RawConfigParser()
config.read("settings.ini")

dt = config.getfloat("sim", "dt") #Delta-time for each step (in seconds).
x = config.getint("prog", "x")
y = config.getint("prog", "y")
scale = config.getfloat("prog", "scale")
unidir = os.getcwd() + "/" + config.get("prog", "unidir")
#</settings>


#<init>
print "Graviton: initializing..."
pygame.init()
screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Graviton - " + sys.argv[1])

s_icon = "images/icon.png"
icon = pygame.image.load(s_icon)
pygame.display.set_icon(icon)

m = fileManager.FileManager(unidir)
camera = gfx.Camera()
r = gfx.Renderer(screen, pygame, camera, scale)
uni = m.loadUni(sys.argv[1])
ui = ui.UI()

run = True

#</init>


#<main>
print "Graviton: Starting main loop."

while run:
    uni.update(dt)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
            
    r.render(uni, ui)

#</main>

m.saveUni(uni)

