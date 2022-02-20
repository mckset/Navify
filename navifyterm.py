import pickle
import subprocess
import random
import os
import sys
import re
from pynput import keyboard

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
    
def genList(): 
	global spotList
	global ID
	global listed
	global level
   
	# RESETS VALUES
	listed=[] 
	ID=[]
	spotName=[]
	sortID=[]
	sortListed=[]
	tempID=[]
	combinedList=[]    
	level=0

   	# Lists tracks in the Cache folder (Spotify Cache)
	tempID=next(walk(home + "cache/"), (None, None, []))[2]
	for i in range(len(tempID)):
		currentFile = subprocess.Popen(["cat", home + "cache/" + tempID[i]], stdout=subprocess.PIPE, text=True).communicate()[0]
		if ";" in currentFile:
			length=int(currentFile[len(currentFile)-3:])
			sortID.append(currentFile[0:length])
			sortListed.append((currentFile[length+1:len(currentFile)-3]))
			spotName.append(tempID[i])

	# Removes 'The' from the beginning of tracks to better sort
	for i in range(len(sortListed)):
		if "The ".lower() in sortListed[i][0:4].lower():
			sortListed[i] = sortListed[i][4:] + ", The"

	# Sorts the tracks alphabetically
	for i in range(len(sortID)):
		combinedList.append([sortListed[i],sortID[i], spotName[i]])    
	combinedList.sort()  

	# Stores the sorted values in the lists
	for i in range(len(sortID)):
		ID.append(combinedList[i][1])
		listed.append([combinedList[i][0], combinedList[i][2]])   

	# Adds "The " back into the track name
	for i in range(len(listed)):
		if ", The".lower() in listed[i][0].lower():
			listed[i][0] = "The " + listed[i][0][0:len(listed[i][0])-5]
	
	# Removes line breaks if they are at the end of the song      
	for i in range(len(listed)):
		if "\n" in listed[i]:
			listed[i][0]=listed[i][0][0:len(listed[i][0])-1]
	spotList.append("[PLAY ALL]")
	for i in range(len(listed)):
		spotList.append(listed[i][0])

	# Gets the liked tracks
	if exists(home + "icons/likes.pkl"):
		f = open(home + 'icons/likes.pkl', 'rb')
		likes = pickle.load(f)
		f.close()

def viewAll(path): 
	listOfFile = os.listdir(path)
	allFiles = list()
	for entry in listOfFile:
		fullPath = os.path.join(path, entry)
		if os.path.isdir(fullPath):
			allFiles = allFiles + viewAll(fullPath)
		else:
			allFiles.append(fullPath)
	return allFiles           
	
def viewAllCondense(l1, l2):
	global locTracks # NAMES OF THE SONGS
	global locPaths # LISTED PATH TO SONG WITH SONG NAMES
	global listed 
	global ID
	locTracks=[]
	locPaths=[]
	locID=[] # URLS AND PATHS TO SONGS
	tempSort1=[]
	tempSort2=[]

	for i in range(len(l1)):
		if ".wav" in l1[i] or ".ogg" in l1[i] or ".mp3" in l1[i]:
			locPaths.append(l1[i])
			locID.append(l1[i])
			x=0
			y=0
			for a in range(len(l1[i])):						
				if "/" in l1[i][a:a+1]:
					x=a
			locTracks.append(l1[i][x+1:len(l1[i])-4])
	for i in range(len(locTracks)):
		tempSort1.append([locTracks[i], locPaths[i], locID[i]])
	tempSort1.sort()
	
	locTracks=[]
	locPaths=[]
	locID=[] # URLS AND PATHS TO SONGS
	

	for i in range(len(l2)):
		locTracks.append(subprocess.Popen(["cat", l2[i]], stdout=subprocess.PIPE, text=True).communicate()[0])
		a=0
		for x in range(len(l2[i])):
			if "/" in l2[i][x:x+1]:
				a=x
		locID.append("https://www.youtube.com/watch?v=" + l2[i][a+1:])		
		locPaths.append(l2[i][0:a+1]+locTracks[len(locTracks)-1])		


	for i in range(len(locTracks)):
		tempSort2.append([locTracks[i], locPaths[i], locID[i]])
	tempSort2.sort()

	locTracks=["...", "", "[TRACKS]"]
	locPaths=["...", "", "[TRACKS]"]
	locID=["...", "", "[TRACKS]"] # URLS AND PATHS TO SONGS

	for i in range(len(tempSort1)):
		locTracks.append(tempSort1[i][0])		
		locPaths.append(tempSort1[i][1])		
		locID.append(tempSort1[i][2])

	for i in range(len(tempSort2)):
		locTracks.append(tempSort2[i][0])		
		locPaths.append(tempSort2[i][1])		
		locID.append(tempSort2[i][2])

	for i in range(len(locTracks)):
		if "\n" in locTracks[i]:
			locTracks[i] = locTracks[i][0:len(locTracks[i])-1]
	tempList=list(locTracks)

	for i in range(1,len(ID)):
		for x in range(len(locPaths)):
			if ID[i] == locID[x]:
				del locPaths[x]
				del locTracks[x]
				del locID[x]
				break

	for i in range(len(locTracks)):
		listed.append([locPaths[i], locTracks[i]])
		ID.append(locID[i])

	return tempList	

