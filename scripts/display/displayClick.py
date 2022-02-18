import pickle
import subprocess
from os.path import exists

if exists('/home/seth/.navi/navify/info.pkl'): 
    f = open('/home/seth/.navi/navify/info.pkl', 'rb')
    info = pickle.load(f)
    f.close()
    
    fText=str(info[0]) + " " + str(info[1])
    text=""
    for i in range(0,len(fText)):
        if fText[i:i+1] == " ":
            text=text+"+"
        else:
            text=text+fText[i:i+1]
    subprocess.run(['firefox', "https://www.youtube.com/results?search_query=" + text])
    subprocess.run(['xed', "/home/seth/.navi/navify/cache/" + str(info[2])])
    #https://www.youtube.com/results?search_query=
