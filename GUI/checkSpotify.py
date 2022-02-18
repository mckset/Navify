import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyOAuth

os.environ['SPOTIPY_CLIENT_ID']='481da7d376c747408b5ec25f609c193b'
os.environ['SPOTIPY_CLIENT_SECRET']='4ec619360c6e497a9ce1f126a3c10f93'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost'

scope = ["user-library-read", "user-library-modify"]
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
