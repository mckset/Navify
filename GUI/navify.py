import pickle
import subprocess
import os
import sys
import re
from os.path import exists

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from urllib import request, parse

loop="true"

# Sets environmental variables
os.environ['SPOTIPY_CLIENT_ID']='481da7d376c747408b5ec25f609c193b'
os.environ['SPOTIPY_CLIENT_SECRET']='4ec619360c6e497a9ce1f126a3c10f93'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'

scope = ["user-library-read", "user-library-modify"]
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

recId=[]
recList=[]
recTrack=[]
recArtist=[]
settings=[]
vol=100
header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}


def unlike(track):
    sp.current_user_saved_tracks_delete([track])

def like(track):
    sp.current_user_saved_tracks_add([track])

def genRec():
    global recId
    global recList
    global recTrack
    global recArtist    
    recID=[]
    fText=""

    f = open('/home/seth/.navi/navify/tracks.pkl', 'rb')
    trackB = pickle.load(f)
    f.close()
    f = open('/home/seth/.navi/navify/videos.pkl', 'rb')
    videoB = pickle.load(f)
    f.close()

    # Sets up the track list used to grab recommendations
    
    if exists('/home/seth/.navi/navify/recommend.pkl'):
        f = open('/home/seth/.navi/navify/recommend.pkl', 'rb')
        tracks = pickle.load(f)
        f.close()
    else:
        print("WARNING: Recommended tracks list is not set up. Defaulting to the first 5 liked songs. Please run navify -s")
        x=0
        tracks=["","","","",""]
        # Sets up the playlist to use based off of the first 5 tracks in the liked playlist
        results = sp.current_user_saved_tracks()
        for i in range(0,5):
            for y in range(0,len(trackB)):    
                if (results['items'][int(i+x)]['track']['id'] == trackB[y]):
                    y=0
                    x=x+1
            tracks[i] = results['items'][int(i+x)]['track']['id']    
    rec=sp.recommendations(seed_tracks=tracks, limit=50)
    
    for i in range(0,49):
        if not exists('/home/seth/.navi/navify/blacklist/' + str(rec['tracks'][i]['id'])):
            recTrack.append(str(rec['tracks'][i]['name']))
            recArtist.append(str(rec['tracks'][i]['artists'][0]['name']))
            recList.append(str(rec['tracks'][i]['name']) + " " + str(rec['tracks'][i]['artists'][0]['name']))
            recId.append(rec['tracks'][i]['id'])
        else:
            recTrack.append("skip")
            recArtist.append("skip")
            recList.append("skip")
            recId.append("skip")
            
    results = sp.current_user_saved_tracks()
    likes=[]
    for idx, item in enumerate(results['items']):
        likes.append(results['items'][idx]['track']['id'])

    tracksName=[]    
    i=0
    for i in range(0,len(recId)):
        if not exists("/home/seth/.navi/navify/cache/" + recId[i]) and recId[i] != "skip":
            fText=str(recTrack[i]) + " - " + str(recArtist[i])
            fText = re.sub(r'[^\x00-\x7f]',r'', fText)
            name=fText
            for x in range(0,len(fText)):
                if " " in fText[x:x+1]:
                    fText=fText[0:x] + "+" + fText[x+1:]            
            search(recList[i], recId[i], name, fText)
        print(str(i))
    for i in range(0,len(recId)):
        currentFile = subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + recId[i]], stdout=subprocess.PIPE, text=True).communicate()[0]                    
        tracksName.append(currentFile[0:43])
    return tracksName

def search(string, cache, name, url):
       
    req=request.Request("https://youtube.com/results?search_query=" + url, headers=header)
    U = request.urlopen(req)
    data = U.read().decode('utf-8')
    
    for i in range(0,len(data)):
	    if "videoid" in data[i:i+7].lower() and not "videoids" in data[i:i+8].lower():
		    video=data[i+10:i+21]
		    break
    
    f = open("/home/seth/.navi/navify/cache/" + str(cache) , "w")
    f.write("https://www.youtube.com/watch?v=" + video + ";" + name + " " + str(len("https://www.youtube.com/watch?v=" + video)))
    f.close()
    print(cache)
        
