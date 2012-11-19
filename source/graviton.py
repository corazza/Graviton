import sys
import os
import time
import ConfigParser

import pygame
from pygame.locals import *

import gfx
import fileManager
import ui as uim
import event
import tick

from body import *

if len(sys.argv) < 2:
    raise Exception("World name not given!")

#<settings>
config = ConfigParser.RawConfigParser()
config.read("settings.ini")

dts = config.getfloat("sim", "dts") #Delta-time scale (2 means that the simulation will run 2 times the normal speed of the universe).
cdt = config.getfloat("sim", "cdt") #Constant delta-time (better perfrmace, poorer presentation).
vardt = config.get("prog", "vardt") == "true"
x = config.getint("prog", "x")
y = config.getint("prog", "y")
unidir = os.getcwd() + "/" + config.get("prog", "unidir")
ps = config.getint("prog", "ps")
ui_path = config.get("prog", "ui")
cs = config.getint("prog", "cs")
zoom = config.getfloat("prog", "zoom")
#</settings>






#<init>
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
ui = uim.UI(uni, camera)

#camera.center(uni.bodies["earth"])
camera.zoom = zoom
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

infoEnabled = True

def disableInfo():
    global infoEnabled
    infoEnabled = False
    time_info.disable()
    description.disable()
    
def enableInfo():
    global infoEnabled
    infoEnabled = True
    time_info.enable()
    description.enable()



time_info = uim.Text(200, 20)
description = uim.Text(x/2, 20)
description.setText(uni.description)
description.x -= description.w/2


update_info()

ui.addElement(time_info, "time")
ui.addElement(description, "description")

tick.Interval(update_info, 0.1)
#</setup>

#<main>

# 3. On planet click, center on that planet and begin displaying info on it.
# > On space click, release the camera and stop displaying info on the planet (also release on c).
# 4. Statistics and improved integration.

while run:
    if vardt:
        dt = time.time() - last
        last = time.time()
    else:
        dt = cdt
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        if event.type == MOUSEBUTTONDOWN:
            ui.down(pygame.mouse.get_pos())

        if event.type == MOUSEBUTTONUP:
            ui.up(pygame.mouse.get_pos())


        if event.type == KEYUP and event.key == K_i:
            if infoEnabled:
                disableInfo()
            else:
                enableInfo()

        if event.type == KEYUP and event.key == K_n:
            if ui.namesEnabled:
                ui.disableNames()
            else:
                ui.enableNames()

        if event.type == KEYUP and event.key == K_v:
            if ui.vectorsEnabled:
                ui.disableVectors()
            else:
                ui.enableVectors()

        if event.type == KEYUP and event.key == K_c:
            camera.position.x = 0
            camera.position.y = 0
            

        if event.type == KEYUP and (event.key == K_q or event.key == K_e):
            camera.zooming = 1

        if event.type == KEYDOWN and event.key == K_q:
            camera.zooming = 1.01

        if event.type == KEYDOWN and event.key == K_e:
            camera.zooming = 0.99


        if event.type == KEYUP and event.key == K_u:
            if ui.enabled:
                ui.disable()
            else:
                ui.enable()


                
        if event.type == KEYDOWN and event.key == K_w:
            camera.velocity.y += -cs/camera.zoom
            
        if event.type == KEYDOWN and event.key == K_a:
            camera.velocity.x += -cs/camera.zoom

        if event.type == KEYDOWN and event.key == K_s:
            camera.velocity.y += cs/camera.zoom
        
        if event.type == KEYDOWN and event.key == K_d:
            camera.velocity.x += cs/camera.zoom
        

        if event.type == KEYUP and event.key == K_w:
            camera.velocity.y += cs/camera.zoom
            
        if event.type == KEYUP and event.key == K_a:
            camera.velocity.x += cs/camera.zoom

        if event.type == KEYUP and event.key == K_s:
            camera.velocity.y += -cs/camera.zoom
        
        if event.type == KEYUP and event.key == K_d:
            camera.velocity.x += -cs/camera.zoom


    camera.position.x += camera.velocity.x * dt
    camera.position.y += camera.velocity.y * dt
    camera.zoom *= camera.zooming

    uni.update(dt*dts)
    r.render(uni, ui)
    tick.check()

#</main>

