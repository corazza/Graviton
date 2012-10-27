import json

from uni import *
from body import *
from vector2 import *

class FileManager:
    def __init__(self, unisf):
        self.unisf = unisf
        
    def saveUni(self, uni):
        """Read the name and all important state vars, create a JSON file in ../unis with uni.name as the filename, and save the state there."""
        print "File manager: saving uni with name " + uni.name + "."
        
        json.dump(uni.desc(), open(self.unisf + uni.name, "w"))

    def loadUni(self, filename):
        """Read the JSON file specified by filename, create a uni, return the uni."""
        print "File manager: loading uni " + filename + "."
        
        desc = json.load(open(self.unisf + filename, "r"))
        
        uni = Uni(desc["name"], desc["G"], desc["time"])

        for bid in desc["bodies"]:
            d = desc["bodies"][bid]

            body = Body(d["name"], d["m"], d["r"], d["color"])
            body.position = Vector2(d["position"]["x"], d["position"]["y"])
            body.velocity = Vector2(d["velocity"]["x"], d["velocity"]["y"])

            uni.addBody(body, bid)
        
        return uni
        
