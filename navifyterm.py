import pickle
import subprocess
import random
import os
import sys
import re

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from urllib import request, parse
import requests

from multiprocessing import Process

# File checking
from os.path import exists
from os import walk

# Used to communicate with the taskbar
import socket 

# PLAYER STUFF
ID=[] # Youtube URL to Songs
listed=[] # Name of Songs and the Spotify ID for it
spotList=[] # Name of Spotify Songs Only to List in GUI
localList=[] # Name of Local Songs Only to List in GUI

likes=[] # List of Liked Songs

playerLoc="/.navi/navify/"
home=os.path.expanduser('~') + playerLoc # Users Home Path

localMain=["ALL", "LOCAL CACHE","MUSIC"] # The Main Screen for the Local Section

# NAVIFY STUFF
header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
sp=""

# LOCAL SERVER STUFF
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
port=6969
s.bind(('', port))

#-------------------------------------------------
# SETUP FUNCTIONS
#-------------------------------------------------

def loadSpotify():
	global sp
	try:
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=["user-library-read", "user-library-modify"]))
		sp.current_user_saved_tracks(1, 1) # Attempts to gets the first liked song to let the program if the user needs to input a redirect like
	except:
		print("Error: invalid Spotify settings.\n")
		spotSetup()

def spotSetup():
	global sp
	key=[]
	inp=""
	while len(inp) == 0:
		inp = input("Please enter your Spotify Client ID: ")
	key.append(inp)
	inp=""
	while len(inp) == 0:
		inp = input("Please enter your Spotify Client Secret Key: ")
	key.append(inp)
	inp=""
	while len(inp) == 0:
		inp = input("Please enter yout Spotify Redirect URI: ")
	key.append(inp)
	f = open(home + "keys.pkl", 'wb')
	pickle.dump(key, f)
	f.close()
	os.environ['SPOTIPY_CLIENT_ID']=key[0]
	os.environ['SPOTIPY_CLIENT_SECRET']=key[1]
	os.environ['SPOTIPY_REDIRECT_URI']=key[2]
	loadSpotify()

if exists(home + "keys.pkl"):
	key=[]
	f = open(home + "keys.pkl", 'rb')
	key = pickle.load(f)
	f.close()
	os.environ['SPOTIPY_CLIENT_ID']=key[0]
	os.environ['SPOTIPY_CLIENT_SECRET']=key[1]
	os.environ['SPOTIPY_REDIRECT_URI']=key[2]
	loadSpotify()
else:
	spotSetup()
		
# Initializes setting files
def setupSettings():
	if not exists(home + "info.pkl"):
		f = open(home + "info.pkl", 'wb')
		pickle.dump(["","","",""])
		f.close()
	if not exists(home + "settings.pkl"):
		f = open(home + "settings.pkl", 'wb')
		pickle.dump([100])
		f.close()
	if not exists(home + "recommend.pkl"):
		f = open(home + "recommend.pkl", 'wb')
		pickle.dump(genLikes()[0:5])
		f.close()		
		
def genLikes():
	likes=[]
	results=[]
	x=0
	while True: 
		results.append(sp.current_user_saved_tracks(20, x))
		x+=20
		if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
		    break
	for i in range(0,len(results)):
		for x in range(0,len(results[i]['items'])):
			likes.append(results[i]['items'][x]['track']['id'])
	return likes

setupSettings()	   
likes=genLikes()		    
#-------------------------------------------------
# DEFINE MAIN FUNCTIONS
#-------------------------------------------------

def Play(x):
	track=ID[x]
	trackID=ID[x]    
	vol=100

	if exists(home + "settings.pkl"):
		f = open(home + 'settings.pkl', 'rb')
		settings = pickle.load(f)
		f.close()
	vol=settings[0]

	subprocess.run(["mpv","--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume=" + str(vol), track])

def playAll(select, isCache):
	tracks=next(walk(select), (None, None, []))[2]
	tempName=[]
	tracks.sort()
	for i in range(len(tracks)):
		if isCache == True:
			tempName.append(subprocess.Popen(["cat", select + "/" + tracks[i]], stdout=subprocess.PIPE, text=True).communicate()[0])			
		else:
			if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]:
				tempName.append(tracks[i])
	for i in range(len(tempName)):

		if isCache==False:
			if ".wav" in tempName[i] or ".ogg" in tempName[i] or ".mp3" in tempName[i]:
				tempName[i] = tempName[i][0:len(tempName[i])-4]
	return tempName


def upDesktop(x, alt):
	global currentTrack

	# Dumps the info so the desktop can read it
	valid=0
	name=listed[x][0]
	if len(alt) > 0:
		name=alt
	print("Now Playing: " + name)
	print(ID[x])
	fname=name
	
	if "\n" in name:
		name=name[:len(name)-1]
		fname=name
	name = re.sub(r'[^\x00-\x7f]',r'', name)

	if len(name) > 16:
		name = str(name)[0:len(name)] + " | "

		valid=1
		info = [fname, "", listed[x][1], name, ""]
		f = open(home + 'info.pkl', 'wb')
		pickle.dump(info, f)
		f.close()
		currentTrack=(str(listed[x][1]))
		for c in range(0,len(likes)):
				if (listed[x][1] == likes[c]):
					window["-LIKE-"].update(image_filename=home + "icons/like.png")
					break          

	if valid == 0:
		currentTrack = "none"
		info = [fname, "", "", name, ""]
		f = open(home + 'info.pkl', 'wb')
		pickle.dump(info, f)
		f.close()
    
