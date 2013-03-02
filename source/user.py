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

def check(uni):
    return
    date = uni.getDate()

    if date.find("2006") != -1:
        print date


add("update_done", check)
