import PySimpleGUI as sg
import pickle
import subprocess
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Sets environmental variables
os.environ['SPOTIPY_CLIENT_ID']='481da7d376c747408b5ec25f609c193b'
os.environ['SPOTIPY_CLIENT_SECRET']='4ec619360c6e497a9ce1f126a3c10f93'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# Colors
background="#ccccdc"
foreground="#99aabf"
mouseover=("","#67778f")

defaultFont="Inter 40"

def main():
    results=[]
    i=0
    x=0
    while i != 1: 
        results.append(sp.current_user_saved_tracks(20, x))
        #print(len(sp.current_user_saved_tracks(20, x)['items']))
        x+=20
        if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
            i=1
    
    f = open('/home/seth/.navi/navify/recommend.pkl' ,'rb')    
    cRec = pickle.load(f)
    f.close()

    ID=[]
    name=[]
    cName=cRec # Name of current saved tracks
    for i in range(0, len(results)):
        for idx, item in enumerate(results[i]['items']):
            name.append(item['track']['name'] + " - " + item['track']['artists'][0]['name'])
            ID.append(item['track']['id'])
            for a in range(0, len(cRec)):
                if (item['track']['id'] == cRec[a]):
                    cName[a] = item['track']['name'] + " - " + item['track']['artists'][0]['name']
    
    f = open('/home/seth/.navi/navify/icons/likes.pkl', 'wb')
    pickle.dump(ID,f)
    f.close()
    for i in range(0,len(cRec)):
        pass

    f = open("/home/seth/.navi/navify/settings.pkl", 'rb')
    settings = pickle.load(f)
    f.close()
    layout2 = [
    [
        sg.Slider(range=(0,150), font=defaultFont, background_color= background, trough_color = foreground, default_value=settings[0], enable_events=True, key="-VOL2-"),
        sg.Listbox(values=name, background_color=foreground, font=defaultFont, text_color="#ffffff", no_scrollbar=True, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-LIKES-"),
        sg.Listbox(values=cName, background_color=foreground, font=defaultFont, text_color="#ffffff", no_scrollbar=True, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-CREC-")
    
    
    
    ],
    [
        sg.Text("Volume", background_color=background, font=defaultFont)
    ],
    [
        sg.Button("SUBMIT", font=defaultFont, button_color=foreground, mouseover_colors=mouseover, border_width=0,enable_events=True, key="-SUBMIT2-"),
        sg.Button("CANCEL", font=defaultFont, button_color=foreground, mouseover_colors=mouseover, border_width=0,enable_events=True, key="-CANCEL2-")
    ]        
    ]
    window2 = sg.Window("Settings", layout2, background_color="#ccccdc", border_depth=None)
    while True:
        event2, values2 = window2.read()
        window2["-VOL2-"].bind("<ButtonRelease-1>", window2["-VOL2-"].update())
        if event2 == "-VOL2-":
            #print(event2)
            #print(values2["-VOL2-"])
            settings[0] = values2["-VOL2-"]
            subprocess.Popen(["/home/seth/.navi/navify/GUI/changeVolume.sh", str(values2["-VOL2-"])])
        
        if event2 == "-SUBMIT2-":
            f = open("/home/seth/.navi/navify/settings.pkl", 'wb')
            pickle.dump(settings, f)
            f.close()
            window2.close()
            break


        if event2 == "-CANCEL2-":
            window2.close()
            break

#main()
