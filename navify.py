# Navify GUI by Seth McKee
# Version 1.0: Oops! All bloat!

# Other programs
import subwindows

# System
import pickle
import subprocess
import random
import os
import sys
import re

from multiprocessing import Process
from multiprocessing.pool import ThreadPool
import multiprocessing as mp 
from os.path import exists
from os import walk

# Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# YouTube 
from urllib import request, parse
import requests
import io
from PIL import Image
import PySimpleGUI as sg

# Used to communicate with the taskbar
import socket 

# Fonts
defaultFont="Inter 40"
smallFont="Inter 32"

# GUI Colors
background="#ccccdc"
foreground="#99aabf"
accent="#99aabf"
highlight="#bbccdf"
hover=("","#67778f")
textc="#ffffff"
alpha=0.8

# PLAYER STUFF
ID=[] # Youtube URL to Songs
listed=[] # Name of Songs and the Spotify ID for it
spotList=[] # Name of Spotify Songs Only to List in GUI
localList=[] # Name of Local Songs Only to List in GUI
locPaths=[] # List of paths to local songs

likes=[] # List of Liked Songs

playerLoc=os.path.expanduser('~')
home=os. getcwd() + "/" # Location of python script

localMain=["ALL", "LOCAL CACHE","MUSIC"] # The Main Screen for the Local Section

# NAVIFY STUFF
header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
sp=""

#-------------------------------------------------
# SETUP FUNCTIONS
#-------------------------------------------------

def LoadSpotify():
	global sp
	try:
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=["user-library-read", "user-library-modify"]))
		sp.current_user_saved_tracks(1, 1) # Attempts to gets the first liked song to let the program if the user needs to input a redirect like
	except:
		print("Error: invalid Spotify settings.\n")
		SpotSetup()

def SpotSetup():
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
	LoadSpotify()

if exists(home + "keys.pkl"):
	key=[]
	f = open(home + "keys.pkl", 'rb')
	key = pickle.load(f)
	f.close()
	os.environ['SPOTIPY_CLIENT_ID']=key[0]
	os.environ['SPOTIPY_CLIENT_SECRET']=key[1]
	os.environ['SPOTIPY_REDIRECT_URI']=key[2]
	LoadSpotify()
else:	
	subprocess.run(["touch", home + "keys.pkl"])
	SpotSetup()
		
# Initializes missing files
def SetupSettings():
	if not exists(home + "settings.pkl"):
		f = open(home + "settings.pkl", 'wb')
		pickle.dump([100, 1], f)
		f.close()

	# Makes sure the recommended is readable
	if exists(home + "recommend.pkl"):
		try:
			f = open(home + "recommend.pkl", 'rb')
			x = pickle.load(f)
		except:
			os.remove(home + "recommend.pkl")
	if not exists(home + "recommend.pkl"):
		f = open(home + "recommend.pkl", 'wb')
		pickle.dump(likes[0:5], f)
		f.close()		

	try:
		f = open(home + "icons/state.pkl", 'wb')
		pickle.dump("2", f)
		f.close()
	except:
		os.remove(home + "icon/state.pkl")
		f = open(home + "icons/state.pkl", 'wb')
		pickle.dump("2", f)
		f.close()

	if not exists(home + "/playCache"):
		subprocess.run(["mkdir", home + "playCache"])
	if not exists(home + "/cache"):
		subprocess.run(["mkdir", home + "cache"])
	if not exists(home + "blacklist"):
		subprocess.run(["mkdir", home + "blacklist"])

def GenLikes():
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
	try:	
		f = open(home + "icons/likes.pkl", 'wb')
		pickle.dump(likes, f)
	except:
		os.remove(home + "icons/likes.pkl")
		f = open(home + "icons/likes.pkl", 'wb')
		pickle.dump(likes, f)
	f.close()
	return likes

likes=GenLikes()
SetupSettings()	   

if exists(home + "theme.pkl"):
	f = open(home + "theme.pkl", 'rb')
	t = pickle.load(f)
	f.close()
	foreground=t[0]
	background=t[1]
	textc=t[2]
	highlight=t[3]
	accent=t[4]
	hover=("",t[5])
	alpha=t[6]
else:
	f = open(home + "theme.pkl", 'wb')
	pickle.dump([foreground, background, textc, highlight, accent, "#67778f", alpha], f)
	f.close()

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
	print(track)
	subprocess.run(["mpv","--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume=" + str(vol), track])

