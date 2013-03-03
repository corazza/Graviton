import os
import json

from uni import *
from body import *
from vector2 import *

class FileManager:
    def __init__(self, unisdir):
        self.unisdir = unisdir

    def saveUni(self, uni, alt_name):
        """Read the name and all important state vars, create a JSON file in ../unis with uni.name as the filename, and save the state there."""

        desc = json.dumps(uni.desc())

        if alt_name == -1: #Overwrite the original file.
            open(self.unisdir + uni.name + ".json", "w").write(desc)

        elif alt_name == -2: #Use a dedicated directory and a new file.
            directory = self.unisdir + uni.name + "/"

            if not os.path.exists(directory):
                os.makedirs(directory)

            open(directory + uni.getDate() + ".json", "w").write(desc)

        else: #Use a new file name.
            open(self.unisdir + alt_name + ".json", "w").write(desc)

    def load(self, filename):
        """Read the JSON file specified by filename, create a uni, return the uni."""

        desc = json.loads(open(filename, "r").read())
        uni = Uni(desc["name"], desc["G"], desc["time"])
        uni.description = desc["description"]

        if desc.has_key("datatime"):
            uni.datatime = desc["datatime"] #UNIX time at which the data was acquired.
        else:
            uni.datatime = "N/A"

        for bid in desc["bodies"]:
            d = desc["bodies"][bid]

            body = Body(d["name"], d["m"], d["r"], d["color"])
            body.position = Vector2(d["position"]["x"], d["position"]["y"], d["position"]["z"])
            body.velocity = Vector2(d["velocity"]["x"], d["velocity"]["y"], d["velocity"]["z"])

            uni.addBody(body, bid)

        return uni

    def delSaves(self, name):
        """Called when the -fe option is on, but the -cnt is not."""
        dire = self.unisdir + name + "/"

        try:
            dirs = os.listdir(dire)
        except:
            dirs = []
            print "Can't delete", dire + ": not found."

        for dfile in dirs:
            file_path = os.path.join(dire, dfile)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e

    def cnt(self, name):

        filename = self.unisdir + name + "/"

        od = os.getcwd()

        os.chdir(filename)
        filelist = os.listdir(os.getcwd())
        filelist = filter(lambda x: not os.path.isdir(x), filelist)

        filename += max(filelist, key=lambda x: os.stat(x).st_mtime)

        os.chdir(od)

        return self.load(filename)

    def loadUni(self, name):
        """Read the JSON file specified by filename, create a uni, return the uni."""

        filename = self.unisdir + name + ".json"

        return self.load(filename)

