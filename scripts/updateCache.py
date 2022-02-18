import os
import sys
from os.path import exists
import subprocess
from os import walk

ID=next(walk("/home/seth/.navi/navify/cache/"), (None, None, []))[2]

for i in range(0,len(ID)):
    inp = ID[i]
    text=subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + inp], stdout=subprocess.PIPE, text=True).communicate()[0]
    if ";" in text:
        print("skipping: " + ID[i])
    elif "you" in text:
        #text=subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + inp], stdout=subprocess.PIPE, text=True).communicate()[0]
        name=subprocess.Popen(["youtube-dl", "--get-title",text], stdout=subprocess.PIPE, text=True).communicate()[0]
        print(text)
        print(name)
        subprocess.run(["/home/seth/.navi/navify/scripts/write2Cache.sh", name, inp, str(len(text))])
        print(subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + inp], stdout=subprocess.PIPE, text=True).communicate()[0])
