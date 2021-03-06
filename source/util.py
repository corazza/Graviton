def toScreen(vector, camera, width=1300, height=700):
    np = [vector.x, vector.y]

    np[0] -= camera.position.x
    np[1] -= camera.position.y

    np[0] *= camera.zoom
    np[1] *= camera.zoom

    np[0] += width/2
    np[1] += height/2

    np[0] = int(np[0])
    np[1] = int(np[1])

    return np

def toScreenXy(np, camera, width=1300, height=700):
    np[0] -= camera.position.x
    np[1] -= camera.position.y

    np[0] *= camera.zoom
    np[1] *= camera.zoom

    np[0] += width/2
    np[1] += height/2

    np[0] = int(np[0])
    np[1] = int(np[1])

    return np

def toWorld(vector, camera, w=1300, h=700):
    np = [vector.x, vector.y]

    np[0] -= camera.position.x
    np[1] -= camera.position.y

    np[0] *= camera.zoom
    np[1] *= camera.zoom

    np[0] += width/2
    np[1] += height/2

    np[0] = int(np[0])
    np[1] = int(np[1])

    return np

def lengthToWorld(l, camera):
    return l/camera.zoom

def lengthToScreen(l, camera):
    return l*camera.zoom

#at 1,142,271,059 seconds
def getDate(seconds):
    """Calculate the date offset from 2006-Mar-13 17:30:59"""

    return "2006-Mar-13 17:30:59 + " + str(seconds) + " seconds"
