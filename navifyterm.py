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
		# Networking
		try:
			if pN.is_alive() == False:
				print("test")
				pN.join()
				f = open(home + 'info.pkl', 'rb')
				cmd=pickle.load(f)[4]
				print(cmd)
				if cmd == "blacklist":
					event="-BLACKLIST-"
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
		
		# Resets after the song is finished		
		try:
			if isPlaying == True and p.is_alive() == False:
				p.join()
				window["-LIKE-"].update(image_filename=home + "icons/elike.png")
				isPlaying=False
		except:
			pass

		# END OF SONG WITH NO QUEUE EVENT    
		if len(queue) == 1 and isPlaying == False:          
			if repeat == 1:
				queue = ["[CLEAR]"]
				for i in range(len(prequeue)):
					queue.append(prequeue[i])
			window["-PLAY-"].update(image_filename=home + "icons/play.png")
			window["-PLAYING-"].update("Now Playing: Nothing")
			window["-TIME-"].update("0:00/0:00")
			window["-BAR-"].update(0, range=(0,1))
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
					window["-PLAYING-"].update("Now Playing: " + tname)
				if listed[i][0] == queue[a] or skip==True:
					valid=1
					if skip==False:
						window["-PLAYING-"].update("Now Playing: " + listed[i][0])
					upDesktop(i, tname)
					p = Process(target=Play, args=(i, ), daemon=True)
					p.start()
					playing=queue[a]
					del queue[a]              
					window["-QUEUE-"].update(values=queue)
					play=True
					window["-PLAY-"].update(image_filename=home + "icons/pause.png")                
					isPlaying=True					
					break
			if valid==0:
				del queue[a]
				window["-QUEUE-"].update(values=queue)
 
