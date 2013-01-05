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
    
