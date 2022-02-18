import pickle
import subprocess
import os
import sys
import keyboard
from os.path import exists

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Sets environmental variables
os.environ['SPOTIPY_CLIENT_ID']='481da7d376c747408b5ec25f609c193b'
os.environ['SPOTIPY_CLIENT_SECRET']='4ec619360c6e497a9ce1f126a3c10f93'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

subprocess.run(["clear"])

def home():

    print("s - Settings")
    print("r - Change which tracks to use for recommendations")
    print("x - Close ")
    inp = input("Command: ")
    
    if inp == "r":
        update()
    
    if inp == "s":
        settings()
    
    if inp == "x":
        exit()
    home()

def settings():
    subprocess.run(["clear"])
    inp2=""
    print("v - volume")
    print("x - exit")
    inp2=input("Option: ")

    if (inp2 == "v"):
        subprocess.run(["clear"])
        print("Use the UP and DOWN arrows to change the volume")
        print("Press ENTER to save the changes")
        print("Press X to exit without saving")
        print("")        
        x=0
        loop=1
        setting=[]
        while (loop != "0"):
            if (keyboard.read_key() == "up"):
                x=x+5
                subprocess.run(["/home/seth/.navi/navify/scripts/changeVolume.sh", "1"])
            if (keyboard.read_key() == "down"):
                x=x-5
                subprocess.run(["/home/seth/.navi/navify/scripts/changeVolume.sh", "-1"])
            if (keyboard.read_key() == "enter"):
                
                
                if not exists("/home/seth/.navi/navify/settings.pkl"):                
                    subprocess.run(["echo", "100 > /home/seth/.navi/navify/settings.pkl"])
                    f = open("/home/seth/.navi/navify/settings.pkl", 'wb')
                    pickle.dump([100], f)
                    f.close()
                f = open("/home/seth/.navi/navify/settings.pkl", 'rb')
                setting = pickle.load(f)
                f.close()
                f = open("/home/seth/.navi/navify/settings.pkl", 'wb')
                setting[0]=setting[0] + x
                pickle.dump(setting, f)                
                f.close()
                loop="0"                
                print("Total volume: " + str(setting[0]))
            if (keyboard.read_key() == "x"):
                loop="0"

            if (x > 0):
                print("Current volume +" + str(x))
            else:
                print("Current volume " + str(x))
                       
            #print(keyboard.read_key())
        print("Press any key to continue")
        while not (keyboard.read_key()):
            x=0
    if (inp2 == "x"):
        subprocess.run(["clear"])
        home()
    settings()

# Updates the track list used for getting recommendations
def update():
    subprocess.run(["clear"])
    tracks=[]
    results=[]
    i=0;    
    x=0
    while i != 1: 
        results.append(sp.current_user_saved_tracks(20, x))
        #print(len(sp.current_user_saved_tracks(20, x)['items']))
        x+=20
        if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
            i=1
            
                    

    inp2=""
    
    while inp2 != "x":
        for i in range(0, len(results)):
            for idx, item in enumerate(results[i]['items']):
                track = item['track']
                select=""
                for a in range(len(tracks)):
                    if (tracks[a] == results[i]['items'][idx]['track']['id']):
                        select="[X] "
                print(select + str(idx + 20 * i), track['artists'][0]['name'], " – ", track['name'])
        print(" ")   
        inp2 = input("Track (one at a time, x to exit): ")
        subprocess.run(["clear"])
        if inp2 == "x":
            break
        x=0        
        if (int(inp2) > 19):
            for i in range(0,int(inp2)):
                if (int(inp2) - i * 20 <=0):
                    x=i-1
                    inp2=int(inp2) - x*20
                    break;
        tracks.append(results[x]['items'][int(inp2)]['track']['id'])
    print(tracks)
    
    # Stores the track information to be read by navify
    f = open('/home/seth/.navi/navify/recommend.pkl', 'wb')
    pickle.dump(tracks, f)
    f.close()

    likes=[]
    for i in range(0,len(results[0]['items'])):
        print(results[0]['items'][i]['track']['id'])
        likes.append(results[0]['items'][i]['track']['id'])
   
    for i in range(0,len(results[1]['items'])):
        print(results[1]['items'][i]['track']['id'])
        likes.append(results[1]['items'][i]['track']['id']) 
    f = open('/home/seth/.navi/navify/icons/likes.pkl', 'wb')
    pickle.dump(likes, f)
    f.close()    


    home()

def updateLikes():
    i=0
    results=[]
    x=0
    while i != 1: 
        results.append(sp.current_user_saved_tracks(20, x))
        #print(len(sp.current_user_saved_tracks(20, x)['items']))
        x+=20
        if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
            i=1

    for i in range(0,len(results)):
        for x in range(0,len(results[i]['items'])):
            cache=results[i]['items'][x]['track']['id']
            if not exists("/home/seth/.navi/navify/cache/" + str(cache)):
                f = open("/home/seth/.navi/navify/update/" + str(cache) , "w")
                f.write(str(results[i]['items'][x]['track']['artists'][0]['name']) + " - " + str(results[i]['items'][x]['track']['name']))
                f.close()


def exit():
    sys.exit()
updateLikes()
home()
