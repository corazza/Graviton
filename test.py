import us #Import UniSim

iterr = 0

def end (u):
    print "Simulation ran for", u.time, "seconds."


def run (u):
    global iterr
    
    iterr += 1
    
    if iterr <= 1000:
        return True
    else:
        return False
        

def init (u):
    u.addBody(us.Body(10000, 20))


uni1 = us.Uni("uni1", 6.7)

us.start(uni1, init, run, end, 0.001)

