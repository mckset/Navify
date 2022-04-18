# Navify GUI
# Version 2.1 : Hot fix

# Other programs
import subwindows

# System
import pickle
import subprocess
import random
import os
import sys

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
playerHome=os. getcwd() + "/" # Location of python script
localMusic = home + "/Music"

localMain=["ALL", "LOCAL CACHE","MUSIC"] # The Main Screen for the Local Section

# NAVIFY STUFF
header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
sp=""

#-------------------------------------------------
# SETUP FUNCTIONS
#-------------------------------------------------

# Checks if all the dependencies exist and creates missing files
def SetupSettings():
	global likes
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

	err=""
	if not exists(playerHome + "icons"):
		err = "The 'icons' folder is missing from " + playerHome + ". Please make sure the folder is in the right location."
	try:
		subprocess.run(["socat"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	except:
		err = err + "\n\nsocat is not installed. Please install socat"
	try:
		subprocess.run(["mpv"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		try:
			subprocess.run(["youtube-dl"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
		except:	
			err = err + "\n\nyoutube-dl is not installed. Please install youtube-dl"	
	except:
		err = err + "\n\nmpv is not installed. Please install both mpv and youtube-dl"
	
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

	if not exists(playerHome + "settings.pkl"):
		pickle.dump([100, 1, home + "/Music"], open(playerHome + "settings.pkl", 'wb'))
	if not exists(playerHome + "/playCache"):
		subprocess.run(["mkdir", playerHome + "playCache"])
	if not exists(playerHome + "/cache"):
		subprocess.run(["mkdir", playerHome + "cache"])
	if not exists(playerHome + "blacklist"):
		subprocess.run(["mkdir", playerHome + "blacklist"])
	if not exists(playerHome + "playlists"):
		subprocess.run(["mkdir", playerHome + "playlists"])

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

	settings = pickle.load(open(playerHome + "settings.pkl", 'rb'))
	localMusic = settings[2]

	if not exists(localMusic):
		print("WARNING: " + home + "Music does not exist. Please enter the path to local songs in the settings menu") 

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
	x=0
	try:
		sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=["user-library-read", "user-library-modify", "playlist-read-private"])) # read - get recommended; modify - change like statues; read-private - get playlists
		sp.current_user_saved_tracks(1, 1) # Attempts a connetion
	except:
		print("Error: invalid Spotify settings.\n")
		SpotSetup()
		if e == 1:
			return

def SpotSetup():
	global sp
	global key
	global e
	spotWindow = sg.Window(
			"Enter Spotify Values", 
			setupLayout(), 
		  	background_color=background, 
 		   	button_color=accent,
			resizable=True,
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

a=0
key=['','','']
if exists(playerHome + "keys.pkl"):
	try:
		key = pickle.load(open(playerHome + "keys.pkl", 'rb'))
		os.environ['SPOTIPY_CLIENT_ID']=key[0]
		os.environ['SPOTIPY_CLIENT_SECRET']=key[1]
		os.environ['SPOTIPY_REDIRECT_URI']=key[2]
		LoadSpotify()
		if e == 1:
			sys.exit()
			quit()
	except:
		if e == 0:
			SpotSetup()
		else:
			sys.exit()
else:	
	subprocess.run(["touch", playerHome + "keys.pkl"])
	SpotSetup()

		
# Gets Playlist ids
print("Gettings playlists...")
while True:
	try:
		playlists = sp.current_user_playlists()['items']
		plIDS=[]
		plNames=[]
		for i in range(len(playlists)):
			plIDS.append(playlists[i]['id'])
			plNames.append(playlists[i]['name'])
		plNames.append("Close")
		break
	except:
		pass

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
			resizable=True,
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
	cache=[]
	x=0

	print("Getting liked songs...")
	while True: 
		try:
			results.append(sp.current_user_saved_tracks(20, x))
			x+=20
			if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
				break
		except:
			pass

	for i in range(len(results)):
		for x in range(len(results[i]['items'])):
			likes.append(results[i]['items'][x]['track']['id'])
			# Checks for songs that need to be cached
			if not exists(playerHome + "cache/" + likes[x+(20*i)]):
				cache.append([likes[x+(20*i)], results[i]['items'][x]['track']['name'] + " - " + results[i]['items'][x]['track']['artists'][0]['name']])

	if len(likes) == 0:
		window = sg.Window("NOTICE", 
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
	elif len(cache) > 0:
		CacheLikes(cache)
	return likes  


#-------------------------------------------------
# FUNCTIONS THAT GET CALLED DURING THE MAIN LOOP
#-------------------------------------------------

def Play(x, name):  
	track=ID[x]
	settings = pickle.load(open(playerHome + 'settings.pkl', 'rb'))
	vol=settings[0]
	for i in range(3):  # 3 attempts to retrieve the song
		try:
			print("attempt #" + str(i+1))	
			subprocess.run(["mpv","--title=" + name, "--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume=" + str(vol), track])
			break
		except:
			pass

def PlayAll(select, isCache): # Plays all songs
	tracks=next(walk(select), (None, None, []))[2]
	tempName=[]
	for i in range(len(tracks)):
		if isCache == True:
			tempName.append(subprocess.Popen(["cat", select + "/" + tracks[i]], stdout=subprocess.PIPE, text=True).communicate()[0])		
		else:
			if ".wav" in tracks[i] or ".ogg" in tracks[i] or ".mp3" in tracks[i]or ".mid" in tracks[i]:
				tempName.append(tracks[i])
	tempName.sort()
	return tempName

def UpLocal(select, isCache):
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
				tempName.append(subprocess.Popen(["cat", select + "/" + tracks[i]], stdout=subprocess.PIPE, text=True).communicate()[0])			
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
				if "/" in l1[i][len(l1[i]) - a:]:
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
		locTracks.append(subprocess.Popen(["cat", l2[i]], stdout=subprocess.PIPE, text=True).communicate()[0])
		a=0
		for x in range(len(l2[i])):
			if "/" in l2[i][len(l2[i]) - x:]:
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
		mpv = subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["quit"] }'), stdout=subprocess.PIPE).stdout, text=True)
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
	tempID=next(walk(playerHome + "cache/"), (None, None, []))[2]
	for i in range(len(tempID)):
		f = open (playerHome + "cache/" + tempID[i], encoding="utf-8").readlines(0)
		sortID.append(f[0][0:len(f[0])-1])
		prevListed.append(f[1])
		sortListed.append(f[1].upper())
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
		ViewAllCondense(ViewAll(localMusic), ViewAll(playerHome + "playCache"))
	else:
		ViewAllCondense([], ViewAll(playerHome + "playCache")) 

def getPlaylistSongs(selID):
	plTracks=[]
	plID=[] 
	try:
		p = sp.playlist_items(selID)			
	except:	
		return []

	for i in range(len(p['items'])):
		if not exists(playerHome + 'blacklist/' + p['items'][i]['track']['id']):
			plTracks.append(p['items'][i]['track']['name'] + " - " + p['items'][i]['track']['album']['artists'][0]['name'])
			plID.append(p['items'][i]['track']['id'])
	checkCache(plTracks, plID)
	return plTracks			

def Navify():
	try:
		recList=[] 
		recId=[]
		tracks = pickle.load(open(playerHome + 'recommend.pkl', 'rb'))
					
		# Sets up the playlist to use based off of the first 5 tracks in the liked playlist
		rec=sp.recommendations(seed_tracks=tracks, limit=50)
		   
		# Checks to see if a track is in the blacklist
		for i in range(len(rec['tracks'])):
			if not exists(playerHome + 'blacklist/' + str(rec['tracks'][i]['id'])):
				recList.append(str(rec['tracks'][i]['name']) + " - " + str(rec['tracks'][i]['artists'][0]['name']))
				recId.append(rec['tracks'][i]['id'])
		checkCache(recList, recId)	
		return recList
	except:
		return []

def checkCache(songs, ids):
	fText=""

    # Checks to see if a track is in the cache directory and caches it if not  
	for i in range(0,len(ids)):
		if not exists(playerHome + "cache/" + ids[i]):
			#print(i)
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
	f = open(playerHome + "cache/" + str(cache) , "w", encoding="utf-8")
	f.write("https://www.youtube.com/watch?v=" + video + "\n" + name)
	f.close()

likes=GenLikes()
if not exists(playerHome + "recommend.pkl") and likes[0]:
		pickle.dump([likes[0]], open(playerHome + "recommend.pkl", 'wb'))
GenList() 
		
def reloadNavify(queue, name, liked):
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
		sg.Button(image_filename=playerHome + "icons/search.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SEARCH-"),
		sg.Text("Songs", text_color=textc, background_color=background,  expand_x=True),
		sg.Button(image_filename=playerHome + "icons/edit.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-EDIT-")
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
		sg.Button(image_filename=playerHome + "icons/add.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-ADD-"),
		sg.Text("Local", background_color=background,text_color=textc,  expand_x=True),
		sg.Button(image_filename=playerHome + "icons/playlist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAYLIST-")
		],
		[
		sg.Listbox(values=localMain, background_color=foreground, text_color=textc, no_scrollbar=False, size=(1,1), enable_events=True, expand_y=True, expand_x=True, key="-LOCAL-")
		] 
	]

	# Queued Songs
	Queue = [
		[
		sg.Button(image_filename=playerHome + "icons/navi.png", right_click_menu=[[""], plNames], enable_events=True, mouseover_colors=hover, border_width=0, key="-NAVIFY-"),
		sg.Text("Queue",text_color=textc, background_color=background,  expand_x=True),
		sg.Button(image_filename=playerHome + "icons/settings.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SETTINGS-")
		],
		[
		sg.Listbox(values=queue, background_color=foreground, text_color=textc, no_scrollbar=False, size=(1,1), enable_events=True, key="-QUEUE-", expand_y=True, expand_x=True)
		] 
	]

	# Play Bar
	BottomBar = [
		[
		sg.Text(text="Now Playing: " + current, text_color=textc, size=(1,1), justification="left", font=smallFont, expand_x=True, background_color=foreground, key="-PLAYING-"),
		sg.Button(image_filename=playerHome + "icons/nrepeat.png", enable_events=True ,mouseover_colors=hover, border_width=0, key="-REPEAT-"),
		sg.Button(image_filename=playerHome + "icons/blacklist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-BLACKLIST-"),
		sg.Button(image_filename=playerHome + "icons/prev.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PREV-"),
		sg.Button(image_filename=playerHome + "icons/play.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAY-"),
		sg.Button(image_filename=playerHome + "icons/next.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SKIP-"),
		sg.Button(image_filename=playerHome + "icons/elike.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-LIKE-"),
		sg.Button(image_filename=playerHome + "icons/nshuffle.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SHUFFLE-"),
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
	global listed
	global spotList

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
	
	level=0 # How Many Folders Down the Local Section is
	duration=1 # How long the song lasts
	current=1 # Current playtime position
	editI=0 # Index of the song that is being edited in the list 'listed'
	time=0 # Count down to start moving the scrollbar again
	timeS=0 # Controls how fast scrolling text should change	
	oldLen=0 # The length of the previous search to prevent the player from constantly updating

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
			except:
				pass	
		else:
			try: # Links the player to a left over song after a crash
				x=subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["get_property", "duration"] }'), stdout=subprocess.PIPE).stdout, text=True)
				if x != '':
					isPlaying = True
					name = subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["get_property", "title"]}'), stdout=subprocess.PIPE).stdout, text=True)
					for i in range(len(name[8:])):
						if name[i:i+2] == '\",':
							name=name[9:i]
							break					
					window["-PLAYING-"].update("Now Playing: " + name)
			except:
				pass
		try:
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
		except:
			pass

		# Key '<'
		if event == "comma:59":
			event = "-PREV-"

		# Things that happen when a song is playing (Progress bar and keyboard inputs)
		if isPlaying == True:			
			try:
				duration = subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["get_property", "duration"] }'), stdout=subprocess.PIPE).stdout, text=True)
				current = subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["get_property", "playback-time"] }'), stdout=subprocess.PIPE).stdout, text=True)
					
				for i in range(len(duration[8:])):
					if duration[i:i+1] == ',':
						duration=float(duration[8:i])
						break
				for i in range(len(current[8:])):
					if current[i:i+1] == ',':
						current=float(current[8:i])
						break
				
				# KEYBOARD EVENTS
				if event == "space:65": # Spacebar
					event="-PLAY-"

				if event == "period:60": # Key '>'
					event = "-SKIP-"

				if event == "Up:111": # Arrows Up and Down
					settings[0] = settings[0] + 2
					if settings[0] > 150:
						settings[0] = 150
					subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "volume", '+ str(settings[0]) + ']}'), stdout=subprocess.PIPE).stdout)
					f = open(playerHome + "settings.pkl", 'wb')
					pickle.dump(settings, f)
					f.close()
				if event == "Down:116":
					settings[0] = settings[0] - 2
					if settings[0] < 0:
						settings[0] = 0
					subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "volume", '+ str(settings[0]) + ']}'), stdout=subprocess.PIPE).stdout)
					f = open(playerHome + "settings.pkl", 'wb')
					pickle.dump(settings, f)
					f.close()

				if event == "Right:114": # Left and Right arrow key events
					current = current + 5 
					subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["set_property", "playback-time", ' + str(current) + '] }'), stdout=subprocess.PIPE).stdout, text=True)

				if event == "Left:113":
					current = current - 5 
					if current < 0:
						current = 0
					subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["set_property", "playback-time", ' + str(current) + '] }'), stdout=subprocess.PIPE).stdout, text=True)


				# PROGRESS BAR STUFF
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
				if sec >= 10:
					duration = str(min) + ":" + str(sec)
				else:
					duration = str(min) + ":0" + str(sec)
				current = current + "/" + duration
				window["-TIME-"].update(current)	
			except:
				pass

			# Grabbing the slider
			if event == "-BAR-":
				time=200 # How long to wait before the program automatically moves the slider again
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{ "command": ["set_property", "playback-time", ' + str(values["-BAR-"]/100) + '] }'), stdout=subprocess.PIPE).stdout, text=True)

		# LOCAL SONG EVENT
		if event == "-LOCAL-" and len(values["-LOCAL-"]) > 0:
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
							if "/" in path[i:i+1]:
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
						else: # Play all tracks in local folder
							tempName=[]
							tempName=PlayAll(path, isCache)
							for i in range(len(tempName)):					
								queue.append(tempName[i])
								queuePaths.append(path+"/"+tempName[i])
								if repeat == True:
									prequeue.append(tempName[i])	
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

			if edit == True and level > 0 and str(values["-LOCAL-"][0]) != "..." and str(values["-LOCAL-"][0]) != "[TRACKS]" and str(values["-LOCAL-"][0]) != "[ALL]" and len(str(values["-LOCAL-"][0])) > 0:
				r=0			
				for i in range(0, len(listed)):
					if ".wav" in str(values["-LOCAL-"][0]) or ".ogg" in str(values["-LOCAL-"][0]) or ".mp3" in str(values["-LOCAL-"][0]) or ".mid" in str(values["-LOCAL-"][0]):
						if str(listed[i][1]) == str(values["-LOCAL-"][0][0:len(str(values["-LOCAL-"][0]))-4]):
							r=subwindows.Edit(listed[i][1], ID[i], listed[i][0], 2)
							event="-EDIT-"
							break
					else:
						if str(listed[i][1]) == str(values["-LOCAL-"][0]):					
							a=0
							for x in range(len(listed[i][0])):
								if listed[i][0][x:x+1] == '/':
									a=x
							sendID=listed[i][0][0:a] + "/" + ID[i][32:]
							r=subwindows.Edit(listed[i][1], ID[i], sendID, 1)
							event="-EDIT-"
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
		if event == "-SONGS-" and len(values["-SONGS-"]) > 0:
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
						event="-EDIT-"
						break
				if r == 1:				
					GenList()
					window["-SONGS-"].update(values=spotList)

		# QUEUE Event
		if event == "-QUEUE-" and len(values["-QUEUE-"]) > 1:
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
			
		# Append Navify or Playlist results to queue
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
						
					p = Process(target=Play, args=(i, name, ), daemon=True)
					p.start()
					del queue[a]   
					del queuePaths[a]           
					window["-QUEUE-"].update(values=queue)
					play=True
					window["-PLAY-"].update(image_filename=playerHome + "icons/pause.png")                
					isPlaying=True	
					liked="elike.png"
					window["-LIKE-"].update(image_filename=playerHome + "icons/elike.png")
					for c in range(0,len(likes)):
						if (listed[i][1] == likes[c]):
							window["-LIKE-"].update(image_filename=playerHome + "icons/like.png")
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
			if repeat == True:
				queue = ["[CLEAR]"]
				queuePaths=[""]
				for i in range(len(prequeue)):
					queue.append(prequeue[i])
					queuePaths.append(prequeuePaths[i])
			else:
				window["-PLAY-"].update(image_filename=playerHome + "icons/play.png")
				window["-PLAYING-"].update("Now Playing: ")
				liked="elike.png"
				window["-LIKE-"].update(image_filename=playerHome + "icons/elike.png")
				window["-TIME-"].update("0:00/0:00")
				window["-BAR-"].update(0, range=(0,1))
				play=False

		# Repeat
		if event == "-REPEAT-":
			if repeat == False:
				window["-REPEAT-"].update(image_filename=playerHome + "icons/repeat.png")
				repeat=True
				if isPlaying == True:
					prequeue.append(name)
					prequeuePaths.append(namePath)
					for i in range(1,len(queue)):
						prequeue.append(queue[i])
						prequeuePaths.append(queuePaths[i])
			else:
				window["-REPEAT-"].update(image_filename=playerHome + "icons/nrepeat.png")
				repeat=False
				prequeue=[]
				prequeuePaths=[]

		# Shuffle
		if event == "-SHUFFLE-":
			if shuffle == 0:
				window["-SHUFFLE-"].update(image_filename=playerHome + "icons/shuffle.png")
				shuffle=True
			else:
				window["-SHUFFLE-"].update(image_filename=playerHome + "icons/nshuffle.png")
				shuffle=False

		# BLACKLIST
		if event == "-BLACKLIST-" and isPlaying == True and currentTrack !="none":
			subprocess.Popen(["mv", playerHome + "cache/" + currentTrack, playerHome + "blacklist/" ])
			for i in range(len(listed)):
				if listed[i][1] == currentTrack:
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
					window["-LIKE-"].update(image_filename=playerHome + "icons/elike.png")
					while True:
						try:						
							sp.current_user_saved_tracks_delete([currentTrack])
							break
						except:						
							pass
					break
			if liked == 1:
				while True:  
					try:
						sp.current_user_saved_tracks_add([currentTrack])
						break
					except:
						pass
				window["-LIKE-"].update(image_filename=playerHome + "icons/like.png")            
			likes = GenLikes()
			f = open(playerHome + "icons/likes.pkl", 'wb')
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

		# Skip/Next
		if event == "-SKIP-" and isPlaying == True:
			KillMPV()  
			isPlaying = False  

		# PLAY/PAUSE
		if event == "-PLAY-" and isPlaying == True:    		
			if play == True:
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "pause", true]}'), stdout=subprocess.PIPE).stdout, text=True)
				play = False
				window["-PLAY-"].update(image_filename=playerHome + "icons/play.png") 
			else:
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "pause", false]}'), stdout=subprocess.PIPE).stdout, text=True)
				play = True
				window["-PLAY-"].update(image_filename=playerHome + "icons/pause.png")				
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
		
		if event == "-RELOAD-":
			window.close()
			window = reloadNavify(queue, name, liked)

		# 
		# SUB WINDOWS EVENTS
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
				window = reloadNavify(queue, name, liked)
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
			if plNames[i] == event and not "Close" in event and navify == False:
				pool = ThreadPool(processes=1)
				tempQ = pool.apply_async(getPlaylistSongs, args=(plIDS[i],))
				window["-NAVIFY-"].update(disabled=True)
				navify = True


		if time != 0:
			time=time-100     

print("Starting player...")
Player() # Starts the GUI
print("Closing...")
KillMPV() 
