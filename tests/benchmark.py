import subprocess
import time
import os

def get_time(cdt, unit, tu):
    if unit == "min":
        tu *= 60
    if unit == "h":
        tu *= 60*60
    if unit == "d":
        tu *= 24*60*60
    if unit == "m":
        tu *= 30*24*60*60
    if unit == "h":
        tu *= 365*24*60*60

    start_time = time.time()
    os.chdir("../")
    with open(os.devnull, "w") as fnull:
        subprocess.call(["./graviton", "solar_system", "-min", "-cdt", str(cdt), "-tu", str(tu)], stdout = fnull, stderr = fnull)
    os.chdir("tests")
    return time.time() - start_time
