# System
import pickle
import subprocess
import os
import sys

from os.path import exists
from os import walk

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# YouTube 
from urllib import request, parse
import requests
import io
from PIL import Image
import PySimpleGUI as sg

# Fonts
defaultFont="Inter 40"
smallFont="Inter 32"

home=os. getcwd() + '/' # Location of python script

# GUI Colors
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

header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}



#-------------------------------------------------
# SUB-WINDOW LAYOUTS
#-------------------------------------------------	

def AddLayoutSpot():
	Search = [
		[
		sg.Text("Search For A Song: ", background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,  visible=True, key="-ASEARCH-"),
		sg.Button("Search", enable_events=True, mouseover_colors=hover, border_width=0, key="-AENTER-")
		]
	]
	SpotResults = [
		[
		sg.Text("Results:", background_color=background),
		sg.Listbox(values=[], auto_size_text=True, background_color=foreground, text_color=textc, size=(25,1), no_scrollbar=False,disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-ASRESULTS-"),
		sg.Button("Select", enable_events=True, mouseover_colors=hover, disabled=True, border_width=0, key="-ASEL-")
			]
		]
	Results = [
		[
		sg.Text("Links:", background_color=background),
		sg.Listbox(values=[], auto_size_text=True, background_color=foreground, text_color=textc, size=(25,1), no_scrollbar=False,disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-ARESULTS-"),
		sg.Button("Submit", enable_events=True, mouseover_colors=hover, border_width=0, key="-ASUBMIT-", disabled=True)
			]
		]
	Buttons = [
		[
		sg.Button("Local", enable_events=True, mouseover_colors=hover, border_width=0, key="-ALOCAL-", expand_x=True)
		],
		[
		sg.Button("Open", enable_events=True, mouseover_colors=hover, border_width=0, key="-AOPEN-", disabled=True, expand_x=True)
		],
		[
		sg.Button("Cancel", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACANCEL-", expand_x=True)
		]
	]	
	
	Image = [
		[
		sg.Text("", text_color=accent, background_color=background, expand_x=True, justification="center", key="-ANAME-")],
		[
		sg.Image(source=None, background_color=background,size=(256,192), expand_x=True, key="-AIMAGE-") # Thumbnail	
		]
	]

	layoutAdd = [
		[
		sg.Column(Search, expand_y=True, background_color=background,expand_x=True) # Search
		],
		[
		sg.Column(SpotResults, expand_y=True, background_color=background,expand_x=True) # SpotResults
		],
		[
		sg.Column(Results, expand_y=True, background_color=background,expand_x=True) # Results
		],
		[
		sg.Column(Buttons, expand_y=True, background_color=background),
		sg.VSeparator(color=None),
		sg.Column(Image, expand_y=True, background_color=background),
		]
	]
	return layoutAdd



def AddLayoutYou(folders):
	Search = [
		[
		sg.Text("Search For A Song: ", background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,  visible=True, key="-ASEARCH-"),
		sg.Button("Search", enable_events=True, mouseover_colors=hover, border_width=0, key="-AENTER-")
		]
	]
	Results = [
		[
		sg.Text("Results:", background_color=background, expand_x=True)
		],
		[
		sg.Listbox(values=[], auto_size_text=True, background_color=foreground, text_color=textc, size=(25,1), no_scrollbar=False,disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-ARESULTS-")]
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
		sg.Button("Cache", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACACHE-", disabled=False),
		sg.Button("Open", enable_events=True, mouseover_colors=hover, border_width=0, key="-AOPEN-", disabled=True),
		sg.Button("Cancel", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACANCEL-"),
		sg.VSeparator(color=None),
		sg.Image(source=None, background_color=background,size=(256,192), key="-AIMAGE-") # Thumbnail
		]
	]
	return layoutAdd

def EditLayout(name, link):
	layoutEdit = [
		[
		sg.Text("Name: ", background_color=background),
		sg.Input(name, text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-ENAME-")
		],
		[
		sg.Text("URL: ", background_color=background),
		sg.Input(link, text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-ELINK-")
		],
		[
		sg.Button("Cancel", button_color=foreground, mouseover_colors=hover, border_width=0, expand_x=True, enable_events=True, key="-ECANCEL-"),
		sg.Button("Open", button_color=foreground, mouseover_colors=hover, border_width=0, expand_x=True, enable_events=True, key="-EOPEN-"),
		sg.Button("Submit", button_color=foreground, mouseover_colors=hover, border_width=0, expand_x=True, enable_events=True, key="-ESUBMIT-")		
		
		]
	]
	return layoutEdit

def EditLayoutLocal(name):
	layoutEdit = [
		[
		sg.Text("Name: ", background_color=background),
		sg.Input(name, text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-ENAME-")
		],
		[
		sg.Button("Cancel", button_color=foreground, mouseover_colors=hover, border_width=0, expand_x=True, enable_events=True, key="-ECANCEL-"),
		sg.Button("Submit", button_color=foreground, mouseover_colors=hover, border_width=0, expand_x=True, enable_events=True, key="-ESUBMIT-")		
		
		]
	]
	return layoutEdit

def PlaylistLayout(files):
	layoutPlaylist = [
		[
		sg.Text("Pick A Playlist",background_color=background, expand_x=True),
		sg.Text("Selected",background_color=background, expand_x=True)
		],
 		[
		sg.Listbox(values=files, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PPLAYLISTS-"),
		sg.VSeparator(color=None),
		sg.Listbox(values=[], background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PSEL-")	
		],
		[
		sg.Button("Cancel", expand_x=True, enable_events=True, mouseover_colors=hover, border_width=0, font=smallFont,key="-PCANCEL-"),
		sg.Button("Edit", expand_x=True, enable_events=True, mouseover_colors=hover, border_width=0, font=smallFont,key="-PEDIT-"),
		sg.Button("Submit", expand_x=True, enable_events=True, mouseover_colors=hover, border_width=0,font=smallFont, key="-PSUBMIT-")
		]	
	]
	return layoutPlaylist

def SettingsLayout(settings, likes, rec):
	layoutSettings = [
		[
		sg.Text("Volume", background_color=background),
		sg.Text("Liked", background_color=background, expand_x=True),
		sg.Text("Selected", background_color=background, expand_x=True)
		],
		[
		sg.Slider(range=(0,150), background_color=background,trough_color = foreground, default_value=settings[0], expand_y=True, enable_events=True, key="-SVOL-"),
		sg.Listbox(values=likes, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-LSONGS-"),
		sg.Listbox(values=rec, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=True, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-SSEL-")		
		],
		[
		sg.Text("Add Location: ", background_color=background, justification='right'),		
		sg.Text("Local", background_color=background, justification='right'),
		sg.Slider(range=(0,1), size=(7,15), background_color=background,trough_color = foreground, default_value=settings[1], orientation='h', disable_number_display=True, enable_events=True, key="-SBAR-"),		
		sg.Text("Cache", background_color=background, justification='right'),
		sg.Button("SUBMIT", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SSUBMIT-"),
		sg.Button("CANCEL", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SCANCEL-"),
		sg.Button("THEME", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-STHEME-")
		]        
	]
	return layoutSettings

def ThemeLayout(theme):
	layoutSettings = [
		[
		sg.Text("Foreground", background_color=background),
		sg.Input(theme[0], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TFOR-")
		],
		[
		sg.Text("Background", background_color=background, expand_x=True),
		sg.Input(theme[1], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TBAC-")
		],		
		[
		sg.Text("Text", background_color=background, expand_x=True),
		sg.Input(theme[2], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TTEX-")		
		],
		[
		sg.Text("Highlight", background_color=background, expand_x=True),
		sg.Input(theme[3], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-THIG-")		
		],
		[
		sg.Text("Accent", background_color=background, expand_x=True),
		sg.Input(theme[4], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TACC-")		
		],
		[
		sg.Text("Hover", background_color=background, expand_x=True),
		sg.Input(theme[5], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-THOV-")		
		],
		[
		sg.Text("Alpha", background_color=background, expand_x=True),
		sg.Input(theme[6], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TALF-")		
		],
		[sg.Text("All colors must be 7 characters long and includ a #", background_color=background, expand_x=True)],
		[
		sg.Button("Cancel", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-TCANCEL-"),
		sg.Button("Default", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-TDEF-"),
		sg.Button("Submit", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-TSUBMIT-")
		]        
	]
	return layoutSettings

#-------------------------------------------------
# DEFINE SUB-WINDOWS
#-------------------------------------------------

# Adds a new song to a separate cache directory 
def Add(sp, layout):	
	results=False
	while results == False:
		if layout == "spot":
			results = AddSpot(sp)
			layout="you"	
		if layout == "you" and results != True:
			results = AddYou()
			layout = "spot"

def AddSpot(sp):
	window = sg.Window(
			"Add Song", 
			AddLayoutSpot(), 
		  	background_color=background, 
 		   	button_color=accent,
   		   	font=defaultFont,
		   	text_justification="left",
		   	border_depth=None
		  	)
	tracks=[]
	ids=[]
	selected=""
	selectedID=""
	selectedLink=""
	while True:
		event, values = window.read()
		if event == "-ASEARCH-": 
			search=values["-ASEARCH-"]   
		if event == "-AENTER-":
			tracks=[]
			ids=[]
			results = sp.search(q=search, limit=25)
			for i in range(len(results['tracks']['items'])):
				#print(str(results['tracks']['items'][i]['name']) + ' - ' + str(results['tracks']['items'][i]['artists'][0]['name']) + " : " + str(results['tracks']['items'][i]['id']))
				tracks.append(str(results['tracks']['items'][i]['name']) + ' - ' + str(results['tracks']['items'][i]['artists'][0]['name']))
				ids.append(results['tracks']['items'][i]['id'])
			window["-ASRESULTS-"].update(values=tracks, disabled=False)
			window["-ASEL-"].update(disabled=True)
			selected=""
			selectedID=""

		if event == "-ASRESULTS-":
			window["-ASEL-"].update(disabled=False)
			for i in range(len(tracks)):
				if tracks[i] == values["-ASRESULTS-"][0]:
					selected=tracks[i]
					selectedID=ids[i]

		if event == "-ASEL-":
			url=selected
			video=[]
			img=[]
			links=[]
			text=[]
			sfolder=""
			content=""
			name=""
			# Retrieves the song from Youtube
			for i in range(0,len(url)):
				if " " in url[i:i+1]:
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

			window["-ARESULTS-"].update(values=links, disabled=False)

		if event == "-ARESULTS-":
			window["-ASUBMIT-"].update(disabled=False)
			window["-AOPEN-"].update(disabled=False)
			selectedLink=values["-ARESULTS-"][0]
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
		if event == "-AOPEN-":
			subprocess.run(["gio", "open", selectedLink])

		if event == "-ASUBMIT-":
			window.close()
			f = open(home + "cache/" + selectedID, 'w')
			f.write(selectedLink + "\n" + selected)
			f.close()
			break
		
		if event == "-ALOCAL-":
			window.close()
			return False
			break

		if event == "-ACANCEL-":
			window.close()			
			break

	return True

def AddYou():
	temp=next(walk(home + "playCache/"), (None, None, []))[1]
	temp.sort()
	folders=["---create new---"]

	for i in range(0,len(temp)):
		folders.append(temp[i])

	window = sg.Window(
			"Add Song", 
			AddLayoutYou(folders), 
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
		
		if event == "-ACACHE-":
			window.close()
			return False
			break

		if event == "-ACANCEL-":    
			window.close()
			break

	return True

def Edit(name, link, ID, t):
	if t != 2:
		window = sg.Window(
				"Edit Song", 
				EditLayout(name, link), 
			  	background_color=background, 
	 		   	button_color=accent,
	   		   	font=defaultFont,
			   	text_justification="left",
			   	border_depth=None
			  	)
	else:
		window = sg.Window(
			"Edit Song", 
			EditLayoutLocal(name), 
		  	background_color=background, 
 		   	button_color=accent,
   		   	font=defaultFont,
		   	text_justification="left",
		   	border_depth=None
		  	)
	tempName=name
	tempLink=link
	while True:
		event, values = window.read()
	
		if event == "-ENAME-":
			tempName = values["-ENAME-"]

		if event == "-ELINK-":
			tempLink = values["-ELINK-"]	

		if event == "-EOPEN-":
			subprocess.run(["gio", "open", link])

		if event == "-ECANCEL-":
			window.close()
			break

		if event == "-ESUBMIT-":
			if tempName != name or tempLink != link:
				if t == 0:
					f = open(home + "cache/" + ID, 'w')
					f.write(tempLink + "\n" + tempName)
					f.close()
				if t == 1:
					tempLink = tempLink[len(tempLink)-11:]
					if not tempLink in ID[len(ID)-11:]:
						os.remove(ID)
						ID=ID[0:len(ID)-11] + tempLink
					f = open(ID, 'w')
					f.write(tempName)
					f.close()
				if t == 2:
					path=""
					for i in range(len(ID)-1):
						if '/' in ID[len(ID)- i - 1: len(ID)-i]:
							path=ID[0:len(ID)-i]
							break
					oldName=name+link[len(link)-4:]
					newName = tempName + link[len(link)-4:]
					subprocess.run(["mv", path + oldName, path + newName])
				window.close()
				break

def Playlist(listed):
	files=["---create new---"]
	temp=next(walk(home + "playlists/"), (None, None, []))[2]
	temp.sort()
	songs=[]
	selected=[]
	playlist=""

	for i in range(0,len(temp)):
		files.append(temp[i])
	for i in range(len(listed)):
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
	selected=[]
	edit=False
	while True:
		event, values = window.read()
		edit=False
		if event == "-PEDIT-" and len(playlist) > 0:
			edit = True
			for i in range(len(selected)):
				selected[i] = str(i) + ": " + selected[i]			

		if event == "-PPLAYLISTS-" or edit == True:
			if edit == False:
				selected=[]
			if values["-PPLAYLISTS-"][0] == "---create new---" or edit == True:
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
						for i in range(int(values2["-PSELECTED2-"][0][0:1]),len(selected)):
							selected[i] = str(i) + selected[i][len(str(i+1)):]
						window2["-PSELECTED2-"].update(values=selected)

					if event2 == "-PSUBMIT2-" and len(selected) > 0:
						if edit == False:
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
						else:
							name = values["-PPLAYLISTS-"][0]
						if len(name) > 0:
							f = open(home + "playlists/" + name, 'w')
							content=""							
							for i in range(0, len(selected)):
								content = content + selected[i][len(str(i))+2:] + "\n"
							f.write(content)
							f.close()
							files=["---create new---"]
							temp=next(walk(home + "playlists/"), (None, None, []))[2]
							temp.sort()
							for i in range(0,len(temp)):
								files.append(temp[i])
							window["-PPLAYLISTS-"].update(values=files)
							window["-PSEL-"].update(values=[])
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
						tempSort=[]
						l = len(values2["-PSEARCH2-"].lower())+1
						for x in range(1,len(values2["-PSEARCH2-"].lower())+1):	
							for i in range(len(newList)):
								if values2["-PSEARCH2-"].lower()[0:l-x] == newList[i].lower()[0:l-x]:
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
						window2["-PSONGS2-"].update(values=tempSort)

			else:
				playlist=values["-PPLAYLISTS-"][0]
				f = open(home + "playlists/" + playlist)
				selected=[]			
				while True:
					line = f.readline()
					if not line:
						break
					if "\n" in line:
						line=line[0:len(line) - 1]
					selected.append(line)
				window["-PSEL-"].update(values=selected)

		if event == "-PSUBMIT-" and len(playlist) > 0:
			window.close()
			break

		if event == "-PCANCEL-":
			selected=[]
			window.close()
			break
	ret = list(selected)
	return selected

def Settings(sp):
	global foreground
	global background
	global textc
	global highlight
	global accent
	global hover
	global alpha
	f = open(home + "settings.pkl", 'rb')
	settings = pickle.load(f)
	f.close()
	x=0
	rec=[]
	recId=[]
	likes=[]
	likesId=[]
	results=[]

	while True: 
		results.append(sp.current_user_saved_tracks(20, x))
		x+=20
		if (len(sp.current_user_saved_tracks(20, x)['items']) == 0):
			break

	for i in range(0, len(results)):
		for idx, item in enumerate(results[i]['items']):
			likes.append(item['track']['name'] + " - " + item['track']['artists'][0]['name'])
			likesId.append(item['track']['id'])
	f = open(home + "recommend.pkl", 'rb')
	rec = pickle.load(f)
	f.close()
	recId = list(rec)
	for x in range(len(rec)):
		for i in range(len(likes)):
			if rec[x] == likesId[i]:
				rec[x] = likes[i]
	window = sg.Window(
		"Settings", 
		SettingsLayout(settings, likes, rec), 
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
			try:
				subprocess.check_output(('socat', '-', '/tmp/mpvsocket'), stdin=subprocess.Popen(('echo', '{"command": ["set_property", "volume", '+ str(values["-SVOL-"]) +']}'), stdout=subprocess.PIPE).stdout)
			except:
				print("MPV is not running")

		if event == "-SSEL-" and len(rec) > 0:
			for i in range(len(rec)):
				if rec[i] == values["-SSEL-"][0]:
					del rec[i]
					del recId[i]
					break
		window["-SSEL-"].update(values=rec)
		
		if event == "-LSONGS-" and len(rec) < 5:
			valid=1
			for i in range(len(rec)):
				if rec[i] == values["-LSONGS-"][0]:
					valid=0
					break
			if valid == 1:
				for i in range(len(likes)):
					if likes[i] == values["-LSONGS-"][0]:
						rec.append(likes[i])
						recId.append(likesId[i])
						window["-SSEL-"].update(values=rec)
						break

		if event == "-SSUBMIT-":
			f = open(home + "settings.pkl", 'wb')
			pickle.dump([values["-SVOL-"], values["-SBAR-"]], f)
			f.close()
			window.close()
			f = open(home + "recommend.pkl", 'wb')
			pickle.dump(recId, f)
			f.close()
			break

		if event == "-STHEME-":
			r = Theme()
			if r != 0:
				window.close()
				foreground = r[0]
				background = r[1]
				textc = r[2]
				highlight = r[3]
				accent = r[4]
				hover = r[5]
				alpha = r[6]
				Settings(sp)
				break	

		if event == "-SCANCEL-":
			window.close()
			break

def Theme():
	t=[]
	if exists(home + "theme.pkl"):
		f = open(home + "theme.pkl", 'rb')
		t = pickle.load(f)
		f.close()
	else:
		return 0
	window = sg.Window(
		"Theme", 
		ThemeLayout(t), 
		background_color="#ccccdc",
		button_color=accent,
		font=defaultFont,
		text_justification="center",
		border_depth=None
	)
	foreground = t[0]
	background = t[1]
	textc = t[2]
	high = t[3]
	acc = t[4]
	hov = t[5]
	alf = t[6]
	
	while True:
		event, values = window.read()
		
		if event == "-TDEF-":
			background="#ccccdc"
			foreground="#99aabf"
			acc="#99aabf"
			high="#bbccdf"
			hov=("","#67778f")
			textc="#ffffff"
			alf=0.8

		if event == "-TCANCEL-":
			window.close()
			return 0
		
		if event == "-TSUBMIT-":
			foreground = values["-TFOR-"]
			background = values["-TBAC-"]
			textc = values["-TTEX-"]
			high = values["-THIG-"]
			acc = values["-TACC-"]
			hov = values["-THOV-"]
			alf = values["-TALF-"]

			t = [foreground, background, textc, high, acc, hov, alf]
			valid=1
			for i in range(len(t)-1):
				if len(t[i]) != 7 or t[i][0] != '#':
					valid=0
					break
			if valid == 1:
				f = open(home + "theme.pkl", 'wb')
				pickle.dump(t,f)
				f.close()
				window.close()
				return t
			
