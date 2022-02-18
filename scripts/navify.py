import pickle
import subprocess
import os
import sys
import re
from os.path import exists

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import spotipy
from spotipy.oauth2 import SpotifyOAuth

loop="true"

# Sets environmental variables
os.environ['SPOTIPY_CLIENT_ID']='481da7d376c747408b5ec25f609c193b'
os.environ['SPOTIPY_CLIENT_SECRET']='4ec619360c6e497a9ce1f126a3c10f93'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'

scope = ["user-library-read", "user-library-modify"]
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "/home/seth/.navi/navify/client.json"

    # Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

recId=[]
recList=[]
recTrack=[]
recArtist=[]
settings=[]
vol=100

def genRec():
    global recId
    global recList
    global recTrack
    global recArtist    
    
    

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
            
    print(recTrack)
    results = sp.current_user_saved_tracks()
    likes=[]
    for idx, item in enumerate(results['items']):
        likes.append(results['items'][idx]['track']['id'])
    
    f = open('/home/seth/.navi/navify/icons/likes.pkl', 'wb')
    pickle.dump(likes, f)
    f.close()  

def search(string, cache, name):
    
    print("Searching youtube for the song...\n\n")    

    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q=string,
        type="video"
    )
    response = request.execute()    
    #print(response)
    #print(response['items'][0]['id']['videoId'])
    video=response['items'][0]['id']['videoId']
    print("Video name: " + str(response['items'][0]['snippet']['title']) + " Channel: " + str(response['items'][0]['snippet']['channelTitle']))
    subprocess.run(["mpv","-vo","null", "--input-ipc-server=/tmp/mpvsocket", "https://www.youtube.com/watch?v=" + video])
    
    f = open("/home/seth/.navi/navify/cache/" + str(cache) , "w")
    f.write("https://www.youtube.com/watch?v=" + video + ";" + fText + " " + str(len("https://www.youtube.com/watch?v=" + video)))
    f.close()
        
    
def playCache(cache):
    subprocess.run(["mpv","--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume="+str(vol), "--playlist=/home/seth/.navi/navify/cache/" + str(cache)]) 
    
c=0
genRec()

while loop=="true":
    if not exists("/home/seth/.navi/navify/pause.txt"):
        # Sets the global settings        
        if exists("/home/seth/.navi/navify/settings.pkl"):
            f = open('/home/seth/.navi/navify/settings.pkl', 'rb')
            settings = pickle.load(f)
            f.close()
            vol=settings[0]

        # Makes sure the take shouldn't be skipped
        if recId[c] != "skip":
            print("Now playing: " + str(recList[c] + " " + str(recId[c])))
            
            # Stores the track information so that the display can read it 
            # Track Name + Artist Name + Track Id + Name Section
            
            # Filters out non latin characters            
            fText=str(recTrack[c]) + " - " + str(recArtist[c])
            fText = re.sub(r'[^\x00-\x7f]',r'', fText)
            if len(fText) > 16:
                fText=fText+" | "
            
            # Stores the information for the display to read    
            info = [recTrack[c], recArtist[c], recId[c], fText]
            f = open('/home/seth/.navi/navify/info.pkl', 'wb')
            pickle.dump(info, f)
            f.close()  
            if exists('/home/seth/.navi/navify/cache/' + recId[c]):
                # Checks for ; in the file
                length=0

                if ";" in recId[c]:
                    
                    length = int(recId[c][len(recId[c])-3:])
                    recId[c]=recId[c][0:length] 
                playCache(recId[c])
            else:       
                search(recList[c], recId[c], fText)
            



            # Checks if the songs like state changed
            if exists('/home/seth/.navi/navify/like.pkl'):
                f = open("/home/seth/.navi/navify/like.pkl", 'rb')
                liked = pickle.load(f)
                f.close()
                if liked == 0:
                    sp.current_user_saved_tracks_add([recId[c]])
                else:
                    sp.current_user_saved_tracks_delete([recId[c]])
                os.remove("/home/seth/.navi/navify/like.pkl")
                    
            # Checks if there is a request to go back
            if not exists("/home/seth/.navi/navify/prev.txt"):
                c=c+1
            elif c != 0:
                if recId[c-1] == "skip" and c != 1:
                    c=c-1
                c=c-1
                os.remove("/home/seth/.navi/navify/prev.txt")
            else:
                os.remove("/home/seth/.navi/navify/prev.txt")
               
        else:
            c=c+1
                
        if c == 49:
            c=0
            genRec()


