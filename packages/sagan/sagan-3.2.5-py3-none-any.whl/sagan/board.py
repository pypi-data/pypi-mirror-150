import subprocess
from subprocess import PIPE

def checkVersion():
    cp = subprocess.run(["i2cdetect", "-y", "1"], stdout=PIPE)
    stdoutstr = str(cp.stdout)
    if "10: 10" in stdoutstr: #APDS9200
        return "5"
    elif "1d" in stdoutstr:
        return "3"
    else:               #OLD Vers.
        return "4"
