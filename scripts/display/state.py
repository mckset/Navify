import pickle
import subprocess
import os
from os.path import exists

pic = "pause.png"
x="2"
if exists("/home/seth/.navi/navify/icons/state.pkl") and not exists("/home/seth/.navi/navify/icons/start.txt"):
    f = open("/home/seth/.navi/navify/icons/state.pkl", 'rb')
    state = pickle.load(f)
    f.close()
    
    if state == "2":
        x="1"
        pic = "play.png"

if exists("/home/seth/.navi/navify/icons/start.txt"):
    os.remove("/home/seth/.navi/navify/icons/start.txt")

f = open("/home/seth/.navi/navify/icons/state.pkl", 'wb')
pickle.dump(x, f)
f.close()
   
print("/home/seth/.navi/navify/icons/" + pic)
subprocess.run(["/home/seth/.navi/navify/scripts/display/pause.sh", x])
