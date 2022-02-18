# Clears anything blacklisted from cache

import os
import sys
from os.path import exists
import subprocess
from os import walk

cache=next(walk("/home/seth/.navi/navify/cache/"), (None, None, []))[2]
bList=next(walk("/home/seth/.navi/navify/blacklist/"), (None, None, []))[2]

subprocess.run(["clear"])
print("Cleaning...\n")
for i in range(0,len(bList)):
   for x in range(0,len(cache)):
        if bList[i] == cache[x]:
            print("Delete: " + str(cache[x]))
            subprocess.run(["rm", "/home/seth/.navi/navify/cache/"+str(cache[x])])
   #print(str(i) + " / " + str(len(bList)))
print("Done\n")
