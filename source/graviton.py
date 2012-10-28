import sys
import os
import time
import ConfigParser

import pygame
from pygame.locals import *

import gfx
import fileManager
import ui as userinterface
import event
import tick

from body import *

if len(sys.argv) < 2:
    raise Exception("World name not given!")

#<settings>
print "Graviton: Reading settings..."
config = ConfigParser.RawConfigParser()
config.read("settings.ini")

dts = config.getfloat("sim", "dts") #Delta-time scale (2 means that the simulation will run 2 times the normal speed of the universe).
x = config.getint("prog", "x")
y = config.getint("prog", "y")
unidir = os.getcwd() + "/" + config.get("prog", "unidir")
ps = config.getint("prog", "ps")
ui_path = config.get("prog", "ui")
#</settings>






#<init>
print "Graviton: initializing..."
pygame.init()
pygame.display.set_caption("Graviton - " + sys.argv[1])

s_icon = "images/icon.png"
icon = pygame.image.load(s_icon)
pygame.display.set_icon(icon)

screen = pygame.display.set_mode((x, y))


m = fileManager.FileManager(unidir)
camera = gfx.Camera()
r = gfx.Renderer(screen, pygame, camera)
uni = m.loadUni(sys.argv[1])
ui = userinterface.UI()

#camera.center(uni.bodies["earth"])
camera.zoom = 0.000001
r.scale = ps

run = True
last = time.time()

ui.load(open("ui.json", "r").read(), ui_path)

#image_surf = pygame.image.load("myimage.bmp").convert()
#</init>








#<events>
def save():
    m.saveUni(uni)

event.sub("save", save)
#</events>


#<setup>
def update_info():
    time_info.setText("Time: " + str(int(uni.time/60/60)) + "h.")

time_info = userinterface.Text(10, y - 200)

update_info()

ui.addElement(time_info, "time")

tick.Interval(update_info, 0.1)
#</setup>

#<main>

print "Graviton: starting."

while run:
    dt = time.time() - last
    last = time.time()
    
    uni.update(dt*dts)

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == MOUSEBUTTONDOWN:
            ui.down(pygame.mouse.get_pos())
        if event.type == MOUSEBUTTONUP:
            ui.up(pygame.mouse.get_pos())
            
    r.render(uni, ui)
    tick.check()

#</main>

