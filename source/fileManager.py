import json

from uni import *
from body import *
from vector2 import *

class FileManager:
    def __init__(self, unisf):
        self.unisf = unisf
        
    def saveUni(self, uni, alt_name):
        """Read the name and all important state vars, create a JSON file in ../unis with uni.name as the filename, and save the state there."""

        desc = json.dumps(uni.desc())
        
        if alt_name == -1:
            open(self.unisf + uni.name + ".json", "w").write(desc)
        else:
            open(self.unisf + alt_name + ".json", "w").write(desc)            

    def loadUni(self, filename):
        """Read the JSON file specified by filename, create a uni, return the uni."""
        
        desc = json.loads(open(self.unisf + filename + ".json", "r").read())
        uni = Uni(desc["name"], desc["G"], desc["time"])
        uni.description = desc["description"]

        for bid in desc["bodies"]:
            d = desc["bodies"][bid]

            body = Body(d["name"], d["m"], d["r"], d["color"])
            body.position = Vector2(d["position"]["x"], d["position"]["y"])
            body.velocity = Vector2(d["velocity"]["x"], d["velocity"]["y"])

            uni.addBody(body, bid)
        
        return uni
        
