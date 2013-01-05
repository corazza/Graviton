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
zcps = config.getfloat("prog", "zcps") #Zoom change per second
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

camera.zoom = zoom
r.scale = ps

run = True
last = time.time()

def update_time_info(el):
    el.setText("Time: " + str(int(uni.time/60/60)) + "h.")

def update_zoom_info(el):
    el.setText("Zoom: " + str(camera.zoom) + ".")
    
def set_desc(el):
    el.setText(uni.description)
    el.x = x/2 - el.w/2

ui.addSetter("desc", set_desc)
ui.addUpdate("time", update_time_info)
ui.addUpdate("zoom", update_zoom_info)

ui.load(open("ui.json", "r").read(), ui_path)

tick.Interval(ui.update, 0.1)


infoEnabled = True

def disableInfo():
    global infoEnabled
    infoEnabled = False
    ui.getElement("time").disable()
    ui.getElement("zoom").disable()
    
def enableInfo():
    global infoEnabled
    infoEnabled = True
    ui.getElement("time").enable()
    ui.getElement("zoom").enable()


keys = {
    "e": False,
    "q": False,
    "w": False,
    "a": False,
    "s": False,
    "d": False,
}
#</init>








#<events>
def save():
    m.saveUni(uni)

event.sub("save", save)
#</events>



#<setup>

#</setup>



#<main>

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
            

        if event.type == KEYDOWN and event.key == K_q:
            keys["q"] = True

        if event.type == KEYDOWN and event.key == K_e:
            keys["e"] = True

        if event.type == KEYUP and event.key == K_q:
            keys["q"] = False

        if event.type == KEYUP and event.key == K_e:
            keys["e"] = False


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


    if keys["e"]:
        camera.zoom += zcps*camera.zoom*dt - camera.zoom*dt
        
    if keys["q"]:
        camera.zoom -= zcps*camera.zoom*dt - camera.zoom*dt

    camera.position.x += camera.velocity.x * dt
    camera.position.y += camera.velocity.y * dt

    uni.update(dt*dts)
    r.render(uni, ui)
    tick.check()

#</main>