def PlayAll(select, isCache):
	tracks=next(walk(select), (None, None, []))[2]
	tempName=[]
	tracks.sort()
	for i in range(len(tracks)):
		if isCache == True:
			tempName.append(subprocess.Popen(["cat", select + "/" + tracks[i]], stdout=subprocess.PIPE, text=True).communicate()[0])			
		else:
			if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]:
				tempName.append(tracks[i])
	return tempName

def UpLocal(select, isCache):
	newList=["..."]    

	if select == home + "playCache" or select == playerLoc +"/Music":
		newList.append("[ALL]")

	folders=next(walk(select), (None, None, []))[1]
	tracks=next(walk(select), (None, None, []))[2]

	if len(folders) > 0:
		for i in range(len(folders)):
			newList.append(folders[i])
		
	if isCache == False:
		tempTracks=[]
		for i in range(len(tracks)):
			if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]:
					tempTracks.append(tracks[i])
		tracks=list(tempTracks)

	if len(tracks) != 0:				
		newList.append("")
		newList.append("[TRACKS]")

		tempID=[]
		tempName=[]
		tracks.sort()
		for i in range(len(tracks)):
			if isCache == True:
				tempName.append(subprocess.Popen(["cat", select + "/" + tracks[i]], stdout=subprocess.PIPE, text=True).communicate()[0])			
				tempID.append("https://www.youtube.com/watch?v=" + tracks[i])
			else:
				if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]:
					tempName.append(tracks[i])
					tempID.append(select + "/" + tracks[i])
		tracks=[]

		for i in range(len(tempName)):
			tracks.append(tempName[i])
			if "\n" in tracks[i]:
				tracks[i] = tracks[i][0:len(tracks[i]) - 1]
			if isCache==False:
				if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]:
					tempName[i] = tempName[i][0:len(tempName[i])-4]
		for i in range(len(tracks)):
			newList.append(tracks[i])

	window["-LOCAL-"].update(values=newList)
	

def ViewAll(path): 
	listOfFile = os.listdir(path)
	allFiles = list()
	for entry in listOfFile:
		fullPath = os.path.join(path, entry)
		if os.path.isdir(fullPath):
			allFiles = allFiles + ViewAll(fullPath)
		else:
			allFiles.append(fullPath)
	return allFiles           
	
def ViewAllCondense(l1, l2):
	global listed 
	global ID
	global locPaths
	
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
	for i in range(len(locPaths)):
		if "\n" in locPaths[i]:
			locPaths[i] = locPaths[i][0:len(locPaths[i])-1]

	for i in range(len(locTracks)):
		for x in range(len(ID)):
			if locID[i] != ID[x]:
				listed.append([locPaths[i], locTracks[i]])
				ID.append(locID[i])
				break

	return tempList	

def KillMPV():
	mpv = subprocess.check_output(['grep', "tmp/mpvsocket"], stdin=subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE).stdout, text=True)	
	mpv=mpv[4:]
	for i in range(0,len(mpv)):
		if not " " in mpv[i:i+1]:
			mpv=mpv[i:]
			break
	for i in range(0, len(mpv)):
		if " " in mpv[i:i+1]:
			mpv=mpv[0:i]
			break
	subprocess.run(["kill", mpv]) 
	
def GenList(): 
	global spotList
	global ID
	global listed
	global level
   
	prevListed=[]

	# RESETS VALUES
	listed=[] 
	ID=[]
	spotName=[]
	sortID=[]
	sortListed=[]
	tempID=[]
	combinedList=[]    
	level=0
	spotList=[]

   	# Lists tracks in the Cache folder (Spotify Cache)
	tempID=next(walk(home + "cache/"), (None, None, []))[2]
	for i in range(len(tempID)):
		currentFile = subprocess.Popen(["cat", home + "cache/" + tempID[i]], stdout=subprocess.PIPE, text=True).communicate()[0]
		split=0
		for x in range(len(currentFile)):
			if '\n' in currentFile[x:x+1]:
				split=x
				break
		sortID.append(currentFile[0:split])
		prevListed.append(currentFile[split+1:])
		sortListed.append((currentFile[split+1:]).upper())
		spotName.append(tempID[i])

	# Removes 'The' from the beginning of tracks to better sort
	for i in range(len(sortListed)):
		if "THE " in sortListed[i][0:4]:
			sortListed[i] = sortListed[i][4:] + ", THE"

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
		
	for i in range(len(listed)):
		for x in range(len(prevListed)):
			if listed[i][0].lower() in prevListed[x].lower():
				listed[i][0] = prevListed[x]

	# Removes line breaks if they are at the end of the song      
	for i in range(len(listed)):
		if "\n" in listed[i]:
			listed[i][0]=listed[i][0][0:len(listed[i][0])-1]
	spotList.append("[PLAY ALL] (" + str(len(listed)) + ")")
	for i in range(len(listed)):
		spotList.append(listed[i][0])

