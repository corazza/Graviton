import time

events = {
    "update_done": [],
    "report": [],
    "save": []
}

def add(event, handler):
    if events.has_key(event):
        events[event].append(handler)
    else:
        events[event] = [handler]

#--------#
#seconds in a year: 31536000


def additional_data(uni):
    earth = uni.bodies["earth"]
    ep = earth.desc()["position"]
    ev = earth.desc()["velocity"]
    print "Earth position: (" + str(ep["x"]) + ", " + str(ep["y"]) + ")"
    print "Earth velocity: (" + str(ev["x"]) + ", " + str(ev["y"]) + ")"

def check(uni):
    return

def report(uni, real_date, percent, eta, has_been_running_real, has_been_running_univ, will_be_running, settings):
    print
    print " --- This is an automatic status report. --- "
    print "The simulation started at real date |" + real_date + "|."
    print
    print "Percent completed: " + percent + "."
    print "ETA (real): " + eta + "."
    print
    print "It has been running for {0:.2f} real seconds.".format(has_been_running_real)
    print "It has been running for {0:.2f} simulated seconds.".format(has_been_running_univ)
    print "It will be running for another " + will_be_running + "."
    print
    print "Universe date: " + uni.getDate() + "." #uni.datatime = UNIX time at which the data was acquired.
    print "Universe time: " + str(uni.time) + " (in simulated seconds)."
    print
    print "Program settings:"
    print settings
    print
    print "Additional data:"
    additional_data(uni)
    print
    print "#####################################"
    print

add("update_done", check)
