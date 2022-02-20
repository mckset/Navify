# Navify GUI by Seth McKee
# Version 1.0
# Oops! All bloat!

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

import io
from PIL import Image
import PySimpleGUI as sg

from multiprocessing import Process

# File checking
from os.path import exists
from os import walk

# Used to communicate with the taskbar
import socket 

# Fonts
defaultFont="Inter 40"
smallFont="Inter 32"

# GUI Colors
background="#ccccdc"
foreground="#99aabf"
accent="#99aabf"
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

playerLoc="/.navi/navify/"
home=os.path.expanduser('~') + playerLoc # Users Home Path

localMain=["ALL", "LOCAL CACHE","MUSIC"] # The Main Screen for the Local Section

# NAVIFY STUFF
header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
sp=""


# SPOTIFY STUFF
#481da7d376c747408b5ec25f609c193b
#4ec619360c6e497a9ce1f126a3c10f93
#http://localhost
		
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

def Play(x, finished):
	track=ID[x]
	trackID=ID[x]    
	vol=100

	if exists(home + "settings.pkl"):
		f = open(home + 'settings.pkl', 'rb')
		settings = pickle.load(f)
		f.close()
	vol=settings[0]

	subprocess.run(["mpv","--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume=" + str(vol), track])
	finished.put(True)

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
		info = [fname, "", "", name]
		f = open(home + 'info.pkl', 'wb')
		pickle.dump(info, f)
		f.close()