def Events():
	keyDown = keyboard.Listener(on_press=GetKey)
	# Grabbing the slider
		if event == "-BAR-" and isPlaying==True:
			time=200
			subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["set_property", "playback-time", ' + str(values["-BAR-"]/100) + '] }'), stdout=subprocess.PIPE).stdout, text=True)

		# LOCAL SONG EVENT
		if event == "-LOCAL-":
			if edit==False: # I still don't know how this works
				if level == 0:
					if values["-LOCAL-"][0] == localMain[1]:
						path = home + "playCache"
						isCache=True
						updateLocal(path, isCache)

					elif values["-LOCAL-"][0] == localMain[2] and level == 0:
						path = home[0:len(home) - len(playerLoc)] +"/Music"
						isCache=False
						updateLocal(path, isCache)

					else:
						vAll=True
						path="all"
						locTracks = viewAllCondense(viewAll(home[0:len(home) - len(playerLoc)] +"/Music"), viewAll(home + "playCache"))
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
						updateLocal(path, isCache)
					vAll=False
				
				if values["-LOCAL-"][0] == "[ALL]" and level == 1:				
					if isCache==False:
						locTracks = viewAllCondense(viewAll(home[0:len(home) - len(playerLoc)] +"/Music"), [])
						window["-LOCAL-"].update(values=locTracks)
					else:
						locTracks = viewAllCondense([], viewAll(home + "playCache"))	
						window["-LOCAL-"].update(values=locTracks)
					path=path+"/ "
					vAll=True			
					level=level+1	
			
				# Opens folders
				if os.path.isdir(path + "/" + values["-LOCAL-"][0]) and level != 0:
					path = path + "/" + values["-LOCAL-"][0]				
					updateLocal(path, isCache)
					level = level + 1

				else:

					# Plays a song 
					if vAll==False: # Especially this part. HOW?
						if values["-LOCAL-"][0] != "[TRACKS]": 					
							for i in range(1, len(listed)):
								if (listed[i][0] == path + "/" + values["-LOCAL-"][0]):
									queue.append(listed[i][1])
									if repeat == 1:
										prequeue.append(listed[i][1])
									window["-QUEUE-"].update(values=queue)
									break
						else:
							tempName=[]
							tempName=playAll(path, isCache)
							for i in range(len(tempName)):					
								queue.append(tempName[i])
								if repeat == 1:
									prequeue.append(tempName[i])
		
					# If all is active on main level				
					else:
						if values["-LOCAL-"][0] != "[TRACKS]":
							for i in range(len(locTracks)):
								if values["-LOCAL-"][0] == locTracks[i]: 					
									for x in range(1,len(listed)):
										if (listed[x][0] == locPaths[i]):
											queue.append(listed[x][1])
											
											if repeat == 1:
												prequeue.append(listed[x][1])
											window["-QUEUE-"].update(values=queue)
											break 
									break
						else:
							for i in range(3,len(locTracks)):					
								queue.append(locTracks[i])
								if repeat == 1:
									prequeue.append(locTracks[i])
					window["-QUEUE-"].update(values=queue)

			if edit == True:
				window["-INSEARCH-"].update(disabled=False)
				window["-INSEARCH-"].update(str(values["-LOCAL-"][0]))
				for i in range(0, len(listed)):
					if (str(listed[i]) == str(values["-LOCAL-"][0])):
						editI=i
						break
			
		# SONG SELECTED EVENT
		if event == "-SONGS-":
			if edit == False:
				if values["-SONGS-"][0] == "[PLAY ALL]":
					for i in range(1,len(spotList)):
						queue.append(spotList[i])
						window["-QUEUE-"].update(values=queue)
				else:
					# Checks if the song needs to be added to queue
					for i in range(len(listed)):
						if (listed[i][0] == values["-SONGS-"][0]):
							queue.append(listed[i][0])
							if repeat == 1:
								prequeue.append(listed[i][0])
							window["-QUEUE-"].update(values=queue)
							break      
			if edit == True:
				window["-INSEARCH-"].update(disabled=False)
				window["-INSEARCH-"].update(str(values["-SONGS-"][0]))
				for i in range(0, len(listed)):
					if (str(listed[i][0]) == str(values["-SONGS-"][0])):
						editI=i
						break
		# QUEUE Event
		if event == "-QUEUE-":
			if values["-QUEUE-"][0] == "[CLEAR]":
				if repeat==1:
					for i in range(1,len(queue)):
						for x in range(len(prequeue)):
							if prequeue[x] in queue[i]:
								del prequeue[x]
								break
				queue=["[CLEAR]"]
				window["-QUEUE-"].update(values=queue)
			else:
				for i in range(1,len(queue)):
					if queue[i] == str(values["-QUEUE-"][0]):
						if (repeat == 1):
							for x in range(len(prequeue)):
								if (prequeue[x] == queue[i]):
									del prequeue[x]
									break
						del queue[i]
						window["-QUEUE-"].update(values=queue)
						break
			# Add song event
		if event == "-ADD-":
			Add()
			genList()
			window["-LOCAL-"].update(values=localMain)
            
		# Repeat
		if event == "-REPEAT-":
			if repeat == 0:
				window["-REPEAT-"].update(image_filename=home + "icons/repeat.png")
				repeat=1
				if isPlaying == True:
					prequeue.append(playing)
					for i in range(1,len(queue)):
						prequeue.append(queue[i])
			else:
				window["-REPEAT-"].update(image_filename=home + "icons/nrepeat.png")
				repeat=0
				prequeue=[]

		# Shuffle
		if event == "-SHUFFLE-":
			if shuffle == 0:
				window["-SHUFFLE-"].update(image_filename=home + "icons/shuffle.png")
				shuffle=1
			else:
				window["-SHUFFLE-"].update(image_filename=home + "icons/nshuffle.png")
				shuffle=0
		# BLACKLIST
		if event == "-BLACKLIST-" and isPlaying == True and currentTrack !="none":
			subprocess.Popen(["mv", home + "cache/" + currentTrack, home + "blacklist/" ])
			genList()
			window["-SONGS-"].update(values=spotList)
			event="-SKIP-"

		# Like
		if event == "-LIKE-" and isPlaying == False and currentTrack != "none":
			if exists(home + "icons/likes.pkl"):
				f = open( home + 'icons/likes.pkl', 'wb')
				liked=1            
				for i in (range(0,len(likes))):
					if currentTrack == likes[i]:
						liked=0
						window["-LIKE-"].update(image_filename=home + "icons/elike.png")
						sp.current_user_saved_tracks_delete([track])
						del likes[i]
						break
				if liked == 1:  
					likes.append(current)
					sp.current_user_saved_tracks_add([track])
					window["-LIKE-"].update(image_filename=home + "icons/like.png")            
				pickle.dump(likes, f)
				f.close()
                
		# Search
		if event == "-SEARCH-" and edit == False:
			if (search == False):
				search=True
				window["-INSEARCH-"].update("",disabled=True)
				window["-SONGS-"].update(values=spotList)
				window["-SEARCH-"].update(button_color="#99aabf")
			else:
				search=False
				window["-SEARCH-"].update(button_color="#bbccdf")        
				window["-INSEARCH-"].update(disabled=False)
        
		# EDIT CLICKED EVENT
		if event == "-EDIT-":
			if edit == False:
				edit = True
				search=True  
				window["-SEARCH-"].update(button_color="#99aabf")
				window["-EDIT-"].update(button_color="#bbccdf")
				editName=""
				editI="999999999999999999999999999999999"
			else:
				window["-EDIT-"].update(button_color="#99aabf")
				edit = False
				if len(editName) == 0:
					window["-INSEARCH-"].update("")
					window["-INSEARCH-"].update(disabled=True)
				if len(editName) > 0 and editName != listed[editI]:
					if editI < len(spotList):
						spotSID=" "
						for i in range(0,len(tempID)):
							text=subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + tempID[i]], stdout=subprocess.PIPE, text=True).communicate()[0]                   
							if ID[editI] in text:
								spotSID=tempID[i]
								break

						text=subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/"
     + spotSID], stdout=subprocess.PIPE, text=True).communicate()[0]
						f=open("/home/seth/.navi/navify/cache/" + spotSID, 'w')
						l=text[len(text)-3:]                
						f.write(text[0:int(l)] + ";" + editName + " " + l)
						f.close()
						window["-INSEARCH-"].update("")
						window["-INSEARCH-"].update(disabled=True)
						spotList[editI] = editName
						listed[editI] = editName
						genList()                
						window["-SONGS-"].update(values=spotList)
					else:
						edit = False
						if "\n" in ID[editI]:
							ID[editI] = ID[editI][0:len(ID[editI])-1]
						link=ID[editI][len(ID[editI])-11:]
						for i in range(len(locID)):                
							if link in locID[i]:
								if exists(home + locID[i]):
									f=open(home + locID[i], 'w')               
									f.write(editName)
									f.close()
									window["-INSEARCH-"].update("")
									window["-INSEARCH-"].update(disabled=True)
									for i in range(0, len(localList)):
										if localList[i] == listed[editI]:                            
											listed[editI] = editName
											localList[i] = editName
											break                
									window["-LOCAL-"].update(values=folders)
									break

		# PLAYLIST BUTTON EVENT
		if event == "-PLAYLIST-":
			temp=[]
			temp=Playlist()
			for i in range(len(temp)):
				queue.append(temp[i])
			window["-QUEUE-"].update(values=queue)

		# Search Box
		if event == "-INSEARCH-":
			if edit == False:
				newList=[]
				for i in range(len(spotList)):
					if values["-INSEARCH-"].lower() in spotList[i].lower():
						newList.append(spotList[i])
				window["-SONGS-"].update(values=newList)
			if edit == True:
				editName=str(values["-INSEARCH-"])

		# NAVIFY EVENT
		if event == "-NAVIFY-": 
			tempList = navify()
			genList()
			window["-SONGS-"].update(values=spotList)
			window["-PLAY-"].update(image_filename=home + "icons/pause.png")
			for i in range(len(tempList)):
				for x in range(len(ID)):
					if tempList[i] == ID[x]:                
						queue.append(listed[x][0])
						if (repeat == 1):
							prequeue.append(listed[x][0])
						break
			window["-QUEUE-"].update(values=queue)

		# SETTINGS        
		if event == "-SETTINGS-":
			Settings()

		# PLAYALL
		if event == "-LAYALL-":
			for i in range(0,len(listed)):
				queue.append(listed[i][0])

		# Skip/Next
		if event == "-SKIP-" and isPlaying == True:
			process = subprocess.Popen([home + "scripts/display/killmpv.sh"], stdout=subprocess.PIPE, text=True)
			process=process.communicate()[0][4:]
			window["-PLAY-"].update(image_filename=home + "icons/pause.png")
			play=True
			for i in range(len(process)):
				if not " " in process[i:i+1]:
					process=process[i:]
					break
			for i in range(0, len(process)):
				if " " in process[i:i+1]:
					process=process[0:i]
					break
			subprocess.run(["kill", process])      
			            

		# PLAY/PAUSE
		if event == "-PLAY-":    
			if play == True:
				subprocess.run([home + "scripts/display/pause.sh", "1"])
				play = False
				window["-PLAY-"].update(image_filename=home + "icons/play.png")   
			else:
				subprocess.run([home + "scripts/display/pause.sh", "2"])
				play = True
				window["-PLAY-"].update(image_filename=home + "icons/pause.png")  
	
viewAllCondense(viewAll(home[0:len(home) - len(playerLoc)] +"/Music"), viewAll(home + "playCache")) # Appends local files to the listed array because I am too lazy to come up with a better solution
Player()
