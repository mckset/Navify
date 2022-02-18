import pickle
import subprocess
import os
import sys
import re
from os.path import exists
from os import walk

# Set to 0 to only list files in the playCache folder
includeCache=1
cacheI=-1

noName=0

track = subprocess.Popen(["cat", "/home/seth/.navi/navify/playing.txt"], stdout=subprocess.PIPE, text=True)
track=track.communicate()[0]
os.remove("/home/seth/.navi/navify/playing.txt")
name=""
trackID=0


# Checks for no input
if (len(track) < 2):
    subprocess.run(["clear"])

    #print("Youtube Files: ")
    # Lists only tracks in the playCache folder
    folders=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[1]
    ID=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[2]
    locID=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[2]
    for i in range(0,len(folders)):
        tempID=(next(walk("/home/seth/.navi/navify/playCache/" + str(folders[i])), (None, None, []))[2])
        for x in range(0,len(tempID)):
            locID.append("playCache/" + str(folders[i]) + "/" + tempID[x])            
            ID.append("https://www.youtube.com/watch?v=" + tempID[x])            
    #print(locID)
    listed=[]

    for i in range(0,len(locID)):
        listed.append(subprocess.Popen(["cat", "/home/seth/.navi/navify/" + locID[i]], stdout=subprocess.PIPE, text=True).communicate()[0])
        
    listed[len(listed)-1]=listed[len(listed)-1][0:len(listed[len(listed)-1])-1]        
    valid=0

    sortID=[]
    sortListed=[]
    # Lists tracks in the Cache folder
    if includeCache==1:
       # print("\nSpotify Files: ")
        #cacheI=len(listed)-1
        tempID=next(walk("/home/seth/.navi/navify/cache/"), (None, None, []))[2]
        for i in range(0,len(tempID)):
            currentFile = subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + tempID[i]], stdout=subprocess.PIPE, text=True).communicate()[0]
            if ";" in currentFile:
                length=int(currentFile[len(currentFile)-3:])
                sortID.append(currentFile[0:length])
                #locID.append("cache/" + currentFile[0:length])
                sortListed.append(currentFile[length+1:len(currentFile)-3])
    combinedList=[]
    oldID=ID
    oldListed=listed
    ID=[]
    listed=[]
    for i in range(0,len(sortID)):
        combinedList.append([sortListed[i],sortID[i]])    
    combinedList.sort()
    cacheI=len(combinedList)-1   
    for i in range(0, len(sortID)):
        ID.append(combinedList[i][1])
        listed.append(combinedList[i][0])
    for i in range(0,len(oldID)):
        ID.append(oldID[i])
        listed.append(oldListed[i])        
    
    while valid==0: 
        for i in range(0,len(listed)):
            if "\n" in listed[i]:
                listed[i]=listed[i][0:len(listed[i])-1]
            print("| " + str(i) + "	| : | " + listed[i])
            if i == cacheI:
                print("\n Local Tracks: ")
        inp = input("Selection: ")
        if "+" in inp:
            inp = str(int(inp[1:]) + cacheI+1)
            print(inp)    
        if (int(inp) < len(listed)):
            track=ID[int(inp)]
            trackID=ID[int(inp)]
            valid=1
            name=listed[int(inp)]
            noName=1
        #subprocess.run(["clear"])
               

# Main Program

# Checks if the song is a youtube link and if it has been played before
if noName == 0:
    if "https://www.youtube" in track:
        short=track[32:]
        print(short)
        if exists("/home/seth/.navi/navify/playCache/" + short):
            name = subprocess.Popen(["cat", "/home/seth/.navi/navify/playCache/" + short], stdout=subprocess.PIPE, text=True)
            name=name.communicate()[0]
        else:    
            name = input("Track name: ")
            f = open("/home/seth/.navi/navify/playCache/" + short , "w")
            f.write(name)
            f.close()
    elif "https://youtu.be" in track:
        short=track[17:]
        #print(short)
        if exists("/home/seth/.navi/navify/playCache/" + short):
            name = subprocess.Popen(["cat", "/home/seth/.navi/navify/playCache/" + short], stdout=subprocess.PIPE, text=True)
            name=name.communicate()[0]
        else:    
            name = input("Track name: ")
            f = open("/home/seth/.navi/navify/playCache/" + short, "w")
            f.write(name)
            f.close()
    elif exists("/home/seth/.navi/navify/playCache/" + track) and noName == 0:
            name = subprocess.Popen(["cat", "/home/seth/.navi/navify/playCache/" + track], stdout=subprocess.PIPE, text=True)
            name=str(name.communicate()[0])
            track=+ trackID

print("Now Playing: " + name)

if "\n" in name:
    name=name[:len(name)-1]
name = re.sub(r'[^\x00-\x7f]',r'', name)

if len(name) > 16:
    name = str(name)[0:len(name)] + " | "
# Stores the track for the display to read
info = ["1", "1", "1", name]


f = open('/home/seth/.navi/navify/info.pkl', 'wb')
pickle.dump(info, f)
f.close()

vol=100

f = open('/home/seth/.navi/navify/settings.pkl', 'rb')
vol=pickle.load(f)
vol=vol[0]
f.close()


subprocess.run(["mpv","--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume=" + str(vol), track])