def updateLocal(select, isCache):
	newList=["..."]    

	if select == home + "playCache" or select == home[0:len(home) - len(playerLoc)] +"/Music":
		newList.append("[ALL]")

	folders=next(walk(select), (None, None, []))[1]
	tracks=next(walk(select), (None, None, []))[2]

	if len(folders) > 0:
		for i in range(len(folders)):
			newList.append(folders[i])
	
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
			"""
			listed.append([select + "/" + tracks[i], tempName[i]])
			ID.append(tempID[i])
			"""
		for i in range(len(tracks)):
			newList.append(tracks[i])
	window["-LOCAL-"].update(values=newList)
	

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

	for i in range(1,len(ID)):
		for x in range(len(locPaths)):
			if ID[i] == locID[x]:
				del locPaths[x]
				del locTracks[x]
				del locID[x]
				break

	for i in range(len(locTracks)):
		for x in range(len(ID):
			if locID[i] != ID[x]:
				listed.append([locPaths[i], locTracks[i]])
				ID.append(locID[i])
				break

	return tempList	

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
genList() 

def Navify(tempQ):
	recList=[] 
	recId=[]
	fText=""

	# Sets up the track list used to grab recommendations
	if exists(home + 'recommend.pkl'):
		f = open(home + 'recommend.pkl', 'rb')
		tracks = pickle.load(f)
		f.close()
	else:
		print("NOTICE: Recommended tracks list is not set up. Defaulting to the first 5 liked songs.")
		tracks = list(likes[0:4])
			    
	# Sets up the playlist to use based off of the first 5 tracks in the liked playlist
	rec=sp.recommendations(seed_tracks=tracks, limit=50)
    
	# Checks to see if a track is in the blacklist
	for i in range(0,49):
		if not exists(home + 'blacklist/' + str(rec['tracks'][i]['id'])):
			recList.append(str(rec['tracks'][i]['name']) + " " + str(rec['tracks'][i]['artists'][0]['name']))
			recId.append(rec['tracks'][i]['id'])

    # Checks to see if a track is in the cache directory and caches it if not
	tracksName=[]    
	for i in range(0,len(recId)):
		if not exists(home + "cache/" + recId[i]) and recId[i] != "skip":
			fText=str(recTrack[i]) + " - " + str(recArtist[i])
			fText = re.sub(r'[^\x00-\x7f]',r'', fText)
			name=fText
			for x in range(0,len(fText)):
				if " " in fText[x:x+1]:
					fText=fText[0:x] + "+" + fText[x+1:]  
			Search(recList[i], recId[i], name, fText)
	
	# Gets tracks info from cache
	for i in range(0,len(recId)):
		currentFile = subprocess.Popen(["cat", home + "cache/" + recId[i]], stdout=subprocess.PIPE, text=True).communicate()[0]                    
		tracksName.append(currentFile[0:43]) # Appends YouTube link
	tempQ.put(tracksName)

def Search(string, cache, name, url):       
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
        			    
#-------------------------------------------------
# SUB-WINDOW LAYOUTS
#-------------------------------------------------			    
def AddLayout(folders):
	Search = [
		[
		sg.Text("Search For Song: ", background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,  visible=True, key="-ASEARCH-"),
		sg.Button("Search", enable_events=True, mouseover_colors=hover, border_width=0, key="-AENTER-")
		]
	]
	Results = [
		[
		sg.Text("Results:", background_color=background, expand_x=True)
		],
		[
		sg.Listbox(values=[], auto_size_text=True, background_color=foreground, text_color=textc, size=(25,1), no_scrollbar=True,disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-ARESULTS-")]
		]

	Name = [
		[
		sg.Text("Name: ", background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, key="-ANAME-"),
		sg.Button("Submit", enable_events=True, mouseover_colors=hover, border_width=0, key="-ASUBMIT-", disabled=True)
		]
	]

	layoutAdd = [
		[
		sg.Column(Search, expand_y=True, background_color=background,expand_x=True) # Search
		],
		[
		sg.Column(Results, expand_y=True, background_color=background,expand_x=True) # Results
		],
		[
		sg.Column(Name, expand_y=True, background_color=background,expand_x=True) # Song Name
		],
		[
		sg.Listbox(values=folders, background_color=foreground,auto_size_text=True, text_color=textc, size=(25,1), no_scrollbar=True,disabled=False, enable_events=True,  expand_y=True, expand_x=True, key="-ACREATE-"),
		sg.VSeparator(color=None), # Folders list
		sg.Button("Cancel", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACANCEL-"), 
		sg.Button("Open", enable_events=True, mouseover_colors=hover, border_width=0, key="-AOPEN-", disabled=True),
		sg.VSeparator(color=None),
		sg.Image(source=None, background_color=background,size=(256,192), key="-AIMAGE-") # Thumbnail
		]
	]
	return layoutAdd

def PlaylistLayout(files):
	layoutPlaylist = [
		[
		sg.Text("Pick A PLaylist",background_color=background, expand_x=True)
		],
 		[
		sg.Listbox(values=files, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PPLAYLISTS-")
		], 
		[
		sg.Button("Cancel", enable_events=True, mouseover_colors=hover, border_width=0, font=smallFont,key="-PCANCEL-"),
		sg.Button("Submit", enable_events=True, mouseover_colors=hover, border_width=0,font=smallFont, key="-PSUBMIT-")
		]	
	]
	return layoutPlaylist

def SettingsLayout(settings, rec):
	layoutSettings = [
		[
		sg.Slider(range=(0,150), background_color=background,trough_color = foreground, default_value=settings[0], enable_events=True, key="-SVOL-"),
		sg.Listbox(values=likes, background_color=foreground, text_color=textc, no_scrollbar=True, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-SLIKES-"),
		sg.Listbox(values=rec, background_color=foreground,text_color=textc, no_scrollbar=True, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-SREC-")
		],
		[
		sg.Text("Volume", background_color=background)
		],
		[
		sg.Button("SUBMIT", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SSUBMIT-"),
		sg.Button("CANCEL", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SCANCEL-")
		]        
	]
	return layoutSettings

#-------------------------------------------------
# DEFINE SUB-WINDOWS
#-------------------------------------------------

# Adds a new song to a separate cache directory 
def Add(): 
	temp=next(walk(home + "playCache/"), (None, None, []))[1]
	temp.sort()
	folders=["---create new---"]

	for i in range(0,len(temp)):
		folders.append(temp[i])

	window = sg.Window(
			"Add Song", 
			AddLayout(folders), 
		  	background_color=background, 
 		   	button_color=accent,
   		   	font=defaultFont,
		   	text_justification="center",
		   	border_depth=None
		  	)
	search="" # Song to search for
	video=[] # List of found videos
	img=[] # Thumbnails
	links=[] # Links to each video
	selected="" # Selected video
	text=[] # Title of each video
	sfolder="" # Selected folder to add the song to
	content=""
	name=""
	
	while True:
		event, values = window.read()
		
		if event == "-ASEARCH-": 
			search=values["-ASEARCH-"]   

		if event == "-AENTER-":
			video=[]
			img=[]
			links=[]
			selected=""
			text=[]
			sfolder=""
			content=""
			name=""
			url=search
			
			# Retrieves the song from Youtube
			for i in range(0,len(search)):
				if " " in search[i:i+1]:
					url=url[0:i] + "+" + url[i+1:] 
			req=request.Request("https://youtube.com/results?search_query=" + url, headers=header)
			U = request.urlopen(req)
			data = U.read().decode('utf-8')
			for i in range(0,len(data)):
				if "videoid" in data[i:i+7].lower() and not "videoids" in data[i:i+8].lower():
					valid=1
					for x in range(0,len(video)):
						if video[x] == data[i+10:i+21]:
							valid=0
					if valid == 1:
						video.append(data[i+10:i+21])
						img.append("https://i.ytimg.com/vi/" + data[i+10:i+21] +"/hqdefault.jpg")
						links.append("https://www.youtube.com/watch?v=" + data[i+10:i+21])
						text.append("Unknown")
						for a in range(i,i+1000):
							if "\"title\":" in data[a:a+8]:
								for y in range(a,i+1000):
									if "\"}]" in data[y:y+3]:
										text[len(text)-1] = data[a+26:y]
										break
								break  

			window["-ARESULTS-"].update(disabled=False)
			window["-ARESULTS-"].update(values=links)
			window["-ANAME-"].update(search)
			window["-ANAME-"].update(disabled=False)
			name=search

		if event == "-ANAME-":
			content=values["-ANAME-"]

		# Updates the name field to match the title and adds a thumbnail
		if event == "-ARESULTS-":
			window["-AOPEN-"].update(disabled=False)
			selected=values["-ARESULTS-"][0]
			for i in range(0,len(links)):
				if links[i] == values["-ARESULTS-"][0]:
					response = requests.get(img[i])    
					pil_image = Image.open(io.BytesIO(response.content))
					png_bio = io.BytesIO()
					pil_image.save(png_bio, format="PNG")
					png_data = png_bio.getvalue()
					response.raw.decode_content = True
					window["-AIMAGE-"].update(data=png_data, size=(256,192), subsample=2)        
					window["-ANAME-"].update(text[i])
					name=video[i]
					content=text[i]

		if event == "-ACREATE-":
			if values["-ACREATE-"][0] != "---create new---":
				sfolder=values["-ACREATE-"][0]
			else:
				sfolder=""
				fname=""
				layoutAdd2 = [
					[
					sg.Text("Create A New Folder ", background_color=background, expand_x=True)
					],
					[
					sg.Text("Name: ", background_color=background, expand_x=True),
					sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-ANAME2-"),
					sg.Button("Create", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACREATE2-", disabled=True),
					sg.Button("Cancel", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACANCEL2-")
					]
				]

				window2 = sg.Window(
					"New Folder", 
					layoutAdd2,
					background_color=background, 
		  			button_color=accent,
		   		   	font=defaultFont,
				   	text_justification="center",
					border_depth=None
				)
				while True:
					event2, values2 = window2.read()

					if event2 == "-ACREATE2-" and len(fname) > 0:
						subprocess.run(["mkdir", home + "playCache/" + fname])
						window2.close()
						break

					if event2 == "-ANAME2-":
						fname=values2["-ANAME2-"]
						if len(fname) > 0:
							window2["-ACREATE2-"].update(disabled=False)
					else:
						window2["-ACREATE2-"].update(disabled=True)

					if event2 == "-ACANCEL2-":
						window2.close()
						break
				temp=next(walk(home + "playCache/"), (None, None, []))[1]
				folders=["---create new---"]
				temp.sort()
				for i in range(0,len(temp)):
					folders.append(temp[i])
				window["-ACREATE-"].update(values=folders)



		if event == "-AOPEN-":
			subprocess.run(["gio", "open", selected])

		if len(name) > 0 and len(sfolder) > 0:
			window["-ASUBMIT-"].update(disabled=False)
		else:
			window["-ASUBMIT-"].update(disabled=True)

		if event == "-ASUBMIT-":
			if not exists(home + "playCache/" + sfolder + "/" + name):
				subprocess.run(["touch", home + "playCache/" + sfolder + "/" + name])
			f = open(home + "playCache/" + sfolder + "/" + name, 'w')
			f.write(content)
			f.close()
			window.close()
			break

		if event == "-ACANCEL-":    
			window.close()
			break
	return []

def Playlist():
	files=["---create new---"]
	temp=next(walk(home + "playlists/"), (None, None, []))[2]
	temp.sort()
	songs=[]
	selected=[]

	for i in range(0,len(temp)):
		files.append(temp[i])
	for i in range(1,len(listed)):
		songs.append(listed[i][0])
	
	window = sg.Window(
		"Select Playlist", 
		PlaylistLayout(files), 
		background_color="#ccccdc", 		
		button_color=accent,
   		font=defaultFont,
	   	text_justification="center", 
		border_depth=None
	)
	while True:
		event, values = window.read()

		if event == "-PPLAYLISTS-":
			if values["-PPLAYLISTS-"][0] == "---create new---":


				Left = [
					[
					sg.Text("Songs", background_color=background,expand_x=True)
					],
					[
					sg.Listbox(values=songs, auto_size_text=True, background_color=foreground, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PSONGS2-")
					]
				]
				Right = [
					[
					sg.Text("Selected", background_color=background,expand_x=True)		
					],
					[
					sg.Listbox(values=selected, auto_size_text=True, background_color=foreground, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PSELECTED2-")
					]
				]

				layoutP2 = [
					[
					sg.Column(Left, expand_y=True, background_color=background,expand_x=True),
					sg.VSeparator(color=None),
					sg.Column(Right, expand_y=True, background_color=background,expand_x=True)
					],
					[
					sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-PSEARCH2-"),					
					sg.Button("CANCEL", enable_events=True, mouseover_colors=hover, border_width=0,font=smallFont, key="-PCANCEL2-"),
					sg.Button("SUBMIT", enable_events=True, mouseover_colors=hover, border_width=0, font=smallFont,key="-PSUBMIT2-")
					]
				]
				window2 = sg.Window(
					"Create Playlist", 
					layoutP2, 
					background_color=background, 
					button_color=accent,
					font=defaultFont,
					text_justification="center",
					border_depth=None, 
					finalize=True
				)
				
				while True:
					event2, values2 = window2.read()

					if event2 == "-PSONGS2-":
						valid=1						
						selected.append(str(len(selected)) + ": " + values2["-PSONGS2-"][0])
						window2["-PSELECTED2-"].update(values=selected)

					if event2 == "-PSELECTED2-" and len(selected) > 0:
						del selected[int(values2["-PSELECTED2-"][0][0:1])]
						for i in range(0,len(selected)):
							selected[i] = str(i) + ": " + selected[i][3:]
						window2["-PSELECTED2-"].update(values=selected)

					if event2 == "-PSUBMIT2-" and len(selected) > 0:
						layoutP3=[
						[
							sg.Text("Name: ", expand_x=True),
							sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,key="-PNAME3-"),
							sg.Button("Create", enable_events=True, font=defaultFont,button_color=foreground, mouseover_colors=hover, border_width=0, key="-PCREATE3-")
						]
						]
						window3 = sg.Window(
							"Create Playlist",
							layoutP3,
							button_color=accent,
							font=defaultFont,
							text_justification="center",
							border_depth=None,
							finalize=True
						)
				
						name=""
						while True:
							event3, values3 = window3.read()
							
							if event3 == "-PNAME3-":
								name=values3["-PNAME3-"]

							if event3 == "-PCREATE3-":
								window3.close()
								break

						if len(name) > 0:
							f = open(home + "playlists/" + name, 'w')
							content=""							
							for i in range(0, len(selected)):
								content = content + selected[i][len(str(i))+2:] + "\n"
							f.write(content)
							f.close()
							window3.close()
							files=["---create new---"]
							temp=next(walk(home + "playlists/"), (None, None, []))[2]
							temp.sort()
							for i in range(0,len(temp)):
								files.append(temp[i])
							window["-PPLAYLISTS-"].update(values=files)
							window2.close()
							break

					if event2 == "-PCANCEL2-":
						window2.close()
						break

					if event2 == "-PSEARCH2-":
						newList=[]
						for i in range(0, len(songs)):
							if values2["-PSEARCH2-"].lower() in songs[i].lower():
								newList.append(songs[i])
						window2["-PSONGS2-"].update(values=newList)

		if event == "-PPLAYLISTS-":
			playlist=values["-PPLAYLISTS-"][0]

		if event == "-PSUBMIT-" and len(playlist) > 0:
			f = open(home + "playlists/" + playlist)
			selected=[]			
			while True:
				line = f.readline()
				if not line:
					break
				if "\n" in line:
					line=line[0:len(line) - 1]
				selected.append(line)
			window.close()
			break

		if event == "-PCANCEL-":
			window.close()
			break
	return selected

def Settings():
	f = open(home + "settings.pkl", 'rb')
	settings = pickle.load(f)
	f.close()
	x=0
	rec=[]
	results=[]

	while True: 
		results.append(sp.current_user_saved_tracks(20, x))
		x+=20
		if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
			break

	for i in range(0, len(results)):
		for idx, item in enumerate(results[i]['items']):
			rec.append(item['track']['name'] + " - " + item['track']['artists'][0]['name'])
             
	window = sg.Window(
		"Settings", 
		SettingsLayout(settings, rec), 
		background_color="#ccccdc",
		button_color=accent,
		font=defaultFont,
		text_justification="center",
		border_depth=None
	)
	
	while True:
		event, values = window.read()
		window["-SVOL-"].bind("<ButtonRelease-1>", window["-SVOL-"].update())
		if event == "-SVOL-":
			settings[0] = values["-SVOL-"]
			try:
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "volume", '+ str(values["-SVOL-"]) +']}'), stdout=subprocess.PIPE).stdout)
			except:
				print("MPV is not running")

		if event == "-SSUBMIT-":
			f = open(home + "settings.pkl", 'wb')
			pickle.dump(settings, f)
			f.close()
			window.close()
			break

		if event == "-SCANCEL-":
			window.close()
			break

#-------------------------------------------------
# DEFINE MAIN WINDOW LAYOUT
#-------------------------------------------------

# Spotify Songs
SongList = [
	[
	sg.Button(image_filename=home + "icons/search.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SEARCH-"),
	sg.Text("Songs", background_color=background,  expand_x=True),
	sg.Button(image_filename=home + "icons/edit.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-EDIT-")
	],
	[
	sg.Listbox(values=spotList, background_color=foreground, font=defaultFont, text_color=textc, no_scrollbar=True, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-SONGS-")], 
	[
	sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, key="-INSEARCH-")
	]
]

# Local Files
Local = [
	[
	sg.Button(image_filename=home + "icons/add.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-ADD-"),
	sg.Text("Local", background_color=background, expand_x=True),
	sg.Button(image_filename=home + "icons/playlist.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-PLAYLIST-")
	],
	[
	sg.Listbox(values=localMain, background_color=foreground, text_color=textc, no_scrollbar=True, size=(1,1), enable_events=True, expand_y=True, expand_x=True, key="-LOCAL-")
	] 
]

# Queued Songs
Queue = [
	[
	sg.Button(image_filename=home + "icons/navi.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-NAVIFY-"),
	sg.Text("Queue",background_color=background,  expand_x=True),
	sg.Button(image_filename=home + "icons/settings.png", enable_events=True, mouseover_colors=hover, border_width=0, key="-SETTINGS-")
	],
	[
	sg.Listbox(values=["[CLEAR]"], background_color=foreground, text_color=textc, no_scrollbar=True, size=(1,1), enable_events=True, key="-QUEUE-", expand_y=True, expand_x=True)
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
	sg.Column(Local, expand_y=True,background_color=background,  expand_x=True), # Local Songs
	sg.VSeparator(color=None),
	sg.Column(SongList, expand_y=True,background_color=background,  expand_x=True), # Spotify Songs
	sg.VSeparator(color=None),
	sg.Column(Queue, expand_y=True, background_color=background, expand_x=True) # Queued Songs
	],
	[
	sg.Slider(range=(0,1), default_value=0, enable_events=True, background_color=foreground, trough_color=foreground, orientation='h', disable_number_display=True, border_width = 1, expand_x=True, key="-BAR-") # Progress Bar
	],
	[
	sg.Column(BottomBar, background_color=background, expand_x=True) # Play Bar
	]
]

# Create the window
window = sg.Window("Navify", 
		   layout, keep_on_top=False, 
		   force_toplevel=False, 
		   no_titlebar=False, 
		   resizable=True, 
		   auto_size_text=True, 
		   use_default_focus=True, 
		   alpha_channel=0.8, 
		   background_color=background, 
		   button_color=accent,
		   font=defaultFont,
		   text_justification="center",
		   return_keyboard_events=True,
		   border_depth=None
		  )

#-------------------------------------------------
# MAIN LOOP
#-------------------------------------------------

def Player():
	global spotList
	global level
					   
	# Default Values
	isPlaying=False # Set to True When a Song Gets Played
	navify=False # Set to True when the Navify event is called
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
		event, values = window.read(timeout=100)
				
		# Networking
		try:
			if pN.is_alive() == False:
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

		# Resets after the song is finished		
		if isPlaying == True:
			if finished=p.get(finished) == True:
				p.join()
				isPlaying=False

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
				print("Songs is not playing yet")
				
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

			if edit == True and level > 0 and isCache == True:
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

		# Append Navify to queue
		if navify==True:
			if len(pNa.put(tempQ)) > 0:
				genList()
				window["-SONGS-"].update(values=spotList)
				for i in range(len(tempList)):
					for x in range(len(ID)):
						if tempQ[i] == ID[x]:                
							queue.append(listed[x][0])
							if (repeat == 1):
								prequeue.append(listed[x][0])
							break
				window["-QUEUE-"].update(values=queue)
				tempQ=[]
				pNa.join()
				navify=False
						
		# END OF SONG WITH NO QUEUE EVENT    
		if len(queue) == 1 and isPlaying == False:          
			if repeat == 1:
				queue = ["[CLEAR]"]
				for i in range(len(prequeue)):
					queue.append(prequeue[i])
			else:
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
					finished = Process.Queue(False)
					p = Process(target=Play, args=(i, finished, ), daemon=True)
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
		if event == "-NAVIFY-" and navify == False: 
			navify = True
			tempQ = Process.Queue([])
			pNa = Process(target=Navify, args=(tempQ, ), daemon=True)
			pNa.start()
			
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

		if event == sg.WIN_CLOSED:
			break

		if time != 0:
			time=time-100

#-------------------------------------------------
# NETWORKING
#-------------------------------------------------
def Listener(cmd):
	global s
	s.listen(5)
	while True:	
		c, a = s.accept() 
		print (a, " connected to the server")
		cmd.put(c.recv(1024).decode())
		c.close()
		print(a, " left the server (Disconnected by user)")
		break

viewAllCondense(viewAll(home[0:len(home) - len(playerLoc)] +"/Music"), viewAll(home + "playCache")) # Appends local files to the listed array because I am too lazy to come up with a better solution
Player()

#-------------------------------------------------
# END AND CLEANUP
#-------------------------------------------------
		  
window.close() # Closes the window
s.shutdown(socket.SHUT_RDWR) # Shuts down the server
s.close() 
		  
process = subprocess.Popen([home + "scripts/display/killmpv.sh"], stdout=subprocess.PIPE, text=True) # Stops the music player
process=process.communicate()[0][4:]
for i in range(0,len(process)):
	if not " " in process[i:i+1]:
		process=process[i:]
		break
for i in range(0, len(process)):
	if " " in process[i:i+1]:
		process=process[0:i]
		break
subprocess.run(["kill", process])        