genList() 

#-------------------------------------------------
# MAIN LOOP
#-------------------------------------------------

def Player():
	global spotList
	global locTracks
	global locPaths
	
	# Default Values
	isPlaying=False # Set to True When a Song Gets Played
	path="" # Path to Local Songs
	level=0 # How Many Folders Down the Local Section is
	isCache=True # Set to true if the viewed folder is YouTube cache
	queue=["[CLEAR]", ""] # Queued songs 
	playing=""
	duration=1 # How long the song lasts
	current=1 # Current playtime position
	search=True # Is the search bar off
	play=False # State for the play button
	edit=False # Is the user going to edit a song
	editI=0 # Index of the song that is being edited in the list 'listed'
	editName="" # New name for the song
	time=0 # Count down to start moving the scrollbar again
	repeat=0 # is the player set to repeat
	shuffle=0 # Is the player set to shuffle
	prequeue=[] # Saved queue to be called when repeat is on
	vAll=False # Set to true when local is viewing all tracks
	cmd="" # Received command from taskbar
		  
	# Start of the Main Loop
	while True:
		keyDown = keyboard.Listener(on_press=events)
		
		# Networking
		try:
			if pN.is_alive() == False:
				print("test")
				pN.join()
				f = open(home + 'info.pkl', 'rb')
				cmd=pickle.load(f)[4]
				print(cmd)
				pN = Process(target=Listener, args=(), daemon=True)
				pN.start()
				cmd=""
		except:
			pN = Process(target=Listener, args=(), daemon=True)
			pN.start()


		# Progress bar stuff
		if isPlaying == True:
			try:
				duration = subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["get_property", "duration"] }'), stdout=subprocess.PIPE).stdout, text=True)
				for i in range(len(duration[8:])):
					if duration[i:i+1] == ',':
						duration=float(duration[8:i])
						break

				current = subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["get_property", "playback-time"] }'), stdout=subprocess.PIPE).stdout, text=True)
				for i in range(len(current[8:])):
					if current[i:i+1] == ',':
						current=float(current[8:i])
						break

				min = int(current/60)
				sec = int((current - min*60))
				if sec >= 10:
					current = str(min) + ":" + str(sec)
				else:
					current = str(min) + ":0" + str(sec)
				min = int(duration/60)
				sec = int((duration - min*60))
				if sec > 10:
					duration = str(min) + ":" + str(sec)
				else:
					duration = str(min) + ":0" + str(sec)
				current = current + "/" + duration
				
			except:
				pass
		
		# Resets after the song is finished		
		try:
			if isPlaying == True and p.is_alive() == False:
				p.join()
				isPlaying=False
		except:
			pass

		# END OF SONG WITH NO QUEUE EVENT    
		if len(queue) == 1 and isPlaying == False:          
			if repeat == 1:
				queue = ["[CLEAR]"]
				for i in range(len(prequeue)):
					queue.append(prequeue[i])
			play=False

		# Checks if there are songs queued
		if len(queue) > 1 and isPlaying == False:
			valid=0
			a=1
			tname=""
			if shuffle == 1 and len(queue) > 2:
				a = random.randrange(1,len(queue))

			for i in range(len(listed)):
				# Checks to see if the song is a local one
				skip=False		
				tname=""		
				if listed[i][1] == queue[a]:
					tname=listed[i][1]					
					skip = True						
				if listed[i][0] == queue[a] or skip==True:
					valid=1
					if skip==False:
					upDesktop(i, tname)
					p = Process(target=Play, args=(i, ), daemon=True)
					p.start()
					playing=queue[a]
					del queue[a]              
					play=True              
					isPlaying=True					
					break
			if valid==0:
				del queue[a]
 
def Events(keyDown):
	try:
		key = keyDown.char
	except:
		key = keyDown.name

		# PLAY/PAUSE
		if 'a' in key:    
			if play == True:
				subprocess.run([home + "scripts/display/pause.sh", "1"])
				play = False
			else:
				subprocess.run([home + "scripts/display/pause.sh", "2"])
				play = True
				
viewAllCondense(viewAll(home[0:len(home) - len(playerLoc)] +"/Music"), viewAll(home + "playCache")) # Appends local files to the listed array because I am too lazy to come up with a better solution
Player()
