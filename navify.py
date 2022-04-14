# Navify GUI
# Version 2.0: Window to a New World

# Other programs
import subwindows

# System
import pickle
import subprocess
import random
import os
import sys
import time as t

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

# Fonts
defaultFont=("Mono", "20")
smallFont=("Mono", "16")
scroll = 13

# GUI Colors
background="#ccccdc"
foreground="#99aabf"
accent="#99aabf"
highlight="#bbccdf"
hover=("","#67778f")
textc="#ffffff"
alpha=1

# PLAYER STUFF
ID=[] # Youtube URL to Songs
listed=[] # Name of Songs and the Spotify ID for it
spotList=[] # Name of Spotify Songs Only to List in GUI
localList=[] # Name of Local Songs Only to List in GUI
locPaths=[] # List of paths to local songs

likes=[] # List of Liked Songs

home=os.path.expanduser('~')
playerHome=os. getcwd() + "\\" # Location of python script
localMusic = home + "\\Music"
mpvLoc=''

localMain=["ALL", "LOCAL CACHE","MUSIC"] # The Main Screen for the Local Section

# NAVIFY STUFF
header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
sp=""

#-------------------------------------------------
# SETUP FUNCTIONS
#-------------------------------------------------

# Checks if all the dependencies exist and creates missing files
def SetupSettings():
	global background
	global foreground
	global accent
	global highlight
	global hover
	global textc
	global alpha
	global defaultFont
	global smallFont
	global localMusic
	global scroll
	global mpvLoc

	err=""
	if not exists(playerHome + "icons"):
		err = "The 'icons' folder is missing from " + playerHome + ". Please make sure the folder is in the right location."

	if len(err) > 0:
		window = sg.Window("ERROR", 
		  layout = [[sg.Text(err, text_color="#ff0000", background_color="#000000",  expand_x=True)]], 
		   resizable=True,
		   alpha_channel=1, 
		   background_color="#000000",
		   font=defaultFont,
		   element_justification='r',
		   text_justification="center",
		   finalize = True
		  )
		window.read()
		window.close()
		sys.exit()

	if not exists(playerHome + "\\playCache"):
		os.system("mkdir " + playerHome + "playCache")
	if not exists(playerHome + "\\cache"):
		os.system("mkdir " + playerHome + "cache")
	if not exists(playerHome + "blacklist"):
		os.system("mkdir " + playerHome + "blacklist")
	if not exists(playerHome + "playlists"):
		os.system("mkdir " + playerHome + "playlists")
	
	if exists(playerHome + "theme.pkl"):
		f = open(playerHome + "theme.pkl", 'rb')
		t = pickle.load(f)
		f.close()
		foreground=t[0]
		background=t[1]
		textc=t[2]
		highlight=t[3]
		accent=t[4]
		hover=("",t[5])
		alpha=t[6]
		defaultFont=(t[7], t[8])
		smallFont = (t[7], t[9])
		scroll = int(t[10])
	else:
		pickle.dump([foreground, background, textc, highlight, accent, "#67778f", alpha, "Mono", "20", "16", "13"], open(playerHome + "theme.pkl", 'wb'))

	if not exists(playerHome + "settings.pkl"):
		pickle.dump([100, 1, home + "\\Music", ""], open(playerHome + "settings.pkl", 'wb'))
	if not exists(localMusic):
		print("WARNING: " + home + "\\Music does not exist. Please enter the path to local songs in the settings menu") 

	settings = pickle.load(open(playerHome + "settings.pkl", 'rb'))

	while not exists(settings[3] + "\\mpv.exe"):	
		setWindow = sg.Window("Enter Path to MPV", 
		  layout = [[sg.Text("Location of MPV", text_color=textc, background_color=background,  expand_x=True),sg.Input(default_text=settings[3], text_color=textc, background_color=foreground, disabled_readonly_background_color = highlight, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-SMPV-")],[sg.Button("Submit", enable_events=True, mouseover_colors=hover, border_width=0, key="-SSUBMIT-", expand_x=True)]], 
		    background_color=background, 
 		   	button_color=accent,
			resizable=True,
   		   	font=defaultFont,
		   	text_justification="left"
		  	)
		while True:
			event, values = setWindow.read()
			
			if event == sg.WIN_CLOSED:
				setWindow.close()
				sys.exit()
			if event == "-SSUBMIT-":    
				setWindow.close()
				break
			settings[3] = values["-SMPV-"]
		if settings[3][len(settings[3])-1] == "\\":
			settings[3] = settings[3][0:len(settings[3])-1]
		pickle.dump(settings, open(playerHome + "settings.pkl", 'wb'))
	mpvLoc=settings[3]
	localMusic = settings[2]

SetupSettings()	
e=0
def setupLayout():
	layout = [
		[
		sg.Text("Spotify Client ID:", text_color=textc, background_color=background,  expand_x=True),
		sg.Input(default_text=key[0], text_color=textc, background_color=foreground, disabled_readonly_background_color = highlight, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-SCID-")
		],
		[
		sg.Text("Spotify Client Secret Key:", text_color=textc, background_color=background,  expand_x=True),
		sg.Input(default_text=key[1], text_color=textc, background_color=foreground, disabled_readonly_background_color = highlight, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-SSID-")
		],
		[
		sg.Text("Spotify Redirect URI:", text_color=textc, background_color=background,  expand_x=True),
		sg.Input(default_text=key[2], text_color=textc, background_color=foreground, disabled_readonly_background_color = highlight, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-SRURI-")
		],
		[
		sg.Button("Submit", enable_events=True, mouseover_colors=hover, border_width=0, key="-SSUBMIT-", expand_x=True)
		]
	]
	return layout

def LoadSpotify():
	global sp
	try:
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=["user-library-read", "user-library-modify", "playlist-read-private"])) # read - get recommended; modify - change like statues; read-private - get weekly playlist
		sp.current_user_saved_tracks(1, 1) # Attempts to gets the first liked song to let the program if the user needs to input a redirect link
	except:
		print("Error: invalid Spotify settings.\n")
		SpotSetup()
		if e == 1:
			return
e=0
def SpotSetup():
	global sp
	global key
	global e
	spotWindow = sg.Window(
			"Enter Spotify Values", 
			setupLayout(), 
		  	background_color=background, 
 		   	button_color=accent,
			resizable=False,
   		   	font=defaultFont,
		   	text_justification="left"
		  	)	
	cid=key[0]
	csid=key[1]
	ruri=key[2]
	while True:
		event, values = spotWindow.read()
		if event == sg.WIN_CLOSED:
			spotWindow.close()
			e=1
			return
		if event == "-SSUBMIT-":    
			spotWindow.close()
			break
		cid = values["-SCID-"]
		csid = values["-SSID-"]
		ruri = values["-SRURI-"]
	key=[cid, csid, ruri]
	pickle.dump(key, open(playerHome + "keys.pkl", 'wb'))
	os.environ['SPOTIPY_CLIENT_ID']=key[0]
	os.environ['SPOTIPY_CLIENT_SECRET']=key[1]
	os.environ['SPOTIPY_REDIRECT_URI']=key[2]
	LoadSpotify()

if exists(playerHome + "keys.pkl"):
	try:
		key = pickle.load(open(playerHome + "keys.pkl", 'rb'))
		os.environ['SPOTIPY_CLIENT_ID']=key[0]
		os.environ['SPOTIPY_CLIENT_SECRET']=key[1]
		os.environ['SPOTIPY_REDIRECT_URI']=key[2]
		LoadSpotify()
	except:
		if e == 0:
			SpotSetup()
		else:
			sys.exit()
else:	
	os.system("echo '' >> " + playerHome + "keys.pkl")
	SpotSetup()
		
# Gets the Discover Weekly Playlist id
playlists = sp.current_user_playlists()['items']
plIDS=[]
plNames=[]
for i in range(len(playlists)):
	plIDS.append(playlists[i]['id'])
	plNames.append(playlists[i]['name'])
plNames.append("Close")

def CacheLikes(cache):
	layout = [
		[
		sg.Text("(1/" + str(len(cache)) + ") Caching: " + cache[0][1], text_color=textc, background_color=foreground,  expand_x=True, key="-LTEXT-")
		]
	]
	likeWindow = sg.Window(
			"Caching Liked Songs", 
			layout, 
		  	background_color=foreground, 
			resizable=False,
   		   	font=defaultFont,
		   	text_justification="left"
		  	)
	for i in range(len(cache)):
		event, values = likeWindow.read(timeout = 100)
		if event == sg.WIN_CLOSED:    
			likeWindow.close()
			sys.exit()
			break
		if i != len(cache)-1:
			likeWindow["-LTEXT-"].update("(" + str(i+2) + "/" + str(len(cache)) + ") Caching: " + cache[i+1][1])
		try:
			print("Caching: " + cache[i][1])
		except:
			print("Language not supported. Please install a font that supports the language for liked song #" + str(i))			
		url = cache[i][1]
		for y in range(len(url)): # Removes spaces to search
			if " " in url[y:y+1]:
				url=url[0:y] + "+" + url[y+1:]
		Search("", cache[i][0], cache[i][1], url)
	likeWindow.close()	


def GenLikes():
	likes=[]
	results=[]
	cache = []
	x=0

	while True: 
		results.append(sp.current_user_saved_tracks(20, x))
		x+=20
		if len(sp.current_user_saved_tracks(20, x)['items']) == 0:
		    break

	for i in range(len(results)):
		for x in range(len(results[i]['items'])):
			likes.append(results[i]['items'][x]['track']['id'])

			# Caches a liked song
			for a in range(len(likes)):
				if not exists(playerHome + "cache\\" + likes[a]):
					cache.append([likes[x+(20*i)], results[i]['items'][x]['track']['name'] + " - " + results[i]['items'][x]['track']['artists'][0]['name']])

					
	if not exists(playerHome + "recommend.pkl") and len(likes) > 0:
		pickle.dump([likes[0]], open(playerHome + "recommend.pkl", 'wb'))	
	elif len(likes) == 0:
		window = sg.Window("ERROR", 
		  layout = [[sg.Text("No tracks have been liked. Navify can still function but the recommended songs button will not work", text_color="#ff0000", background_color="#000000",  expand_x=True)]], 
		   resizable=True,
		   alpha_channel=1, 
		   background_color="#000000",
		   font=defaultFont,
		   element_justification='r',
		   text_justification="center",
		   finalize = True
		  )
		window.read()
		window.close()
	if len(cache) > 0:
		CacheLikes(cache)
	return likes

#-------------------------------------------------
# FUNCTIONS THAT GET CALLED DURING THE MAIN LOOP
#-------------------------------------------------

def PlayAll(select, isCache): # Plays all songs
	tracks=next(walk(select), (None, None, []))[2]
	tempName=[]
	for i in range(len(tracks)):
		if isCache == True:
			tempName.append(os.popen("type " + select + "\\" + tracks[i]).read())		
		else:
			if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]or ".mid" in tracks[i]:
				tempName.append(tracks[i])
	tempName.sort()
	return tempName

def UpLocal(select, isCache):
	if "..." in select:
		return
	newList=["..."]    

	if select == playerHome + "playCache" or select == localMusic:
		newList.append("[ALL]")
	folders=next(walk(select), (None, None, []))[1]
	tracks=next(walk(select), (None, None, []))[2]
	tracks.sort()	
	folders.sort()

	if len(folders) > 0:
		for i in range(len(folders)):
			newList.append(folders[i])
		
	if isCache == False:
		tempTracks=[]
		for i in range(len(tracks)):
			if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i] or ".mid" in tracks[i]:
				tempTracks.append(tracks[i])
		tracks=list(tempTracks)

	if len(tracks) != 0:				
		newList.append("")
		newList.append("[TRACKS]")
		tempName=[] # Used to sort cached songs

		for i in range(len(tracks)):
			if isCache == True:
				tempName.append(os.popen("type " + select + "\\" + tracks[i]).read())		
			else:
				newList.append(tracks[i])
		if len(tempName) > 0:
			tempName.sort()
			for i in range(len(tempName)):
				newList.append(tempName[i])
	window["-LOCAL-"].update(values=newList)
	
def ViewAll(path): 
	try:
		listOfFile = os.listdir(path)
		allFiles = list()
		for entry in listOfFile:
			fullPath = os.path.join(path, entry)
			if os.path.isdir(fullPath):
				allFiles = allFiles + ViewAll(fullPath)
			else:
				allFiles.append(fullPath)
		return allFiles           
	except:
		return []	

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
		if ".wav" in l1[i] or ".ogg" in l1[i] or ".mp3" in l1[i] or ".mid" in l1[i]:
			locPaths.append(l1[i])
			locID.append(l1[i])
			x=0
			for a in range(len(l1[i])):						
				if "\\" in l1[i][len(l1[i]) - a:]:
					x=len(l1[i]) - a
					break
			locTracks.append(l1[i][x+1:len(l1[i])-4])
	for i in range(len(locTracks)):
		tempSort1.append([locTracks[i], locPaths[i], locID[i]])
	tempSort1.sort()
	
	locTracks=[]
	locPaths=[]
	locID=[] # URLS AND PATHS TO SONGS
	
	for i in range(len(l2)):
		locTracks.append(os.popen("type " + l2[i]).read())
		a=0
		for x in range(len(l2[i])):
			if "\\" in l2[i][len(l2[i]) - x:]:
				a=len(l2[i]) - x
				break
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

	for i in range(len(locPaths)):
		if "\n" in locPaths[i]:
			locPaths[i] = locPaths[i][0:len(locPaths[i])-1]
	if len(ID) > 0:
		for i in range(len(locTracks)):
			for x in range(len(ID)):
				if locID[i] != ID[x]: # Checks to make sure it is only appending unique songs
					listed.append([locPaths[i], locTracks[i]])
					ID.append(locID[i])
					break
	else:
		for i in range(len(locPaths)):
			listed.append([locPaths[i], locTracks[i]])
			ID.append(locID[i])
	return locTracks

def KillMPV():
	try:
		os.system('echo quit >\\\\.\\pipe\\mpvsocket')
		while exists("output.txt"):
			os.system("del output.txt")
	except:
		pass

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
	tempID=next(walk(playerHome + "cache\\"), (None, None, []))[2]
	for i in range(len(tempID)):
		currentFile = subprocess.Popen(["type", playerHome + "cache\\" + tempID[i]], shell=True, stdout=subprocess.PIPE, text=True).communicate()[0]
		sortID.append(currentFile[0:43])
		prevListed.append(currentFile[44:])
		sortListed.append((currentFile[44:]).upper())
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
		
	# Returns the name back to the way it was
	for i in range(len(listed)):
		for x in range(len(prevListed)):
			if listed[i][0].lower() == prevListed[x].lower():
				listed[i][0] = prevListed[x]
				break

	spotList.append("[PLAY ALL] (" + str(len(listed)) + ")")
	for i in range(len(listed)):
		spotList.append(listed[i][0])

	if exists(localMusic):
		ViewAllCondense(ViewAll(localMusic), ViewAll(playerHome + "playCache")) # Appends local files to the listed array because I am too lazy to come up with a better solution
	else:
		ViewAllCondense([], ViewAll(playerHome + "playCache")) 

def getPlaylistSongs(selID):
	plTracks=[]
	plID=[] 
	p = sp.playlist_items(selID)			
	
	for i in range(len(p['items'])):
		if not exists(playerHome + 'blacklist/' + p['items'][i]['track']['id']):
			plTracks.append(p['items'][i]['track']['name'] + " - " + p['items'][i]['track']['album']['artists'][0]['name'])
			plID.append(p['items'][i]['track']['id'])

	checkCache(plTracks, plID)
	return plTracks				

def Navify():
	recList=[] 
	recId=[]
	tracks = pickle.load(open(playerHome + 'recommend.pkl', 'rb'))
			    
	# Sets up the playlist to use based off of the first 5 tracks in the liked playlist
	rec=sp.recommendations(seed_tracks=tracks, limit=50)
	   
	# Checks to see if a track is in the blacklist
	for i in range(len(rec['tracks'])):
		if not exists(playerHome + 'blacklist\\' + str(rec['tracks'][i]['id'])):
			recList.append(str(rec['tracks'][i]['name']) + " - " + str(rec['tracks'][i]['artists'][0]['name']))
			recId.append(rec['tracks'][i]['id'])
	checkCache(recList, recId)	
	return recList

def checkCache(songs, ids):
	fText=""

	# Checks to see if a track is in the cache directory and caches it if not  
	for i in range(0,len(ids)):
		if not exists(playerHome + "cache\\" + ids[i]):
			print(i)
			fText=str(songs[i])		
			name=fText
			for x in range(0,len(fText)):
				if " " in fText[x:x+1]:
					fText=fText[0:x] + "+" + fText[x+1:]  
			Search(songs[i], ids[i], name, fText)

def Search(string, cache, name, url):
	req=request.Request("https://youtube.com/results?search_query=" + parse.quote(url), headers=header)
	U = request.urlopen(req)
	data = U.read().decode('utf-8')
	for i in range(0,len(data)):
		if "videoid" in data[i:i+7].lower() and not "videoids" in data[i:i+8].lower():
			video=data[i+10:i+21]
			break

	f = open(playerHome + "cache\\" + str(cache) , "w", encoding='utf-8')
	f.write("https://www.youtube.com/watch?v=" + video + "\n" + name)
	f.close()
	
likes=GenLikes()
GenList() 
		
def ReloadNavify(queue, name, liked):
	SetupSettings()
	# Create the window
	window = sg.Window("Navify", 
		   layout(queue, name, liked), 
		   resizable=True,
		   alpha_channel=alpha, 
		   background_color=background, 
		   button_color=accent,
		   font=defaultFont,
		   element_justification='r',
		   text_justification="center",
		   return_keyboard_events=True,
		   finalize = True,
		   size=(1080,480)
		  )
	return window

#-------------------------------------------------
# DEFINE MAIN WINDOW LAYOUT
#-------------------------------------------------
def layout(queue, current, like):
	# Spotify Songs
	SongList = [
		[
		sg.Button(image_filename=playerHome + "icons\\search.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SEARCH-"),
		sg.Text("Songs", text_color=textc, background_color=background,  expand_x=True),
		sg.Button(image_filename=playerHome + "icons\\edit.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-EDIT-")
		],
		[
		sg.Listbox(values=spotList, background_color=foreground, font=defaultFont, text_color=textc, no_scrollbar=False, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-SONGS-")], 
		[
		sg.Input(text_color=textc, background_color=foreground, disabled_readonly_background_color = highlight, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, key="-INSEARCH-")
		]
	]

	# Local Files
	Local = [
		[
		sg.Button(image_filename=playerHome + "icons\\add.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-ADD-"),
		sg.Text("Local", background_color=background,text_color=textc,  expand_x=True),
		sg.Button(image_filename=playerHome + "icons\\playlist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAYLIST-")
		],
		[
		sg.Listbox(values=localMain, background_color=foreground, text_color=textc, no_scrollbar=False, size=(1,1), enable_events=True, expand_y=True, expand_x=True, key="-LOCAL-")
		] 
	]

	# Queued Songs
	Queue = [
		[
		sg.Button(image_filename=playerHome + "icons\\navi.png", right_click_menu=[[""], plNames], enable_events=True, mouseover_colors=hover, border_width=0, key="-NAVIFY-"),
		sg.Text("Queue",text_color=textc, background_color=background,  expand_x=True),
		sg.Button(image_filename=playerHome + "icons\\settings.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SETTINGS-")
		],
		[
		sg.Listbox(values=queue, background_color=foreground, text_color=textc, no_scrollbar=False, size=(1,1), enable_events=True, key="-QUEUE-", expand_y=True, expand_x=True)
		] 
	]

	# Play Bar
	BottomBar = [
		[
		sg.Text(text="Now Playing: " + current, text_color=textc, size=(1,1), justification="left", font=smallFont, expand_x=True, background_color=foreground, key="-PLAYING-"),
		sg.Button(image_filename=playerHome + "icons\\nrepeat.png", enable_events=True ,mouseover_colors=hover, border_width=0, key="-REPEAT-"),
		sg.Button(image_filename=playerHome + "icons\\blacklist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-BLACKLIST-"),
		sg.Button(image_filename=playerHome + "icons\\prev.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PREV-"),
		sg.Button(image_filename=playerHome + "icons\\play.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAY-"),
		sg.Button(image_filename=playerHome + "icons\\next.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SKIP-"),
		sg.Button(image_filename=playerHome + "icons\\elike.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-LIKE-"),
		sg.Button(image_filename=playerHome + "icons\\nshuffle.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SHUFFLE-"),
		sg.Text("0:00/0:00", justification="right", text_color=textc, font=smallFont, size=(1,1), expand_x=True, background_color=foreground, key="-TIME-")    
		]
	]

	# Sets the Layout for the Main Window
	layout = [
		[
		sg.Column(Local, expand_y=True,background_color=background,  expand_x=True), # Local Songs
		sg.VSeparator(color=foreground),
		sg.Column(SongList, expand_y=True,background_color=background,  expand_x=True), # Spotify Songs
		sg.VSeparator(color=foreground),
		sg.Column(Queue, expand_y=True, background_color=background, expand_x=True) # Queued Songs
		],
		[
		sg.Slider(range=(0,1), default_value=0, enable_events=True, background_color=foreground, trough_color=foreground, orientation='h', disable_number_display=True, border_width = 1, expand_x=True, key="-BAR-") # Progress Bar
		],
		[
		sg.Column(BottomBar, background_color=background, expand_x=True) # Play Bar
		]
	]
	return layout

# Create the window
window = sg.Window("Navify", 
	   layout(["[CLEAR]"], "Nothing", "elike.png"), 
	   resizable=True,
	   alpha_channel=alpha, 
	   background_color=background, 
	   button_color=accent,
	   font=defaultFont,
	   element_justification='r',
	   text_justification="center",
	   return_keyboard_events=True,
	   finalize = True,
	   size=(1080,480)
	  )

#-------------------------------------------------
# MAIN LOOP
#-------------------------------------------------

def Player():
	global level
	global locPaths		  
	global likes
	global window
	global localMusic

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
	isPrev=False # Tells the player if the previous button was pushed and to ignore the repeat function if so
	seek=False # If the player seeks 
	
	level=0 # How Many Folders Down the Local Section is
	duration=1 # How long the song lasts
	current=1 # Current playtime position
	editI=0 # Index of the song that is being edited in the list 'listed'
	time=0 # Count down to start moving the scrollbar again
	timeS=0 # Controls how fast scrolling text should change	
	oldLen=0 # The length of the previous search to prevent the player from constantly updating
	playTime=0 # Time state of when the song starts playing to determine current time 

	path="" # Path to Local Songs
	tempName = "" # Something
	name="" # I think this is the name of the song
	namePath="" # The path to name 
	liked="" # Something to do with likes

	queue=["[CLEAR]"] # Queued songs 
	queuePaths= [""] # Paths to local queued songs
	prequeue=[] # Saved queue to be called when repeat is on
	prequeuePaths = []
	prevSongs=[] # Previous songs, up to 100
	prevPaths = []
	tempQ=[]
	
	settings=pickle.load(open(playerHome + "settings.pkl", 'rb'))

	# Start of the Main Loop
	while True:
		event, values = window.read(timeout=100)

		if event == sg.WIN_CLOSED:
			window.close() # Closes the window
			break
	
		window["-INSEARCH-"].SetFocus(force = False) # Prevents keyboard inputs from accidentally activating events

		try: # Stops shortcuts from working when typing
			if ":" in event:
				if search == True or edit == True:
					event=""		
		except:
			pass

		# Resets after the song is finished		
		if isPlaying == True:
			try:
				if p.is_alive() == False:
					p.join()
					isPlaying=False
					window["-PLAYING-"].update("Now Playing: Something")
			except:
				pass	
		else:
			if exists("output.txt"):
				isPlaying=True
			
		if len(name) >= int(window["-PLAYING-"].get_size()[0] / 10) - scroll: # Scrolling text stuff
			timeS = timeS + 1
			if int(window["-PLAYING-"].get_size()[0] / 10) - scroll > 5:
				if timeS >= 6: # Frequency of the scrolling
					if len(tempName) == 0:
						tempName = name + " | "
					tempName = tempName[1:] + tempName[0] 				
					window["-PLAYING-"].update("Now Playing: " + tempName)
					timeS = 0
			else:
				window["-PLAYING-"].update(name)
		elif len(tempName) != 0:
			tempName = ""
			timeS = 0
			window["-PLAYING-"].update("Now Playing: " + name)

		# Key '<'
		if event == ",":
			event = "-PREV-"
		# Things that happen when a song is playing (Progress bar and keyboard inputs)
		if isPlaying == True:			
			try:						
				if len(duration) == 0:
					os.system('echo print-text ${duration} >\\\\.\\pipe\\mpvsocket')
					duration = os.popen("type output.txt").read()
					try:
						duration=duration[len(duration)-9:]
						x=float(duration[0])
						#print("Accepted: " + duration)
						duration =str(int(duration[0:2]) * 60 + int(duration[3:5]) * 60 + int(duration[6:]))
						playTime=t.time()
						
					except:
							duration=''
				else:
					# KEYBOARD EVENTS
					if event == " ": # Spacebar
						event="-PLAY-"

					if event == ".": # Key '>'
						event = "-SKIP-"

					if event == "Up:38": # Arrows Up and Down
						settings[0] = settings[0] + 2
						
						if settings[0] > 150:
							settings[0] = 150
						os.system('echo set volume ' + str(settings[0]) + ' >\\\\.\\pipe\\mpvsocket')
						f = open(playerHome + "settings.pkl", 'wb')
						pickle.dump(settings, f)
						f.close()
					if event == "Down:40":
						settings[0] = settings[0] - 2
						if settings[0] < 0:
							settings[0] = 0
						os.system('echo set volume ' + str(settings[0]) + ' >\\\\.\\pipe\\mpvsocket')
						f = open(playerHome + "settings.pkl", 'wb')
						pickle.dump(settings, f)
						f.close()

					if event == "Right:39": # Left and Right arrow key events
						playTime = playTime - 5
						current=current + 5
						os.system('echo seek 5 >\\\\.\\pipe\\mpvsocket')
						seek=True
					if event == "Left:37":
						current = current - 5 
						if current <= 0:
							playTime = playTime + (5 + current)
						else:
							playTime = playTime + 5
						os.system('echo seek -5 >\\\\.\\pipe\\mpvsocket')
						seek=True
					if play == True or seek == True:
						seek=False
						# PROGRESS BAR STUFF
						current = float(t.time() - playTime)
						if time == 0:
							window["-BAR-"].update(int(current*100), range=(0,int(duration)*100))
						min = int(current/60)
						sec = int((current - min*60))
						if sec >= 10:
							cur = str(min) + ":" + str(sec)
						else:
							cur = str(min) + ":0" + str(sec)
						min = int(int(duration)/60)
						sec = int((int(duration) - min*60))
						if sec >= 10:
							dur = str(min) + ":" + str(sec)
						else:
							dur = str(min) + ":0" + str(sec)
						window["-TIME-"].update(cur + "/" + dur)
					else:
						playTime = t.time() - current # Updates playTime to keep the current time correct
						
						
			except Exception as e:
				pass

			# Grabbing the slider
			if event == "-BAR-":
				time=200 # How long to wait before the program automatically moves the slider again
				os.system('echo set playback-time ' + str(values["-BAR-"]/100) + ' >\\\\.\\pipe\\mpvsocket')
				playTime = t.time() - float(values["-BAR-"]/100)

		# LOCAL SONG EVENT
		if event == "-LOCAL-" and len(values["-LOCAL-"][0]) > 0:
			if edit==False: # I still don't know how this works. I was tried 
				if level == 0:
					if values["-LOCAL-"][0] == localMain[1]:
						path = playerHome + "playCache"
						isCache=True
						UpLocal(path, isCache)

					elif values["-LOCAL-"][0] == localMain[2] and level == 0 and exists(localMusic):
						path = localMusic
						isCache=False
						UpLocal(path, isCache)

					else:
						vAll=True
						path="all"
						if exists(localMusic):
							locTracks = ViewAllCondense(ViewAll(localMusic), ViewAll(playerHome + "playCache"))
						else:
							locTracks = ViewAllCondense([], ViewAll(playerHome + "playCache"))
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
							if "\\" in path[i:i+1]:
								x=i
						path=path[0:x]
						UpLocal(path, isCache)
					vAll=False
				
				if values["-LOCAL-"][0] == "[ALL]" and level == 1:				
					if isCache==False:
						locTracks = ViewAllCondense(ViewAll(localMusic), [])
						window["-LOCAL-"].update(values=locTracks)
					else:
						locTracks = ViewAllCondense([], ViewAll(playerHome + "playCache"))	
						window["-LOCAL-"].update(values=locTracks)
					path=path+"\\ "
					vAll=True			
					level=level+1	
			
				# Opens folders
				if os.path.isdir(path + "\\" + values["-LOCAL-"][0]) and level != 0 and len(values["-LOCAL-"][0]) > 0 and values["-LOCAL-"][0] != "...":
					path = path + "\\" + values["-LOCAL-"][0]				
					UpLocal(path, isCache)
					level = level + 1

				else:

					# Queues a song 
					if vAll==False: # Especially this part. HOW?
						if values["-LOCAL-"][0] != "[TRACKS]": 					
							for i in range(1, len(listed)):
								if (listed[i][0] == path + "\\" + values["-LOCAL-"][0]):
									queue.append(listed[i][1])
									queuePaths.append(listed[i][0])
									if repeat == True:
										prequeue.append(listed[i][1])
										prequeuePaths.append(listed[i][0])
									window["-QUEUE-"].update(values=queue)
									break
						else: # Play all tracks in local folder
							tempName=[]
							tempName=PlayAll(path, isCache)
							for i in range(len(tempName)):					
								queue.append(tempName[i])
								queuePaths.append(path+"\\"+tempName[i])
								if repeat == True:
									prequeue.append(tempName[i])	
									prequeuePaths.append(path+"\\"+tempName[i])		

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

			if edit == True and level > 0 and str(values["-LOCAL-"][0]) != "..." and str(values["-LOCAL-"][0]) != "[TRACKS]" and str(values["-LOCAL-"][0]) != "[ALL]" and len(str(values["-LOCAL-"][0])) > 0:
				r=0			
				for i in range(0, len(listed)):
					if ".wav" in str(values["-LOCAL-"][0]) or ".ogg" in str(values["-LOCAL-"][0]) or ".mp3" in str(values["-LOCAL-"][0]) or ".mid" in str(values["-LOCAL-"][0]):
						if str(listed[i][1]) == str(values["-LOCAL-"][0][0:len(str(values["-LOCAL-"][0]))-4]):
							r=subwindows.Edit(listed[i][1], ID[i], listed[i][0], 2)
							break
					else:
						if str(listed[i][1]) == str(values["-LOCAL-"][0]):					
							a=0
							for x in range(len(listed[i][0])):
								if listed[i][0][x:x+1] == '\\':
									a=x
							sendID=listed[i][0][0:a] + "\\" + ID[i][32:]
							r=subwindows.Edit(listed[i][1], ID[i], sendID, 1)
							break
				if r == 1:
					GenList()
					if exists(localMusic):
						ViewAllCondense(ViewAll(localMusic), ViewAll(playerHome + "playCache"))				
					else:
						ViewAllCondense([], ViewAll(playerHome + "playCache"))						
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
					for i in range(len(listed)): # Checks if the song needs to be added to queue
						if (listed[i][0] == values["-SONGS-"][0]):
							queue.append(listed[i][0])
							queuePaths.append("")
							if repeat == True:
								prequeue.append(listed[i][0])
								prequeuePaths.append("")
							window["-QUEUE-"].update(values=queue)
							break      
			if edit == True:
				r=0
				for i in range(0, len(listed)):
					if str(listed[i][0]) == str(values["-SONGS-"][0]):
						editI=i				
						r = subwindows.Edit(listed[i][0], ID[i], listed[i][1], 0)
						break
				if r == 1:				
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
			
		# Append Navify or Discover Weekly results to queue
		if navify == True:
			try:
				tempQ=tempQ.get(0.005)
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
				navify = False
				window["-QUEUE-"].update(values=queue)
				window["-NAVIFY-"].update(disabled=False)
				tempQ=[]
			except:
				pass

		# Checks if there are songs queued
		if len(queue) > 1 and isPlaying == False:
			tempName = ""
			valid=0
			a=1
			tname=""
			if shuffle == True and len(queue) > 2 and isPrev == False:
				a = random.randrange(1,len(queue))
			isPrev = False
			for i in range(len(listed)):
				# Checks to see if the song is a local one
				skip=False		
				tname=""		
				if listed[i][0] == queuePaths[a]:
					name=listed[i][1]
					skip = True						
					window["-PLAYING-"].update("Now Playing: " + name)
				if listed[i][0] == queue[a] or skip==True:
					valid=1
					if skip==False:
						window["-PLAYING-"].update("Now Playing: " + listed[i][0])
						name = listed[i][0]
						prevSongs.append(listed[i][0])
						prevPaths.append("")
						currentTrack = listed[i][1]
					else:
						prevSongs.append(listed[i][1])
						prevPaths.append(listed[i][0])
						currentTrack = "none"
						
					#p = Process(target=Play, args=(i,))
					#p.start()
					settings = pickle.load(open(playerHome + 'settings.pkl', 'rb'))
					vol=settings[0]
					os.chdir(mpvLoc)
					os.popen("mpv --no-video --no-resume-playback --input-ipc-server=\\\\.\\pipe\\mpvsocket --volume=" + str(vol) +" " + ID[i] + " > " + playerHome + "\\output.txt")
					os.chdir(playerHome)
					duration=''
					del queue[a]   
					del queuePaths[a]           
					window["-QUEUE-"].update(values=queue)
					play=True
					window["-PLAY-"].update(image_filename=playerHome + "icons\\pause.png")                
					isPlaying=True	
					liked="elike.png"
					window["-LIKE-"].update(image_filename=playerHome + "icons\\elike.png")
					for c in range(0,len(likes)):
						if (listed[i][1] == likes[c]):
							window["-LIKE-"].update(image_filename=playerHome + "icons\\like.png")
							liked="like.png"
							break          
					
					break
					
			if valid==0:
				del queue[a]
				del queuePaths[a]
				window["-QUEUE-"].update(values=queue)

		# END OF SONG WITH NO QUEUE EVENT    
		if len(queue) == 1 and isPlaying == False:     
			tempName=""
			if exists("output.txt"):
				os.system("del output.txt")
			
			if repeat == True:
				queue = ["[CLEAR]"]
				queuePaths=[""]
				for i in range(len(prequeue)):
					queue.append(prequeue[i])
					queuePaths.append(prequeuePaths[i])
			else:
				window["-PLAY-"].update(image_filename=playerHome + "icons\\play.png")
				window["-PLAYING-"].update("Now Playing: ")
				liked="elike.png"
				window["-LIKE-"].update(image_filename=playerHome + "icons\\elike.png")
				window["-TIME-"].update("0:00/0:00")
				window["-BAR-"].update(0, range=(0,1))
				play=False

		# Repeat
		if event == "-REPEAT-":
			if repeat == False:
				window["-REPEAT-"].update(image_filename=playerHome + "icons\\repeat.png")
				repeat=True
				if isPlaying == True:
					prequeue.append(name)
					prequeuePaths.append(namePath)
					for i in range(1,len(queue)):
						prequeue.append(queue[i])
						prequeuePaths.append(queuePaths[i])
			else:
				window["-REPEAT-"].update(image_filename=playerHome + "icons\\nrepeat.png")
				repeat=False
				prequeue=[]
				prequeuePaths=[]

		# Shuffle
		if event == "-SHUFFLE-":
			if shuffle == 0:
				window["-SHUFFLE-"].update(image_filename=playerHome + "icons\\shuffle.png")
				shuffle=True
			else:
				window["-SHUFFLE-"].update(image_filename=playerHome + "icons\\nshuffle.png")
				shuffle=False
		# BLACKLIST
		if event == "-BLACKLIST-" and isPlaying == True and currentTrack !="none":
			os.system("move " + playerHome + "cache\\" + currentTrack + " " + playerHome + "blacklist\\")
			for i in range(len(listed)):
				if listed[i][1] == currentTrack:
					print(listed[i])
					print(spotList[i])
					del listed[i]
					del ID[i]
					del spotList[i]
					break
			window["-SONGS-"].update(values=spotList)
			event="-SKIP-"

		# LIKE
		if event == "-LIKE-" and isPlaying == True and currentTrack != "none":
			liked=1            
			for i in (range(0,len(likes))):
				if currentTrack == likes[i]:
					liked=0
					window["-LIKE-"].update(image_filename=playerHome + "icons\\elike.png")
					sp.current_user_saved_tracks_delete([currentTrack])
					break
			if liked == 1:  
				sp.current_user_saved_tracks_add([currentTrack])
				window["-LIKE-"].update(image_filename=playerHome + "icons\\like.png")            
			likes = GenLikes()
			f = open(playerHome + "icons\\likes.pkl", 'wb')
			pickle.dump(likes, f)
			f.close()

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
		if values["-INSEARCH-"] and len(values["-INSEARCH-"]) > 0 and len(values["-INSEARCH-"]) != oldLen:
			oldLen = len(values["-INSEARCH-"])
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

		# DISCOVER WEEKLY EVENT
		if event == "Discover Weekly Playlist" and navify == False:
			pool = ThreadPool(processes=1)
			tempQ = pool.apply_async(discover)
			window["-NAVIFY-"].update(disabled=True)
			navify = True

		# Skip/Next
		if event == "-SKIP-" and isPlaying == True:
			KillMPV()  
			isPlaying = False  

		# PLAY/PAUSE
		if event == "-PLAY-" and isPlaying == True:    		
			if play == True:
				os.system('echo set pause yes >\\\\.\\pipe\\mpvsocket')
				play = False
				window["-PLAY-"].update(image_filename=playerHome + "icons\\play.png") 
			else:
				os.system('echo set pause no >\\\\.\\pipe\\mpvsocket')
				play = True
				window["-PLAY-"].update(image_filename=playerHome + "icons\\pause.png")				

		# PREVIOUS
		if event == "-PREV-" and len(prevSongs) > 0:
			tempQ = list(queue[1:])
			tempQP = list(queuePaths[1:])
			queue=["[CLEAR]"]
			queuePaths=[""]
			isPrev = True
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
				isPlaying = False
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
			if exists(localMusic):
				ViewAllCondense(ViewAll(localMusic), ViewAll(playerHome + "playCache"))
			else:
				ViewAllCondense([], ViewAll(playerHome + "playCache"))						
			window["-LOCAL-"].update(values=localMain)
			window["-SONGS-"].update(values=spotList)

		# PLAYLIST BUTTON EVENT
		if event == "-PLAYLIST-":
			temp=[]
			temp=subwindows.Playlist(listed)
			for i in range(len(temp[0])):
				queue.append(temp[0][i])
				queuePaths.append(temp[1][i])
				if repeat == True:
					prequeue.append(temp[0][i])
					prequeuePaths.append(temp[1][i])
			window["-QUEUE-"].update(values=queue)   
         
		# SETTINGS        
		if event == "-SETTINGS-":
			r = subwindows.Settings(sp)
			if r == 1:
				window.close()
				window = ReloadNavify(queue, name, liked)
			else:
				GenList()			
				window["-LOCAL-"].update(values=localMain)
				window["-SONGS-"].update(values=spotList)
						
			settings = pickle.load(open(playerHome + "settings.pkl", 'rb'))
			if localMusic != settings[2]:			
				localMusic = settings[2]			
				if exists(localMusic):
					ViewAllCondense(ViewAll(localMusic), ViewAll(playerHome + "playCache"))

		# NAVIFY EVENT
		if event == "-NAVIFY-" and navify == False: 
			pool = ThreadPool(processes=1)
			tempQ = pool.apply_async(Navify)
			window["-NAVIFY-"].update(disabled=True)
			navify = True
			
		# NAVIFY RCLICK EVENT
		for i in range(len(plNames)):
			if plNames[i] == event:
				pool = ThreadPool(processes=1)
				tempQ = pool.apply_async(getPlaylistSongs, args=(plIDS[i],))
				window["-NAVIFY-"].update(disabled=True)
				navify = True

		if time != 0:
			time=time-100     

Player() # Starts the GUI
KillMPV() 
