"""Set custom event handlers in here. They wont overwrite anything."""

#Available handlers
# report(uni, datestring, percent, eta, has_been_running_real, has_been_running_univ, will_be_running, settings)
# update_handler(universe)
# interrupt_handler(univers)
# end_handler(universe)

import time

def additional_data(uni):
    earth   = uni.bodies["earth"]
    ep      = earth.position
    ev      = earth.velocity

    print "Earth position: (" + str(ep.x) + ", " + str(ep.y) + ", " + str(ep.z) + ")"
    print "Earth velocity: (" + str(ev.x) + ", " + str(ev.y) + ", " + str(ev.z) + ")"

def report(uni, real_date, percent, eta, has_been_running_real, has_been_running_univ, will_be_running, settings):

    if will_be_running.find("simulated") != -1:
        try:
            seconds = float(will_be_running.split()[0])
        except:
            seconds = "unknown"
    else:
        seconds = "unknown"

    print " --- This is an automatic status report. --- "
    print "The simulation started at real date |" + real_date + "|."
    print
    print "Percent completed: " + percent + "."
    print "ETA (real): [" + eta + "]."
    print
    print "Total number of updates: " + str(uni.nupdates) + "."
    print "It has been running for {0:.2f} real seconds.".format(has_been_running_real)
    print "It has been running for {0:.2f} simulated seconds.".format(has_been_running_univ)
    print "It will be running for another " + will_be_running + "."
    print "It will end at simulation date |" + uni.getDate(seconds) + "|."
    print
    print "Universe date: " + uni.getDate() + "." #uni.datatime = UNIX time at which the data was acquired.
    print "Universe time: " + str(uni.time) + " (in simulated seconds)."
    print
    print "Program settings:"
    print settings
    print
    print "#####################################"
    print

earth_info = ""

def interrupt_handler(uni):
    print "int"
    global earth_info

    earth       = uni.bodies["earth"]
    sun         = uni.bodies["sun"]

    earth_info += str(earth.position.x) + ' ' + str(earth.position.y) + ' ' + str(earth.position.z) + '\n'

def end_handler(uni):
    user_data = open("userdata/distances.txt", "w")
    user_data.write(earth_info)
    user_data.close()
