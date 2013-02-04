import sys
import os
import time
import ConfigParser

import fileManager
import event as gevent
import util
from body import *

#<command line arguments>
if len(sys.argv) < 2:
    raise Exception("World name not given!")

runForU = -1 #Run for x universe seconds, -1 = run forever.
runForR = -1 #Run for x real seconds, -1 = run forever. One of U and R has to be -1.
mini = False #The minimal version of Graviton should be running.
alt_name = -1 #Save the simulation in an alternative file, without modifying the original, -1 = use the original name, -2 = using -fe.
dir_name = -1 #Save the simulation in a different file each time.
save_sim_each = 0 #Save the simulation each x updates, 0 = no automatic saving, 1 = save each update.
report_each = 0 #Report some state each x real time seconds.

#These will not be booleans, but floats. This is for convenience.
dts = False #Delta-time scale
cdt = False #Constant delta-time

#Flags
vardt = True #This is a boolean, it is determined by the program and not settings.ini.
set_fe = False
cnt = False
save_at_exit = False

#tmp
found_cdt = False
found_tr = False
found_tu = False

for i in range(len(sys.argv)):
    arg = sys.argv[i]

    if arg == "-se":
        save_at_exit = True
        print "When the simulation is over it will save itself."

    if arg == "-cnt":
        print "Will attempt to continue from the last save file (created by the -fe flag)."
        cnt = True

    if arg == "-min":
        mini = True
        vardt = False
        dts = 1
        print "Minimal mode activated."
        print "Delta-time scale set to 1."

    if arg == "-tu":
        if i + 1 < len(sys.argv) and not found_tr:
            found_tu = True
            runForU = float(sys.argv[i+1])
            print "The simulation will be running until " + util.getDate(runForU) + " (universe time)."
        elif found_tr:
            "-tu ignored, -tr already set."
        else:
            raise Exception("Parameter for '-t' not given! It must be a float following '-t', eg. '-t 200000.2432'.")

    if arg == "-tr":
        if i + 1 < len(sys.argv) and not found_tu:
            found_tr = True
            runForR = float(sys.argv[i+1])
            print "The simulation will be running for " + str(runForR) + " seconds."
        elif found_tu:
            print "-tr ignored, -tu already set."
        else:
            raise Exception("Parameter for '-t' not given! It must be a float following '-t', eg. '-t 200000.2432'.")

    if arg == "-r":
        if i + 1 < len(sys.argv):
            report_each = float(sys.argv[i+1])
            print "There will be a report each " + str(report_each) + " real time seconds."
        else:
            raise Exception("Parameter for '-r' not given! It must be a float following '-r', eg. '-t 120.5'.")

    if arg == "-f":
        if i + 1 < len(sys.argv) and not set_fe:
            alt_name = sys.argv[i+1]
            print "Using alternative name \"" + alt_name + "\" for saving."
        elif set_fe:
            print "Already using the -fe option!"
        else:
            raise Exception("Parameter for '-f' not given! It must be a string following '-f', eg. '-t alternative_name'.")

    if arg == "-fe":
        alt_name = -2
        set_fe = True
        print "The simulation will be saved in a different \"unis/uni_name/[at date].json.\" file each time (save() is called)."

    if arg == "-s":
        if i + 1 < len(sys.argv):
            save_sim_each = int(sys.argv[i+1])
            print "The simulation will be saved each " + str(save_sim_each) + " universe updates."
        else:
            raise Exception("Parameter for '-s' not given! It must be an integer following '-s', eg. '-s 20'.")

    if arg == "-dts":
        if i + 1 < len(sys.argv) and not found_cdt and not mini:
            dts = float(sys.argv[i+1])
            print "Running the simulation with a delta-time scale of " + str(dts) + "."
            print "WARNING: delta-time is variable."

        elif found_cdt or mini:
            dts = 1
            if found_cdt:
                print "WARNING: cannot set a non-one delta-time scale if constant delta-time is set."

            if mini:
                print "WARNING: cannot set a non-one delta-time scale if min mode is on. Use -cdt <float> to set a constant delta-time."

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

print
#</command line arguments>

#Effects imports:
if not mini:
    import pygame
    from pygame.locals import *

    import tick

    import gfx
    import ui as uim

#<settings>
config = ConfigParser.RawConfigParser()
config.read("settings.ini")

