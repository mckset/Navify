import subprocess
import os
import sys
from os import walk



ID=[]
listed=[]
valid=[]


def load():
    combinedList=[]
    files=next(walk("/home/seth/.navi/navify/blacklist/"), (None, None, []))[2]
    for i in range(0,len(files)):
        currentFile = subprocess.Popen(["cat", "/home/seth/.navi/navify/blacklist/" + files[i]], stdout=subprocess.PIPE, text=True).communicate()[0] 
        listed.append(currentFile)
        valid.append(files[i])
    for i in range(0, len(listed)):
        combinedList.append([listed[i], valid[i]])
    combinedList.sort()
    for i in range(0, len(listed)):
        listed[i]=combinedList[i][0]
        valid[i]=combinedList[i][1]

def main():
    loop=1
    global ID
    global listed
    global valid

    while loop==1:
        subprocess.run(["clear"])
        for i in range(0, len(listed)):
            print("| " + str(i) + "	| : | " + listed[i] + " - " + valid[i])
        inp=input("Select a file to delete (type x to exit): ")
        
        if inp=="x":
            return 0;
        if int(inp) <= len(listed):   
            subprocess.run(["rm", "/home/seth/.navi/navify/blacklist/"+str(valid[int(inp)])])
            #print(valid[i])
        ID=[]
        listed=[]
        valid=[]    
        load()
load()
main()