GenList() 

def Navify():
	recList=[] 
	recId=[]
	recTrack=[]
	fText=""

	# Sets up the track list used to grab recommendations
	if exists(home + 'recommend.pkl'):
		f = open(home + 'recommend.pkl', 'rb')
		tracks = pickle.load(f)
		f.close()
	else:
		tracks = list(likes[0:4])
			    
	# Sets up the playlist to use based off of the first 5 tracks in the liked playlist
	rec=sp.recommendations(seed_tracks=tracks, limit=50)
    
	# Checks to see if a track is in the blacklist
	for i in range(0,49):
		if not exists(home + 'blacklist/' + str(rec['tracks'][i]['id'])):
			recList.append(str(rec['tracks'][i]['name']) + " - " + str(rec['tracks'][i]['artists'][0]['name']))
			recId.append(rec['tracks'][i]['id'])

    # Checks to see if a track is in the cache directory and caches it if not
	tracksName=[]    
	for i in range(0,len(recId)):
		#print(i)
		if not exists(home + "cache/" + recId[i]) and recId[i] != "skip":
			#fText=str(recTrack[i]) + " - " + str(recArtist[i])
			fText=str(recList[i])		
			fText = re.sub(r'[^\x00-\x7f]',r'', fText)
			name=fText
			for x in range(0,len(fText)):
				if " " in fText[x:x+1]:
					fText=fText[0:x] + "+" + fText[x+1:]  
			Search(recList[i], recId[i], name, fText)
	
	# Gets tracks info from cache
	for i in range(0,len(recId)):
		currentFile = subprocess.Popen(["cat", home + "cache/" + recId[i]], stdout=subprocess.PIPE, text=True).communicate()[0]
		split=0
		for x in range(len(currentFile)):
			if '\n' in currentFile[x:x+1]:
				split=x                   
		tracksName.append(currentFile[0:split]) # Appends track link
	return recList

def Search(string, cache, name, url):       
	req=request.Request("https://youtube.com/results?search_query=" + url, headers=header)
	U = request.urlopen(req)
	data = U.read().decode('utf-8')
    
	for i in range(0,len(data)):
		if "videoid" in data[i:i+7].lower() and not "videoids" in data[i:i+8].lower():
			video=data[i+10:i+21]
			break
    
	f = open(home + "cache/" + str(cache) , "w")
	f.write("https://www.youtube.com/watch?v=" + video + "\n" + name)
	f.close()
        			    
#-------------------------------------------------
# DEFINE MAIN WINDOW LAYOUT
#-------------------------------------------------

