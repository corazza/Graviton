subs = {}    
    
def sub(event, f):
    if subs.has_key(event):
        subs[event].append(f)
    else:
        subs[event] = [f]

def unsub(event, f):
    if subs.has_key(event):
        subs[event] = [f2 for f2 in subs if f2 != f]    
    
def pub(event):
    print event
    
    if subs.has_key(event):
        for f in subs[event]: f()
        
