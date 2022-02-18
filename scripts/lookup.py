import subprocess
import os
import sys
from os import walk

ID=[]
listed=[]
inp=input("\nSearh: ").lower()

files=next(walk("/home/seth/.navi/navify/cache/"), (None, None, []))[2]
names=[]
combinedList=[]

for i in range(0,len(files)):
    names.append(subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + files[i]], stdout=subprocess.PIPE, text=True).communicate()[0])
    if ";" in names[i]:    
        length=int(names[i][len(names[i])-3:])            
        names[i]=names[i][length+1:len(names[i])-3]
for i in range(0,len(files)):
    combinedList.append([names[i],files[i]])    
    
combinedList.sort()
for i in range(0, len(files)):
    names[i]=combinedList[i][0]
    files[i]=combinedList[i][1]

for i in range(0,len(files)):
    #print(currentFile)   
    if str(inp) in str(names[i]).lower():
        print("| " + str(i) + "	| : | " + str(names[i]) + " - " + str(files[i]))