# Spotify Songs
SongList = [
	[
	sg.Button(image_filename=home + "icons/search.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SEARCH-"),
	sg.Text("Songs", background_color=background,  expand_x=True, k="SONGS"),
	sg.Button(image_filename=home + "icons/edit.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-EDIT-")
	],
	[
	sg.Listbox(values=spotList, background_color=foreground, font=defaultFont, text_color=textc, no_scrollbar=False, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-SONGS-")], 
	[
	sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, key="-INSEARCH-")
	]
]

# Local Files
Local = [
	[
	sg.Button(image_filename=home + "icons/add.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-ADD-"),
	sg.Text("Local", background_color=background, expand_x=True, k="LOCAL"),
	sg.Button(image_filename=home + "icons/playlist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAYLIST-")
	],
	[
	sg.Listbox(values=localMain, background_color=foreground, text_color=textc, no_scrollbar=False, size=(1,1), enable_events=True, expand_y=True, expand_x=True, key="-LOCAL-")
	] 
]

# Queued Songs
Queue = [
	[
	sg.Button(image_filename=home + "icons/navi.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-NAVIFY-"),
	sg.Text("Queue",background_color=background,  expand_x=True, k="QUEUE"),
	sg.Button(image_filename=home + "icons/settings.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SETTINGS-")
	],
	[
	sg.Listbox(values=["[CLEAR]"], background_color=foreground, text_color=textc, no_scrollbar=False, size=(1,1), enable_events=True, key="-QUEUE-", expand_y=True, expand_x=True)
	] 
]

# Play Bar
BottomBar = [
	[
	sg.Text(text="Now Playing: Nothing", size=(1,1), justification="left", font=smallFont, expand_x=True, background_color=foreground, key="-PLAYING-"),
	sg.Button(image_filename=home + "icons/nrepeat.png", enable_events=True ,mouseover_colors=hover, border_width=0, key="-REPEAT-"),
	sg.Button(image_filename=home + "icons/blacklist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-BLACKLIST-"),
	sg.Button(image_filename=home + "icons/prev.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PREV-"),
	sg.Button(image_filename=home + "icons/play.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAY-"),
	sg.Button(image_filename=home + "icons/next.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SKIP-"),
	sg.Button(image_filename=home + "icons/elike.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-LIKE-"),
	sg.Button(image_filename=home + "icons/nshuffle.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SHUFFLE-"),
	sg.Text("0:00/0:00", justification="right", font=smallFont, size=(1,1), expand_x=True, background_color=foreground, key="-TIME-")    
	]
]

# Sets the Layout for the Main Window
layout = [
	[
	#sg.Titlebar(title = "Navify", icon = "", text_color = textc, background_color = background, k="-TITLE-")
	],
	[
	sg.HorizontalSeparator()
	],
	[
	sg.Column(Local, expand_y=True,background_color=background,  expand_x=True, k="-DIV1-"), # Local Songs
	sg.VSeparator(color=None),
	sg.Column(SongList, expand_y=True,background_color=background,  expand_x=True, k="-DIV2-"), # Spotify Songs
	sg.VSeparator(color=None),
	sg.Column(Queue, expand_y=True, background_color=background, expand_x=True, k="-DIV3-") # Queued Songs
	],
	[
	sg.Slider(range=(0,1), default_value=0, enable_events=True, background_color=foreground, trough_color=foreground, orientation='h', disable_number_display=True, border_width = 1, expand_x=True, key="-BAR-") # Progress Bar
	],
	[
	sg.Column(BottomBar, background_color=background, expand_x=True, k="-DIV4-") # Play Bar
	]
]

# Create the window
window = sg.Window("Navify", 
		   layout, 
		   keep_on_top=False, 
		   force_toplevel=False, 
		   no_titlebar=False, 
		   resizable=False, 
		   auto_size_text=True, 
		   use_default_focus=True, 
		   alpha_channel=alpha, 
		   background_color=background, 
		   button_color=accent,
		   font=defaultFont,
		   element_justification='r',
		   text_justification="center",
		   return_keyboard_events=True,
		   border_depth=None,
		   finalize = True
		  )

def key_down(event): # Prevents the space key from selecting songs
	pass

#-------------------------------------------------
# MAIN LOOP
#-------------------------------------------------

def Player():
	global spotList
	global level
	global locPaths		  
	global likes

	# Default Values
	isPlaying=False # Set to True When a Song Gets Played
	isCache=False # Set to true if the viewed folder is YouTube cache
	navify=False # Set to True when the Navify event is called
	search=False # Is the search bar on
	play=False # State for the play button
	edit=False # Is the user going to edit a song
	repeat=False # is the player set to repeat
	shuffle=False # Is the player set to shuffle
	vAll=False # Set to true when local is viewing all tracks
	fullscreen=False
	
	level=0 # How Many Folders Down the Local Section is
	duration=1 # How long the song lasts
	current=1 # Current playtime position
	editI=0 # Index of the song that is being edited in the list 'listed'
	time=0 # Count down to start moving the scrollbar again
	
	path="" # Path to Local Songs
	playing=""
	cmd="" # Received command from taskbar
	
	queue=["[CLEAR]"] # Queued songs 
	queuePaths= [""] # Paths to local queued songs
	prequeue=[] # Saved queue to be called when repeat is on
	prequeuePaths = []
	prevSongs=[] # Previous songs, up to 100
	prevPaths = []
	tempQ=[]
	
	f = open(home + "settings.pkl", 'rb')
	settings=pickle.load(f)
	f.close()

	# Start of the Main Loop
	while True:
		event, values = window.read(timeout=100)

		# Resets after the song is finished		
		if isPlaying == True:
			try:
				if p.is_alive() == False:
					p.join()
					isPlaying=False
			except:
				pass	

		# Spacebar
		if event == "space:65" and search == False and edit == False:
			event="-PLAY-"

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

				if time == 0:
					window["-BAR-"].update(current*100, range=(0,duration*100))
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
				window["-TIME-"].update(current)
				
			except:
				pass

		# Grabbing the slider
		if event == "-BAR-" and isPlaying==True:
			time=200
			subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["set_property", "playback-time", ' + str(values["-BAR-"]/100) + '] }'), stdout=subprocess.PIPE).stdout, text=True)

		# LOCAL SONG EVENT
		if event == "-LOCAL-":
			if edit==False: # I still don't know how this works. I was tried 
				if level == 0:
					if values["-LOCAL-"][0] == localMain[1]:
						path = home + "playCache"
						isCache=True
						UpLocal(path, isCache)

					elif values["-LOCAL-"][0] == localMain[2] and level == 0:
						path = playerLoc +"/Music"
						isCache=False
						UpLocal(path, isCache)

					else:
						vAll=True
						path="all"
						locTracks = ViewAllCondense(ViewAll(playerLoc +"/Music"), ViewAll(home + "playCache"))
						window["-LOCAL-"].update(values=locTracks)
					level=level+1	
			
				# Goes up one level 
				if values["-LOCAL-"][0] == "..." and level != 0:
					level=level-1			
					if level == 0:
						window["-LOCAL-"].update(values=localMain)
					else:
						x=0
						for i in range(len(path)):
							if "/" in path[i:i+1]:
								x=i
						path=path[0:x]
						UpLocal(path, isCache)
					vAll=False
				
				if values["-LOCAL-"][0] == "[ALL]" and level == 1:				
					if isCache==False:
						locTracks = ViewAllCondense(ViewAll(playerLoc +"/Music"), [])
						window["-LOCAL-"].update(values=locTracks)
					else:
						locTracks = ViewAllCondense([], ViewAll(home + "playCache"))	
						window["-LOCAL-"].update(values=locTracks)
					path=path+"/ "
					vAll=True			
					level=level+1	
			
				# Opens folders
				if os.path.isdir(path + "/" + values["-LOCAL-"][0]) and level != 0 and len(values["-LOCAL-"][0]) > 0:
					path = path + "/" + values["-LOCAL-"][0]				
					UpLocal(path, isCache)
					level = level + 1

				else:

					# Queues a song 
					if vAll==False: # Especially this part. HOW?
						if values["-LOCAL-"][0] != "[TRACKS]": 					
							for i in range(1, len(listed)):
								if (listed[i][0] == path + "/" + values["-LOCAL-"][0]):
									queue.append(listed[i][1])
									queuePaths.append(listed[i][0])
									if repeat == True:
										prequeue.append(listed[i][1])
										prequeuePaths.append(listed[i][0])
									window["-QUEUE-"].update(values=queue)
									break
						else:
							tempName=[]
							tempName=PlayAll(path, isCache)
							for i in range(len(tempName)):					
								queue.append(tempName[i][0:len(tempName[i])-4])
								queuePaths.append(path+"/"+tempName[i])
								if repeat == True:
									prequeue.append(tempName[i][0:len(tempName[i])-4])	
									prequeuePaths.append(path+"/"+tempName[i])		

					# If all is active on main level				
					else:
						if values["-LOCAL-"][0] != "[TRACKS]":
							sel = window["-LOCAL-"].get_indexes()
							if len(sel) > 0:
								sel=sel[0]
								for x in range(1,len(listed)):
									if (listed[x][0] == locPaths[sel]):
										queue.append(listed[x][1])
										queuePaths.append(listed[x][0])
										if repeat == True:
											prequeue.append(listed[x][1])
											prequeuePaths.append(listed[x][0])		
											window["-QUEUE-"].update(values=queue)
										break 
						else:
							for i in range(3,len(locTracks)):					
								queue.append(locTracks[i])
								queuePaths.append(locPaths[i])
								if repeat == True:
									prequeue.append(locTracks[i])
									prequeuePaths.append(locPaths[i])
					window["-QUEUE-"].update(values=queue)

			if edit == True and level > 0:			
				for i in range(0, len(listed)):
					if ".wav" in str(values["-LOCAL-"][0]) or ".ogg" in str(values["-LOCAL-"][0]) or ".mp3" in str(values["-LOCAL-"][0]):
						if str(listed[i][1]) == str(values["-LOCAL-"][0][0:len(str(values["-LOCAL-"][0]))-4]):
							print(listed[i])
							subwindows.Edit(listed[i][1], ID[i], listed[i][0], 2)
							break
					else:
						if str(listed[i][1]) == str(values["-LOCAL-"][0]):					
							print(listed[i])
							a=0
							for x in range(len(listed[i][0])):
								if listed[i][0][x:x+1] == '/':
									a=x
							sendID=listed[i][0][0:a] + "/" + ID[i][32:]
							subwindows.Edit(listed[i][1], ID[i], sendID, 1)
							break
				event="-EDIT-"
				GenList()
				ViewAllCondense(ViewAll(playerLoc +"/Music"), ViewAll(home + "playCache"))				
				level=0
				isCache=False
				vAll=False
				window["-LOCAL-"].update(values=localMain)

		# SONG SELECTED EVENT
		if event == "-SONGS-":
			if edit == False:
				if "[PLAY ALL]" in values["-SONGS-"][0]:
					for i in range(1,len(spotList)):
						queue.append(spotList[i])
						queuePaths.append("")
						if repeat == True:
							prequeue.append(spotList[i])
							prequeuePaths.append("")
					window["-QUEUE-"].update(values=queue)
				else:
					# Checks if the song needs to be added to queue
					for i in range(len(listed)):
						if (listed[i][0] == values["-SONGS-"][0]):
							queue.append(listed[i][0])
							queuePaths.append("")
							if repeat == True:
								prequeue.append(listed[i][0])
								prequeuePaths.append("")
							window["-QUEUE-"].update(values=queue)
							break      
			if edit == True:
				for i in range(0, len(listed)):
					if (str(listed[i][0]) == str(values["-SONGS-"][0])):
						editI=i
						print(listed[i][1])			
						if i != 0:	
							subwindows.Edit(listed[i][0], ID[i], listed[i][1], 0)
						break
				GenList()
				window["-SONGS-"].update(values=spotList)

		# QUEUE Event
		if event == "-QUEUE-":
			if values["-QUEUE-"][0] == "[CLEAR]":
				if repeat==True:
					for i in range(1,len(queue)):
						for x in range(len(prequeue)):
							if prequeue[x] in queue[i]:
								del prequeue[x]
								del prequeuePaths[x]
								break
				queue=["[CLEAR]"]
				queuePaths=[""]
				window["-QUEUE-"].update(values=queue)
			else:
				for i in range(1,len(queue)):
					if queue[i] == str(values["-QUEUE-"][0]):
						if repeat == True:
							for x in range(len(prequeue)):
								if (prequeue[x] == queue[i]):
									del prequeue[x]
									del prequeuePaths[x]
									break
						del queue[i]
						del queuePaths[i]
						window["-QUEUE-"].update(values=queue)
						break

		# Append Navify results to queue
		try:
			tempQ=tempQ.get(0.05)
			GenList()
			window["-SONGS-"].update(values=spotList)
			for i in range(len(tempQ)):
				for x in range(len(ID)):
					if tempQ[i] == listed[x][0]:                
						queue.append(listed[x][0])
						queuePaths.append("")
						if repeat == True:
							prequeue.append(listed[x][0])
							prequeuePaths.append("")
						break
			window["-QUEUE-"].update(values=queue)
			window["-NAVIFY-"].update(disabled=False)
			tempQ=[]
		except:
			pass

		# END OF SONG WITH NO QUEUE EVENT    
		if len(queue) == 1 and isPlaying == False:          
			if repeat == True:
				queue = ["[CLEAR]"]
				queuePaths=[""]
				for i in range(len(prequeue)):
					queue.append(prequeue[i])
					queuePaths.append(prequeuePaths[i])
			else:
				window["-PLAY-"].update(image_filename=home + "icons/play.png")
				window["-PLAYING-"].update("Now Playing: Nothing")
				window["-TIME-"].update("0:00/0:00")
				window["-BAR-"].update(0, range=(0,1))
				play=False
			f = open("/home/seth/.navi/navify/icons/state.pkl", 'wb')
			pickle.dump("2", f)
			f.close()
						
		# Checks if there are songs queued
		if len(queue) > 1 and isPlaying == False:
			valid=0
			a=1
			tname=""
			if shuffle == True and len(queue) > 2:
				a = random.randrange(1,len(queue))

			for i in range(len(listed)):
				# Checks to see if the song is a local one
				skip=False		
				tname=""		
				if listed[i][0] == queuePaths[a]:
					tname=listed[i][1]		
					skip = True						
					window["-PLAYING-"].update("Now Playing: " + tname)
				if listed[i][0] == queue[a] or skip==True:
					valid=1
					if skip==False:
						window["-PLAYING-"].update("Now Playing: " + listed[i][0])
						prevSongs.append(listed[i][0])
						prevPaths.append("")
						currentTrack = listed[i][1]
					else:
						prevSongs.append(listed[i][1])
						prevPaths.append(listed[i][0])
						currentTrack = "none"
					p = Process(target=Play, args=(i, ), daemon=True)
					p.start()
					playing=queue[a]
					del queue[a]   
					del queuePaths[a]           
					window["-QUEUE-"].update(values=queue)
					play=True
					window["-PLAY-"].update(image_filename=home + "icons/pause.png")                
					isPlaying=True					
					break
			if valid==0:
				del queue[a]
				window["-QUEUE-"].update(values=queue)
			f = open("/home/seth/.navi/navify/icons/state.pkl", 'wb')
			pickle.dump("1", f)
			f.close()

		# Repeat
		if event == "-REPEAT-":
			if repeat == False:
				window["-REPEAT-"].update(image_filename=home + "icons/repeat.png")
				repeat=True
				if isPlaying == True:
					prequeue.append(playing)
					for i in range(1,len(queue)):
						prequeue.append(queue[i])
			else:
				window["-REPEAT-"].update(image_filename=home + "icons/nrepeat.png")
				repeat=False
				prequeue=[]

		# Shuffle
		if event == "-SHUFFLE-":
			if shuffle == 0:
				window["-SHUFFLE-"].update(image_filename=home + "icons/shuffle.png")
				shuffle=True
			else:
				window["-SHUFFLE-"].update(image_filename=home + "icons/nshuffle.png")
				shuffle=False
		# BLACKLIST
		if event == "-BLACKLIST-" and isPlaying == True and currentTrack !="none":
			subprocess.Popen(["mv", home + "cache/" + currentTrack, home + "blacklist/" ])
			GenList()
			window["-SONGS-"].update(values=spotList)
			event="-SKIP-"

		# LIKE
		if event == "-LIKE-" and isPlaying == True and currentTrack != "none":
			liked=1            
			for i in (range(0,len(likes))):
				if currentTrack == likes[i]:
					liked=0
					window["-LIKE-"].update(image_filename=home + "icons/elike.png")
					sp.current_user_saved_tracks_delete([currentTrack])
					break
			if liked == 1:  
				sp.current_user_saved_tracks_add([currentTrack])
				window["-LIKE-"].update(image_filename=home + "icons/like.png")            
			likes = GenLikes()
			f = open(home + "icons/likes.pkl", 'wb')
			pickle.dump(likes, f)
			f.close()
    
		# SEARCH
		if event == "-SEARCH-":
			if search == True:
				search=False
				window["-INSEARCH-"].update("",disabled=True)
				window["-SONGS-"].update(values=spotList)
				window["-SEARCH-"].update(button_color=accent)
			else:
				search=True
				window["-SEARCH-"].update(button_color=highlight)        
				window["-INSEARCH-"].update(disabled=False)
		if search == False:
				window.bind('<Key>', key_down)        


		# EDIT CLICKED EVENT
		if event == "-EDIT-":
			if edit == False:
				edit = True
				window["-EDIT-"].update(button_color=highlight)
				editI=""
			else:
				window["-EDIT-"].update(button_color=accent)
				edit = False

		# Search Box
		if event == "-INSEARCH-" and len(values["-INSEARCH-"]) > 0:
			newList=[]
			for i in range(1,len(spotList)):
				if values["-INSEARCH-"].lower() in spotList[i].lower():
					newList.append(spotList[i])
			tempSort=[]
			l = len(values["-INSEARCH-"].lower())+1
			for x in range(1,len(values["-INSEARCH-"].lower())+1):	
				for i in range(len(newList)):
					if values["-INSEARCH-"].lower()[0:l-x] == newList[i].lower()[0:l-x]:
						valid=1
						for a in range(len(tempSort)):
							if newList[i] == tempSort[a]:
								valid=0
								break
						if valid == 1:							
							tempSort.append(newList[i])
			for i in range(len(newList)):
				valid=0
				for x in range(len(tempSort)):
					if newList[i] == tempSort[x]:
						valid=1	
						break				
				if valid == 0:
					tempSort.append(newList[i])
			window["-SONGS-"].update(values=tempSort)

		# NAVIFY EVENT
		if event == "-NAVIFY-" and navify == False: 
			pool = ThreadPool(processes=1)
			tempQ = pool.apply_async(Navify)
			window["-NAVIFY-"].update(disabled=True)

		# Skip/Next
		if event == "-SKIP-" and isPlaying == True:
			KillMPV()    

		# PLAY/PAUSE
		if event == "-PLAY-" and isPlaying == True:    
			f = open("/home/seth/.navi/navify/icons/state.pkl", 'wb')			
			if play == True:
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "pause", true]}'), stdout=subprocess.PIPE).stdout, text=True)
				play = False
				window["-PLAY-"].update(image_filename=home + "icons/play.png") 
				pickle.dump("2", f)  
			else:
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "pause", false]}'), stdout=subprocess.PIPE).stdout, text=True)
				play = True
				window["-PLAY-"].update(image_filename=home + "icons/pause.png")
				pickle.dump("1", f)   
			f.close()
		
		# PREVIOUS
		if event == "-PREV-" and len(prevSongs) > 0:
			tempQ = list(queue[1:])
			tempQP = list(queuePaths[1:])
			queue=["[CLEAR]"]
			queuePaths=[""]
			if len(prevSongs) > 1:
				if isPlaying == True:
					queue.append(prevSongs[len(prevSongs)-2])			
					queue.append(prevSongs[len(prevSongs)-1])
					queuePaths.append(prevPaths[len(prevPaths) -2])
					queuePaths.append(prevPaths[len(prevPaths)-1])
					del prevSongs[len(prevSongs)-1]
					del prevSongs[len(prevSongs)-1]
					del prevPaths[len(prevPaths)-1]
					del prevPaths[len(prevPaths)-1]
				else:
					queue.append(prevSongs[len(prevSongs)-1])
					queuePaths.append(prevPaths[len(prevPaths)-1])
					del prevSongs[len(prevSongs)-1]
					del prevPaths[len(prevPaths)-1]
				KillMPV()
			elif isPlaying == False:
				queue.append(prevSongs[0])
				queuePaths.append(prevPaths[0])
				del prevPaths[0]
				del prevSongs[0]							
		
			for i in range(len(tempQ)):
				queue.append(tempQ[i])
				queuePaths.append(tempQP[i])

		# 
		# SUB WINDOWS
		#

		# Add SONG WINDOW
		if event == "-ADD-":
			if settings[1] == 1:
				subwindows.Add(sp, "spot")
			else:
				subwindows.Add(sp, "you")	
			GenList()
			ViewAllCondense(ViewAll(playerLoc +"/Music"), ViewAll(home + "playCache"))
			window["-LOCAL-"].update(values=localMain)
			window["-SONGS-"].update(values=spotList)

		# PLAYLIST BUTTON EVENT
		if event == "-PLAYLIST-":
			temp=[]
			temp=subwindows.Playlist(listed)
			for i in range(len(temp)):
				queue.append(temp[i])
				queuePaths.append("")
				if repeat == True:
					prequeue.append(temp[i])
					prequeuePaths.append("")
			window["-QUEUE-"].update(values=queue)   
         
		# SETTINGS        
		if event == "-SETTINGS-":
			subwindows.Settings(sp)
			settings = pickle.load(open(home + "settings.pkl", 'rb'))
			f = open(home + "theme.pkl", 'rb')
			t = pickle.load(f)
			f.close()
			f=t[0]
			b=t[1]
			tc=t[2]
			hi=t[3]
			a=t[4]
			ho=t[5]
			alf=t[6]

			window["-SONGS-"].update(background_color=f)
			window["-INSEARCH-"].update(background_color=f)		
			window["-LOCAL-"].update(background_color=f)
			window["-QUEUE-"].update(background_color=f)
			window["-PLAYING-"].update(background_color=f)
			window["-TIME-"].update(background_color=f)
			window["-BAR-"].update(background_color=f, trough_color=f)
		
			window.update(text_color = tc, background_color = background)

		if event == "-MAX-":
			if fullscreen == False:
				window.Maximize()	
				fullscren = True
			else:
				window.Normal()
				fullscreen = False

		if event == "-MIN-":
			window.Minimize()

		if event == sg.WIN_CLOSED or event == "-CLOSE-":
			break

		if time != 0:
			time=time-100
		
ViewAllCondense(ViewAll(playerLoc +"/Music"), ViewAll(home + "playCache")) # Appends local files to the listed array because I am too lazy to come up with a better solution

Player() # Starts the GUI


#-------------------------------------------------
# END AND CLEANUP
#-------------------------------------------------
f = open("/home/seth/.navi/navify/icons/state.pkl", 'wb')
pickle.dump("2", f)
f.close()
window.close() # Closes the window
KillMPV()      
