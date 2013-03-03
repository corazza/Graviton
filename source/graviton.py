import sys
import os
import time
import ConfigParser

import fileManager
import event as gevent
import util
from body import *

import user #For user scripts.


#./graviton solar_system -s x -r 60 -tu y -cdt z -fe -min





#<options>
runForU             = -1 #Run for x simulated seconds, -1 = run forever.
runForR             = -1 #Run for x real seconds, -1 = run forever. One of U and R has to be -1.
mini                = False #The minimal version of Graviton should be running.
alt_name            = -1 #Save the simulation in an alternative file, without modifying the original, -1 = use the original name, -2 = using -fe.
dir_name            = -1 #Save the simulation in a different file each time.
save_sim_each       = 0 #Save the simulation each x updates, 0 = no automatic saving, 1 = save each update.
report_each         = 0 #Report some state each x real time seconds.
orbit_resolution    = 0 #Update orbits each x real time seconds.
orbit_buffer        = 0 #Keep orbit edge positions in memory for x simulated seconds.

#These will not be booleans, but floats. This is for convenience.
dts = False #Delta-time scale
cdt = False #Constant delta-time

#Flags
vardt           = True #This is a boolean, it is determined by the program and not settings.ini.
set_fe          = False
cnt             = False
save_at_exit    = False
draw_orbits     = False
#</options>






#<command line arguments>
if len(sys.argv) < 2:
    raise Exception("World name not given!")

#tmp
found_cdt   = False
found_dts   = False
found_tr    = False
found_tu    = False

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

    if arg == "-do":
        if i + 2 < len(sys.argv):
            draw_orbits = True
            orbit_resolution = float(sys.argv[i+1])
            orbit_buffer = int(sys.argv[i+2])
        else:
            raise Exception("Parameters for '-do' not given! They must be a float and an int following '-do', eg. '-t 0.5 10000.0'.")

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
            save_sim_each = float(sys.argv[i+1])
            print "The simulation will be saved each " + str(save_sim_each) + " simulated seconds."
        else:
            raise Exception("Parameter for '-s' not given! It must be an integer following '-s', eg. '-s 20'.")

    if arg == "-dts":
        if i + 1 < len(sys.argv) and not found_cdt and not mini:
            dts = float(sys.argv[i+1])
            found_dts = True
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








#<effects imports>
if not mini:
    import pygame
    from pygame.locals import *

    import tick

    import gfx
    import ui as uim
#</effects imports>








#<options>
config = ConfigParser.RawConfigParser()
config.read("settings.ini")

#vardt is True by default, if these values were not specified.

try:
    if not found_cdt:
        cdt = config.getfloat("sim", "cdt") #Constant delta-time (better perfrmace, poorer presentation).
except:
    pass

try:
    if not found_dts:
        dts = config.getfloat("sim", "dts") #Delta-time scale (2 means that the simulation will run 2 times the normal speed of the simulation).
except:
    pass

unidir = os.getcwd() + "/" + config.get("prog", "unidir")
FPS = config.getint("prog", "fps")
FPS = 1000.0/FPS

#Effects settings:
if not mini:
    x = config.getint("prog", "x")
    y = config.getint("prog", "y")
    ui_path = config.get("prog", "ui")
    ps = config.getint("prog", "ps") #Renderer scale
    cs = config.getint("prog", "cs") #Camera speed
    zoom = config.getfloat("prog", "zoom") #Default zoom
    zcps = config.getfloat("prog", "zcps") #Zoom change per second
#</options>








#<init>
run = True
last_saved = 0 #How many updates went by since the last save?
last_reported = 0 #How many real time seconds went by since the last save?
last_render = 0
last_take_pos = 0

lasted = 0 #How much did the simulation last? (in real seconds)
last = time.time()
start = last
dtr = 0 #Initially nothing happens (if vardt is on).

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
    renderer = gfx.Renderer(screen, pygame, camera, orbit_buffer, draw_orbits)
    renderer.FPS = FPS
    ui = uim.UI(uni, camera)

    pygame.display.set_caption("Graviton - " + sys.argv[1])
    pygame.display.set_icon(icon)

    camera.zoom = zoom
    renderer.scale = ps

    #<UI updates>
    def update_time_info(el):
        #el.setText("Time: " + str(int(uni.time/60/60)) + "h.")
        el.setText("Date: " + uni.getDate())

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










#<functions>

last_report_percentstamp    = -1
last_report_timestamp       = -1