#vardt is True by default, if these values were not specified.
dts = dts or config.getfloat("sim", "dts") #Delta-time scale (2 means that the simulation will run 2 times the normal speed of the universe).
cdt = cdt or config.getfloat("sim", "cdt") #Constant delta-time (better perfrmace, poorer presentation).
unidir = os.getcwd() + "/" + config.get("prog", "unidir")

#Effects settings:
if not mini:
    x = config.getint("prog", "x")
    y = config.getint("prog", "y")
    ui_path = config.get("prog", "ui")
    ps = config.getint("prog", "ps") #Renderer scale
    cs = config.getint("prog", "cs") #Camera speed
    zoom = config.getfloat("prog", "zoom") #Default zoom
    zcps = config.getfloat("prog", "zcps") #Zoom change per second
#</settings>






#<init>
run = True
last_saved = 0 #How many updates went by since the last save?
last_reported = 0 #How many real time seconds went by since the last save?

lasted = 0 #How much did the simulation last?
last = time.time()
start = last
dt = 0 #Initially nothing happens (if vardt is on).

manager = fileManager.FileManager(unidir)

if not cnt:
    uni = manager.loadUni(sys.argv[1])

    if alt_name == -2:
        print "WARNING: Deleting previous saves of " + sys.argv[1] + "."
        manager.delSaves(sys.argv[1]);

else:
    uni = manager.cnt(sys.argv[1])

uni.name = sys.argv[1] #If it's not set or differs from the filename, which it shouldn't.

if not mini:
    pygame.init()

    icon = pygame.image.load("images/icon.png")
    screen = pygame.display.set_mode((x, y))
    camera = gfx.Camera()
    renderer = gfx.Renderer(screen, pygame, camera)
    ui = uim.UI(uni, camera)

    pygame.display.set_caption("Graviton - " + sys.argv[1])
    pygame.display.set_icon(icon)

    camera.zoom = zoom
    renderer.scale = ps

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

#</init>








#<events>
def save():
    print "Saving."
    manager.saveUni(uni, alt_name)

def report():
    will = -1 #Nothing specified.

    if runForR > -1:
        has = (time.time() - start) #Has been running for / real seconds.
        will = runForR - lasted #Will be running for / real seconds.

        has = str(has) + " real seconds"
        will = str(will) + " real seconds"

    elif runForU > -1:
        has = uni.time #Has been running for / universe seconds.
        will = runForU - uni.time #Will be running for / universe seconds.

        has = str(has) + " universe seconds"
        will = str(will) + " universe seconds"

    if will < 0:
        has = (time.time() - start) #Has been running for / real seconds.
        will = "unlimited"

        has = str(has) + " real seconds"
        will = str(will) + " real seconds"

    print " --- This is an automatic status report. --- "
    print "The simulation started at date " + time.asctime(time.localtime(start)) + "."

    print "It has been running for " + has + "."
    print "It will be running for another " + will + "."

    print "Universe date: " + uni.getDate() + "." #uni.datatime = UNIX time at which the data was acquired.
    print "Universe time: " + str(uni.time) + " (in universe seconds)."
    print
    print "Program settings:"
    if vardt:
        print "Delta-time scale:", dts
    else:
        print "Constant delta-time:", cdt
    print
    print


gevent.sub("report", report)
gevent.sub("save", save)
#</events>


#<functions>
def pygUpdate():
    run = True

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

    renderer.render(uni, ui)
    return run

#</functions>


#<setup>
print "Starting the simulation."
print
report()
#</setup>

#<main>

#1. Mathematically enhance the Uni class.

while run:
    #If variable delta-time is set:
    if vardt:
        uni.update(dt*dts)
    else: #Else forward in time by some constant.
        uni.update(cdt)

    if not mini:
        run = pygUpdate()
        tick.check()

    #The update is considered to be done.

    if save_sim_each > 0:
        last_saved += 1

        if last_saved >= save_sim_each:
            last_saved = 0
            save()

    if report_each > 0:
        last_reported += dt

        if last_reported >= report_each:
            last_reported = 0
            report()

    if runForU > -1:
        if runForU <= uni.time:
            run = False

    elif runForR > -1:
        if runForR <= lasted:
            run = False

    dt = time.time() - last
    last = time.time()
    lasted += dt
#</main>

print "The simulation has ended."
print
report()

if save_at_exit:
    save()
