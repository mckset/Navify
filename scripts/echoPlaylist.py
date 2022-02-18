import os
import pickle
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Sets environmental variables
os.environ['SPOTIPY_CLIENT_ID']='481da7d376c747408b5ec25f609c193b'
os.environ['SPOTIPY_CLIENT_SECRET']='4ec619360c6e497a9ce1f126a3c10f93'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'

scope = ["user-library-read", "user-library-modify"]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#print(sp.current_user_playlists(limit=50, offset=0))
sp.current_user_saved_tracks_delete(tracks=["0AEPHw67BDBpgSLq1VhS4O"])
results = sp.current_user_saved_tracks(limit=50)
print(results['items'][1]['track']['id'])
#print(results['items']['track'][2]['id'])
likes=[]
for idx, item in enumerate(results['items']):
    likes.append(results['items'][idx]['track']['id'])
    

 
for idx, item in enumerate(results['items']):
            track = item['track']
            select=""
            print(select + str(idx), track['artists'][0]['name'], " – ", track['name'] + " : " + track['id'])
  
        
"""
results = sp.current_user_saved_tracks()

for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

i=input("Track: ")
print(results['items'][int(i)])
print(" ")
print(results['items'][int(i)]['track']['id'])
"""
