import sys
import os
import time
import ConfigParser

import pygame
from pygame.locals import *

import gfx
import fileManager
import ui as uim
import event as gevent
import tick
import util
from body import *

if len(sys.argv) < 2:
    raise Exception("World name not given!")



#<settings>

#defaults:
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

#command line args:
runFor = -1 #Run for x seconds, -1 = run forever.
mini = False #The minimal version of Graviton should be running.
alt_name = -1 #Save the simulation in an alternative file, without modifying the original, -1 = use the original name.
save_sim_each = -1 #Save the simulation each x updates, 0 = no automatic saving, 1 = save each update.

found_cdt = False

for i in range(len(sys.argv)):
    arg = sys.argv[i]

    if arg == "-t":
        if i + 1 < len(sys.argv):
            runFor = float(sys.argv[i+1])
            print "The simulation will be running until " + util.getDate(runFor) + "."
        else:
            raise Exception("Parameter for '-t' not given! It must be a float following '-t', eg. '-t 200000.2432'.")
    
    if arg == "-f":
        if i + 1 < len(sys.argv):
            alt_name = sys.argv[i+1]
            print "Using alternative name \"" + alt_name + "\" for saving."
        else:
            raise Exception("Parameter for '-f' not given! It must be a string following '-f', eg. '-t alternative_name'.")

    if arg == "-s":
        if i + 1 < len(sys.argv):
            save_sim_each = int(sys.argv[i+1])
            print "The simulation will be saved each " + str(save_sim_each) + " universe updates."
        else:
            raise Exception("Parameter for '-s' not given! It must be an integer following '-s', eg. '-s 20'.")
            
    if arg == "-dts":
        if i + 1 < len(sys.argv) and not found_cdt:
            dts = float(sys.argv[i+1])
            print "Running the simulation with a delta-time scale of " + str(dts) + "."
        elif found_cdt:
            dts = 1
            print "WARNING: cannot set a non-one delta-time scale if constant delta-time is set."
            print "Delta-time scale set to 1."
        else:
            raise Exception("Parameter for '-dts' not given! It must be a float following '-dts', eg. '-dts 20000.123'.")

    if arg == "-cdt":
        if i + 1 < len(sys.argv):
            cdt = float(sys.argv[i+1])
            vardt = False
            found_cdt = True
            dts = 1
            print "Running the simulation with a constant delta-time of " + str(cdt) + " seconds."
            print "Delta-time scale set to 1."
        else:
            raise Exception("Parameter for '-cdt' not given! It must be a float following '-cdt', eg. '-cdt 10.0'.")
            
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
start = time.time()

#<UI updates>
def update_time_info(el):
    el.setText("Time: " + str(int(uni.time/60/60)) + "h.")

def set_desc(el):
    el.setText(uni.description)
    el.x = x/2 - el.w/2
#</ui updates>


ui.addSetter("desc", set_desc)
ui.addUpdate("time", update_time_info)

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

last_saved = 0 #How many updates went by since the last save?
#</init>








#<events>
def save():
    m.saveUni(uni, alt_name)

gevent.sub("save", save)
#</events>



#<setup>
#</setup>



#<main>

#1. Check whether my time-keeping makes any sense or whether it causes errors.

while run:
    dt = time.time() - last
    last = time.time()
        
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
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
            keys["w"] = True
            
        if event.type == KEYDOWN and event.key == K_a:
            keys["a"] = True

        if event.type == KEYDOWN and event.key == K_s:
            keys["s"] = True
        
        if event.type == KEYDOWN and event.key == K_d:
            keys["d"] = True
        

        if event.type == KEYUP and event.key == K_w:
            keys["w"] = False
            
        if event.type == KEYUP and event.key == K_a:
            keys["a"] = False

        if event.type == KEYUP and event.key == K_s:
            keys["s"] = False
        
        if event.type == KEYUP and event.key == K_d:
            keys["d"] = False
            

    if keys["e"]:
        camera.zoom *= zcps ** dt
        
    if keys["q"]:
        camera.zoom /= zcps ** dt
        
    if camera.determineDirection(keys["w"], keys["a"], keys["s"], keys["d"]):
        factor =  cs * dt / camera.zoom
        camera.position.x += math.cos(camera.direction) * factor
        camera.position.y += math.sin(camera.direction) * factor

    #If variable delta-time is set:
    if vardt:
        uni.update(dt*dts)
    else: #Else forward in time by some constant.
        uni.update(cdt)
        
    r.render(uni, ui)
    tick.check()
    
    #The update is considered to be done.

    if runFor > -1:
        if runFor < uni.time:
            run = False

    if save_sim_each > 0:
        last_saved += 1

        if last_saved >= save_sim_each:
            last_saved = 0
            gevent.pub("save")
#</main>