def report(arg):
    global last_report_percentstamp
    global last_report_timestamp

    will_num = -1 #Nothing specified.

    has_been_running_real   = (time.time() - start)
    has_been_running_univ   = uni.time
    will_be_running_univ    = runForU - uni.time
    will_be_running_real    = runForR - lasted

    time_limit = True

    if runForR > -1:
        will_be_running     = will_be_running_real
        will_be_running_s   = str(will_be_running) + " real seconds"
        has_been_running    = has_been_running_real
        has_been_running_s  = str(has_been_running) + " real seconds"
    elif runForU > -1:
        will_be_running     = will_be_running_univ
        will_be_running_s   = str(will_be_running) + " simulated seconds"
        has_been_running    = has_been_running_univ
        has_been_running_s  = str(has_been_running) + " simulated seconds"
    else:
        time_limit = False
        print "Time limit bb"
        will_be_running     = 0
        will_be_running_s   = "unknown seconds"
        has_been_running    = has_been_running_real
        has_been_running_s  = str(has_been_running) + " real seconds"

    #Some simulations don't have a time limit:
    if time_limit:
        percent     = 100 * has_been_running / (has_been_running+will_be_running)
        percent_s   = "{0:.4f}%".format(percent)
        eta_s       = ""

        if percent != 0 and lasted != 0:
            seconds_since_last_report = time.time() - last_report_timestamp
            percent_since_last_report = percent - last_report_percentstamp

            remaining_percent   = 100 - percent
            percent_per_second  = percent_since_last_report/seconds_since_last_report

            seconds = int(remaining_percent / percent_per_second)

            years   = seconds/60/60/24/365
            seconds -= years*365*24*60*60

            days    = seconds/60/60/24
            seconds -= days*24*60*60

            hours   = seconds/60/60
            seconds -= hours*60*60

            minutes = seconds/60
            seconds -= minutes*60

            eta_s += str(years)     + " years "
            eta_s += str(days)      + " days "
            eta_s += str(hours)     + " hours "
            eta_s += str(minutes)   + " minutes "
            eta_s += str(seconds)   + " seconds"
        else:
            eta_s += "unknown"

        last_report_timestamp = time.time()
        last_report_percentstamp = percent

    else:
        eta_s       = "unknown"
        percent_s   = "unknown"

    if vardt:
        time_setting = "Delta-time scale: " + str(dts)
    else:
        time_setting = "Constant delta-time: " + str(cdt)

    settings = ""

    settings += time_setting

    user.report(uni, time.asctime(time.localtime(start)), percent_s, eta_s, has_been_running_real, has_been_running_univ, will_be_running_s, settings)



def pygUpdate():
    global last_render
    global last_take_pos
    run = True

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
        camera.zoom *= zcps ** dtr

    if keys["q"]:
        camera.zoom /= zcps ** dtr

    if camera.determineDirection(keys["w"], keys["a"], keys["s"], keys["d"]):
        factor =  cs * dtr / camera.zoom
        camera.position.x += math.cos(camera.direction) * factor
        camera.position.y += math.sin(camera.direction) * factor

    if last_render/FPS > 1:
        renderer.render(uni, ui)
        last_render = 0
    else:
        last_render += 1

    if draw_orbits:
        last_take_pos += dtr

        if last_take_pos/orbit_resolution > 1:
            renderer.take_pos(uni)
            last_take_pos = 0

    return run

#</functions>










#<events>
def save(arg):
    print "Saving."
    manager.saveUni(uni, alt_name)

gevent.sub("save", save)
gevent.sub("report", report)

for event in user.events:
    for handler in user.events[event]:
        gevent.sub(event, handler)

#</events>










#<setup>
print "Starting the simulation."
print
gevent.pub("report", None)
#</setup>












#<main>
while run:
    #dtr: real seconds
    #dtu: simulated seconds

    #If variable delta-time is set:
    if vardt:
        dtu = dtr*dts #Immediate delta-time.
    else: #Else forward in time by some constant.
        dtu = cdt

    uni.update(dtu)

    if not mini:
        run = pygUpdate()
        tick.check()

    #The update is considered to be done.

    if save_sim_each > 0:
        last_saved += dtu

        if last_saved >= save_sim_each:
            last_saved = 0
            save()

    if report_each > 0:
        last_reported += dtr

        if last_reported >= report_each:
            last_reported = 0
            gevent.pub("report", None)

    if runForU > -1:
        if runForU <= uni.time:
            run = False

    elif runForR > -1:
        if runForR <= lasted:
            run = False

    dtr = time.time() - last
    last = time.time()
    lasted += dtr
#</main>






#<termination>
gevent.pub("end", uni)
print "The simulation has ended."
print
gevent.pub("report", None)

if save_at_exit:
    save()
#</termination>
