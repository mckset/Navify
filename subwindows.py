# System
import pickle
import subprocess
import os
import sys
import webbrowser

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
defaultFont=("Mono", "20")
smallFont=("Mono", "16")

# GUI Colors
background="#ccccdc"
foreground="#99aabf"
accent="#99aabf"
highlight="#bbccdf"
hover=("","#67778f")
textc="#ffffff"
alpha=1

home=os. getcwd() + '\\' # Location of python script

header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}

def theme():
	global background
	global foreground
	global accent
	global highlight
	global hover
	global textc
	global alpha
	global defaultFont
	global smallFont

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
		defaultFont=(t[7], t[8])
		smallFont=(t[7], t[9])
		scroll = t[10]


#-------------------------------------------------
# SUB-WINDOW LAYOUTS
#-------------------------------------------------	

def AddLayoutBL(files):
	layoutBList = [
		[
		sg.Text("Blacklisted",text_color=textc, background_color=background, expand_x=True),
		sg.Text("Removed",text_color=textc, background_color=background, expand_x=True)
		],
 		[
		sg.Listbox(values=files, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-BBL-"),
		sg.VSeparator(color=None),
		sg.Listbox(values=[], background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-BRM-")	
		],
		[
		sg.Button("Cancel", expand_x=True, enable_events=True, mouseover_colors=hover, border_width=0, font=smallFont,key="-BCANCEL-"),
		sg.Button("Submit", expand_x=True, enable_events=True, mouseover_colors=hover, border_width=0,font=smallFont, key="-BSUBMIT-")
		]
	]
	return layoutBList;

def AddLayoutSpot():
	Search = [
		[
		sg.Text("Search For A Song: ", text_color=textc, background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,  visible=True, key="-ASEARCH-"),
		sg.Button("Search", enable_events=True, mouseover_colors=hover, border_width=0, key="-AENTER-")
		]
	]
	SpotResults = [
		[
		sg.Text("Results:",text_color=textc,  background_color=background),
		sg.Listbox(values=[], auto_size_text=True, background_color=foreground, text_color=textc, size=(25,1), no_scrollbar=False,disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-ASRESULTS-"),
		sg.Button("Select", enable_events=True, mouseover_colors=hover, disabled=True, border_width=0, key="-ASEL-")
			]
		]
	Results = [
		[
		sg.Text("Links:", text_color=textc,  background_color=background),
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
		sg.Text("", text_color=textc, background_color=background, justification="center", key="-ANAME-")],
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
		sg.Text("Search For A Song: ", text_color=textc, background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,  visible=True, key="-ASEARCH-"),
		sg.Button("Search", enable_events=True, mouseover_colors=hover, border_width=0, key="-AENTER-")
		]
	]
	Results = [
		[
		sg.Text("Results:",text_color=textc,  background_color=background, expand_x=True)
		],
		[
		sg.Listbox(values=[], auto_size_text=True, background_color=foreground, text_color=textc, size=(25,1), no_scrollbar=False, disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-ARESULTS-")]
		]

	Name = [
		[
		sg.Text("Name: ", text_color=textc, background_color=background, expand_x=True),
		sg.Input(text_color=textc, background_color=foreground, disabled_readonly_background_color = highlight, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, key="-ANAME-"),
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
		sg.Listbox(values=folders, background_color=foreground,auto_size_text=True, text_color=textc, size=(25,1), no_scrollbar=False,disabled=False, enable_events=True,  expand_y=True, expand_x=True, key="-ACREATE-"),
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
		sg.Text("Name: ", text_color=textc, background_color=background),
		sg.Input(name, text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-ENAME-")
		],
		[
		sg.Text("URL: ", text_color=textc, background_color=background),
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
		sg.Text("Name: ", text_color=textc, background_color=background),
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
		sg.Text("Pick A Playlist",text_color=textc, background_color=background, expand_x=True),
		sg.Text("Selected",text_color=textc, background_color=background, expand_x=True)
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
		sg.Text("Volume",text_color=textc, background_color=background),
		sg.Text("Liked", text_color=textc, background_color=background, expand_x=True),
		sg.Text("Selected",text_color=textc,  background_color=background, expand_x=True)
		],
		[
		sg.Slider(range=(0,150), background_color=background,trough_color = foreground, default_value=settings[0], expand_y=True, enable_events=True, key="-SVOL-"),
		sg.Listbox(values=likes, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-LSONGS-"),
		sg.Listbox(values=rec, background_color=foreground, auto_size_text=True, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-SSEL-")		
		],
		[
		sg.Text("Local Songs Location: ",text_color=textc,  background_color=background, justification='right'),
		sg.Input(settings[2], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-SLOCAL-")
		],
		[
		sg.Text("Add Location: ",text_color=textc,  background_color=background, justification='right'),		
		sg.Text("Local", text_color=textc, background_color=background, justification='right'),
		sg.Slider(range=(0,1), size=(7,15), background_color=background,trough_color = foreground, default_value=settings[1], orientation='h', disable_number_display=True, enable_events=True, key="-SBAR-"),		
		sg.Text("Cache", text_color=textc, background_color=background, justification='right'),
		sg.Button("CANCEL", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SCANCEL-"),
		sg.Button("THEME", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-STHEME-"),
		sg.Button("BLACKLIST", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SBL-"),
		sg.Button("SUBMIT", button_color=foreground, mouseover_colors=hover, border_width=0,enable_events=True, key="-SSUBMIT-")
		]        
	]
	return layoutSettings

def ThemeLayout(theme):
	layoutSettings = [
		[
		sg.Text("Foreground",text_color=textc,  background_color=background),
		sg.Input(theme[0], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TFOR-")
		],
		[
		sg.Text("Background",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[1], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TBAC-")
		],		
		[
		sg.Text("Text",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[2], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TTEX-")		
		],
		[
		sg.Text("Highlight", text_color=textc, background_color=background, expand_x=True),
		sg.Input(theme[3], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-THIG-")		
		],
		[
		sg.Text("Accent",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[4], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TACC-")		
		],
		[
		sg.Text("Hover",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[5], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-THOV-")		
		],
		[
		sg.Text("Alpha",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[6], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TALF-")		
		],
		[
		sg.Text("Font",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[7], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TFNT-")		
		],
		[
		sg.Text("Font Size",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[8], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TFSZ-")		
		],
		[
		sg.Text("Small Font Size",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[9], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TSMF-")		
		],
		[
		sg.Text("Scroll Factor",text_color=textc,  background_color=background, expand_x=True),
		sg.Input(theme[10], text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-TSCL-")		
		],
		[sg.Text("All colors must be 7 characters long and includ a #", text_color=textc, background_color=background, expand_x=True)],
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

# Edits the songs in the blacklist folder
def Blacklist():
	listed=[]
	sortListed=[]
	ID=[]
	sortID=[]
	prevListed=[]
	combinedList=[]
	currentFile=""

   	# Lists tracks in the Cache folder (Spotify Cache)
	tempID=next(walk(home + "blacklist\\"), (None, None, []))[2]
	for i in range(len(tempID)):
		currentFile = os.popen("type " + home + "blacklist\\" + tempID[i]).read()
		prevListed.append((currentFile[44:]))
		sortListed.append((currentFile[44:]).upper())
		sortID.append(tempID[i])

	# Removes 'The' from the beginning of tracks to better sort
	for i in range(len(sortListed)):
		if "THE " == sortListed[i][0:4]:
			sortListed[i] = sortListed[i][4:] + ", THE"

	# Sorts the tracks alphabetically
	for i in range(len(sortID)):
		combinedList.append([sortListed[i],sortID[i]])    
	combinedList.sort()  

	# Stores the sorted values in the lists
	for i in range(len(sortID)):
		ID.append(combinedList[i][1])
		listed.append(combinedList[i][0])   

	# Adds "The " back into the track name
	for i in range(len(listed)):
		if ", The".lower() in listed[i].lower():
			listed[i] = "The " + listed[i][0:len(listed[i])-5]

	# Removes line breaks if they are at the end of the song      
	for i in range(len(listed)):
		if "\n" in listed[i]:
			listed[i]=listed[i][0:len(listed[i])-1]

	# Returns the name back to the way it was
	for i in range(len(listed)):
		for x in range(len(prevListed)):
			if listed[i].lower() in prevListed[x].lower():
				listed[i] = prevListed[x]
				break

	window = sg.Window(
			"Edit Blacklist", 
			AddLayoutBL(listed), 
			force_toplevel = True,
		  	background_color=background, 
 		   	button_color=accent,
   		   	font=defaultFont,
		   	text_justification="left",
		   	border_depth=None
		  	)

	selected=[]
	selID=[]
	while True:
		event, values = window.read()
		
		if event == "-BCANCEL-" or event == sg.WIN_CLOSED:    
			window.close()
			break

		if event == "-BSUBMIT-":    
			window.close()
			for i in range(len(selID)):
				os.system("move " + home + "blacklist\\" + selID[i] + " " + home + "cache")
			break

		if event == "-BBL-":
			selected.append(values["-BBL-"][0])
			selID.append(ID[window["-BBL-"].get_indexes()[0]])
			del ID[window["-BBL-"].get_indexes()[0]]
			del listed[window["-BBL-"].get_indexes()[0]]


		if event == "-BRM-" and len(selected) > 0:
			listed.append(values["-BRM-"][0])
			ID.append(ID[window["-BRM-"].get_indexes()[0]])
			del selID[window["-BRM-"].get_indexes()[0]]
			del selected[window["-BRM-"].get_indexes()[0]]	

			sortListed=list(listed)			
			sortID=list(ID)
			combinedList=[]
			listed=[]
			ID=[]

			# Removes 'The' from the beginning of tracks to better sort
			for i in range(len(sortListed)):
				if "THE " in sortListed[i][0:4]:
					sortListed[i] = sortListed[i][4:] + ", THE"

			# Sorts the tracks alphabetically
			for i in range(len(sortID)):
				combinedList.append([sortListed[i],sortID[i]])    
			combinedList.sort()  

			# Stores the sorted values in the lists
			for i in range(len(sortID)):
				ID.append(combinedList[i][1])
				listed.append(combinedList[i][0])   

			# Adds "The " back into the track name
			for i in range(len(listed)):
				if ", the" in listed[i].lower():
					listed[i] = "The " + listed[i][0:len(listed[i])-5]
			
			# Returns the name back to the way it was
			for i in range(len(listed)):
				for x in range(len(prevListed)):
					if listed[i].lower() == prevListed[x].lower():
						listed[i] = prevListed[x]
						break

		window["-BBL-"].update(values=listed)
		window["-BRM-"].update(values=selected)
			

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
			force_toplevel = True,
			resizable=True,
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
	search=""
	while True:
		event, values = window.read()
		
		if event == "-ACANCEL-" or event == sg.WIN_CLOSED:    
			window.close()
			break
		if event == "-ASEARCH-": 
			search=values["-ASEARCH-"]   
		if event == "-AENTER-" and len(search) > 0:
			tracks=[]
			ids=[]
			results = sp.search(q=search, limit=25)
			for i in range(len(results['tracks']['items'])):
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
			req=request.Request("https://youtube.com/results?search_query=" + parse.quote(url), headers=header)
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
			webbrowser.open(selectedLink)

		if event == "-ASUBMIT-":
			window.close()
			f = open(home + "cache/" + selectedID, 'w', encoding="utf-8")
			f.write(selectedLink + "\n" + selected)
			f.close()
			break
		
		if event == "-ALOCAL-":
			window.close()
			return False
			break

	return True

def AddYou():
	temp=next(walk(home + "playCache\\"), (None, None, []))[1]
	temp.sort()
	folders=["---create new folder---"]

	for i in range(0,len(temp)):
		folders.append(temp[i])

	window = sg.Window(
			"Add Song", 
			AddLayoutYou(folders), 
			resizable=True,
			force_toplevel = True,
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
		
		if event == "-ACANCEL-" or event == sg.WIN_CLOSED:    
			window.close()
			break

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
			req=request.Request("https://youtube.com/results?search_query=" + parse.quote(url), headers=header)
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
			if values["-ACREATE-"][0] != "---create new folder---":
				sfolder=values["-ACREATE-"][0]
			else:
				sfolder=""
				fname=""
				layoutAdd2 = [
					[
					sg.Text("Create A New Folder ",text_color=textc,  background_color=background, expand_x=True)
					],
					[
					sg.Text("Name: ", text_color=textc, background_color=background, expand_x=True),
					sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, key="-ANAME2-"),
					sg.Button("Create", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACREATE2-", disabled=True),
					sg.Button("Cancel", enable_events=True, mouseover_colors=hover, border_width=0, key="-ACANCEL2-")
					]
				]

				window2 = sg.Window(
					"New Folder", 
					layoutAdd2,
					resizable=True,
					force_toplevel = True,
					background_color=background, 
		  			button_color=accent,
		   		   	font=defaultFont,
				   	text_justification="center",
					border_depth=None
				)
				while True:
					event2, values2 = window2.read()

					if event2 == "-ACANCEL2-" or event2 == sg.WIN_CLOSED:
						window2.close()
						break

					if event2 == "-ACREATE2-" and len(fname) > 0:
						os.system("mkdir " + home + "playCache\\" + fname)
						window2.close()
						break

					if event2 == "-ANAME2-":
						fname=values2["-ANAME2-"]
						if len(fname) > 0:
							window2["-ACREATE2-"].update(disabled=False)
					else:
						window2["-ACREATE2-"].update(disabled=True)

				temp=next(walk(home + "playCache\\"), (None, None, []))[1]
				folders=["---create new folder---"]
				temp.sort()
				for i in range(0,len(temp)):
					folders.append(temp[i])
				window["-ACREATE-"].update(values=folders)



		if event == "-AOPEN-":
			webbrowser.open(selected)

		if len(name) > 0 and len(sfolder) > 0:
			window["-ASUBMIT-"].update(disabled=False)
		else:
			window["-ASUBMIT-"].update(disabled=True)

		if event == "-ASUBMIT-":
			if not exists(home + "playCache\\" + sfolder + "\\" + name):
				os.system("echo  '' > " + home + "playCache\\" + sfolder + "\\" + name)
			f = open(home + "playCache\\" + sfolder + "\\" + name, 'w', encoding="utf-8")
			f.write(content)
			f.close()
			window.close()
			break
		
		if event == "-ACACHE-":
			window.close()
			return False
			break

	return True

def Edit(name, link, ID, t):
	if t != 2:
		window = sg.Window(
				"Edit Song", 
				EditLayout(name, link), 
				resizable=True,
				force_toplevel = True,
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
			resizable=True, 
			force_toplevel = True,
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

		if event == "-ECANCEL-" or event == sg.WIN_CLOSED:
			window.close()
			return 0;
			break	

		if event == "-ENAME-":
			tempName = values["-ENAME-"]

		if event == "-ELINK-":
			tempLink = values["-ELINK-"]	

		if event == "-EOPEN-":
			webbrowser.open(link)
		if event == "-ESUBMIT-":
			if tempName != name or tempLink != link:
				if t == 0:
					f = open(home + "cache\\" + ID, 'w', encoding="utf-8")
					f.write(tempLink + "\n" + tempName)
					f.close()
				if t == 1:
					tempLink = tempLink[len(tempLink)-11:]
					if not tempLink in ID[len(ID)-11:]:
						os.remove(ID)
						ID=ID[0:len(ID)-11] + tempLink
					f = open(ID, 'w', encoding="utf-8")
					f.write(tempName)
					f.close()
				if t == 2:
					path=""
					for i in range(len(ID)-1):
						if '\\' in ID[len(ID)- i - 1: len(ID)-i]:
							path=ID[0:len(ID)-i]
							break
					oldName=name+link[len(link)-4:]
					newName = tempName + link[len(link)-4:]
					os.system("move " + path + oldName + " " + path + newName)
				window.close()
				return 1;
				break

def Playlist(listed):
	files=["---create new---"]
	temp=next(walk(home + "playlists\\"), (None, None, []))[2]
	temp.sort()
	songs=[]
	songsPaths=[]
	selected=[]
	selectedPaths=[]
	playlist=""
	x=0
	y=1
	a=-1
	for i in range(0,len(temp)):
		files.append(temp[i])
	for i in range(len(listed)):
		if not listed[i][x] == "..." and a < i:
			songs.append(listed[i][x])
			songsPaths.append(listed[i][y])
		elif a < i:
			songs.append("")
			songs.append("[LOCAL TRACKS]")
			songsPaths.append("")
			songsPaths.append("")
			a=i+2
			x=1
			y=0

	window = sg.Window(
		"Select Playlist", 
		PlaylistLayout(files), 
		resizable=True,
		force_toplevel = True,
		background_color=background, 		
		button_color=accent,
   		font=defaultFont,
	   	text_justification="center", 
		border_depth=None
	)
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
				selectedPaths=[]
			if values["-PPLAYLISTS-"][0] == "---create new---" or edit == True:
				Left = [
					[
					sg.Text("Songs", text_color=textc, background_color=background,expand_x=True)
					],
					[
					sg.Listbox(values=songs, auto_size_text=True, background_color=foreground, text_color=textc, no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PSONGS2-")
					]
				]
				Right = [
					[
					sg.Text("Selected", text_color=textc, background_color=background,expand_x=True)		
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
					force_toplevel = True,
					resizable=True,
					background_color=background, 
					button_color=accent,
					font=defaultFont,
					text_justification="center",
					border_depth=None, 
					finalize=True
				)
				while True:
					event2, values2 = window2.read()

					if event2 == "-PSONGS2-" and values2["-PSONGS2-"][0] != "[LOCAL TRACKS]" and len(values2["-PSONGS2-"][0]) > 0:
						valid=1						
						selected.append(str(len(selected)) + ": " + values2["-PSONGS2-"][0])
						selectedPaths.append(songsPaths[window2["-PSONGS2-"].get_indexes()[0]])

						window2["-PSELECTED2-"].update(values=selected)

					if event2 == "-PSELECTED2-" and len(selected) > 0:
						del selected[window2["-PSELECTED2-"].get_indexes()[0]]
						del selectedPaths[window2["-PSELECTED2-"].get_indexes()[0]]
						for i in range(int(values2["-PSELECTED2-"][0][0:1]),len(selected)):
							selected[i] = str(i) + selected[i][len(str(i+1)):]
						window2["-PSELECTED2-"].update(values=selected)

					if event2 == "-PSUBMIT2-" and len(selected) > 0:
						if edit == False:
							layoutP3=[
							[
								sg.Text("Name: ", text_color=textc, background_color=background, expand_x=True),
								sg.Input(text_color=textc, background_color=foreground, enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,key="-PNAME3-"),
								sg.Button("Create", enable_events=True, font=defaultFont, button_color=foreground, mouseover_colors=hover, border_width=0, key="-PCREATE3-")
							]
							]
							window3 = sg.Window(
								"Create Playlist",
								layoutP3,
								force_toplevel = True,
								resizable=True,
								background_color=background, 
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
							f = open(home + "playlists\\" + name, 'w', encoding="utf-8")
							content=""							
							for i in range(0, len(selected)):
								if len(selectedPaths[i]) > 0:
									content = content + selected[i][len(str(i))+2:] + "\n"
								else:
									content = content + selectedPaths[i][len(str(i))+2:] + "\n"
							f.write(content)
							f.close()
							files=["---create new---"]
							temp=next(walk(home + "playlists\\"), (None, None, []))[2]
							temp.sort()
							for i in range(0,len(temp)):
								files.append(temp[i])
							window["-PPLAYLISTS-"].update(values=files)
							window["-PSEL-"].update(values=[])
							window2.close()
							break							

					if event2 == "-PCANCEL2-" or event2 == sg.WIN_CLOSED:
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
				f = open(home + "playlists\\" + playlist)
				selected=[]			
				while True:
					line = f.readline()
					if not line:
						break
					if "\n" in line:
						line=line[0:len(line) - 1]
					cache=1
					for i in range(len(songsPaths)):
						if line in songsPaths[i]:
							cache = 0
							selected.append(songs[i])
							selectedPaths.append(songsPaths[i])
							break
					if cache == 1: 
						selected.append(line)
						for i in range(len(songs)):
							if selected[len(selected)-1] == songs[i]:
								selectedPaths.append(songsPaths[i])
								break
				
					window["-PSEL-"].update(values=selected)

		if event == "-PSUBMIT-" and len(playlist) > 0:
			window.close()
			break

		if event == "-PCANCEL-" or event == sg.WIN_CLOSED:
			selected=[]
			selectedPaths=[]
			window.close()
			break
	
	return selected, selectedPaths

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
		resizable=True,
		force_toplevel = True,
		background_color=background,
		button_color=accent,
		font=defaultFont,
		text_justification="center",
		border_depth=None
	)
	x=0
	while True:
		event, values = window.read()
		if event == "-SVOL-":
			try:
				os.system('echo set volume ' + str(values["-SVOL-"]) + ' >\\\\.\\pipe\\mpvsocket')
			except:
				#print("MPV is not running")
				pass

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
		if event == "-SBL-":
			Blacklist()

		if event == "-SSUBMIT-":
			local=settings[2]			
			if values["-SLOCAL-"] != settings[2] and exists(values["-SLOCAL-"]):
				local = values["-SLOCAL-"]
					
			f = open(home + "settings.pkl", 'wb')
			pickle.dump([values["-SVOL-"], values["-SBAR-"], local], f)
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
				theme()
				Settings(sp)
				return 1

		if event == "-SCANCEL-" or event == sg.WIN_CLOSED:		
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
		resizable=True,
		force_toplevel = True,
		background_color=background,
		button_color=accent,
		font=defaultFont,
		text_justification="center",
		border_depth=None
	)
	fore = t[0]
	back = t[1]
	textc = t[2]
	high = t[3]
	acc = t[4]
	hov = t[5]
	alf = t[6]
	fnt = t[7]
	fntSize = t[8]
	smlSize = t[9]	
	scroll = t[10]


	while True:
		event, values = window.read()
		
		if event == "-TDEF-":
			window["-TBAC-"].update("#ccccdc")
			window["-TFOR-"].update("#99aabf")
			window["-TTEX-"].update("#ffffff")
			window["-THIG-"].update("#bbccdf")
			window["-TACC-"].update("#99aabf")
			window["-THOV-"].update("#67778f")
			window["-TALF-"].update("1")
			window["-TFNT-"].update("Mono")
			window["-TFSZ-"].update("20")
			window["-TSMF-"].update("16")
			window["-TSCL-"].update("13")
			
		if event == "-TCANCEL-" or event == sg.WIN_CLOSED:
			window.close()
			return 0
		
		if event == "-TSUBMIT-":
			fore = values["-TFOR-"]
			back = values["-TBAC-"]
			textc = values["-TTEX-"]
			high = values["-THIG-"]
			acc = values["-TACC-"]
			hov = values["-THOV-"]
			alf = values["-TALF-"]
			fnt = values["-TFNT-"]
			fntSize = values["-TFSZ-"]
			smlSize = values["-TSMF-"]
			scroll = values["-TSCL-"]	

			t = [fore, back, textc, high, acc, hov, alf, fnt, fntSize, smlSize, scroll]
			valid=1
			for i in range(len(t)-5):
				if t[i][0] != '#':
					valid=0
					break
			try:
				int(t[8])
				int(t[9])
				int(t[10])
			except:
				valid=0
			if valid == 1:
				f = open(home + "theme.pkl", 'wb')
				pickle.dump(t,f)
				f.close()
				window.close()
				return t
theme()
