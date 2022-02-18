import pickle
import subprocess
import os
import sys
import re
from os.path import exists
from os import walk

import PySimpleGUI as sg
files=["---create new---"]

defaultFont="Inter 40"
smallFont="Inter 32"

temp=next(walk("/home/seth/.navi/navify/playlists/"), (None, None, []))[2]
songs=[]
selected=[]

for i in range(0,len(temp)):
	files.append(temp[i])





def main(spot, local):
	global files
	selected=[]
	layout = [
	[
		sg.Text("Pick A PLaylist", justification="center", font=defaultFont,background_color="#ccccdc", expand_x=True)
	],
 	[
		sg.Listbox(values=files, auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-PLAYLISTS-")
	], 
	[
		sg.Button("Cancel", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, font=smallFont,key="-CANCEL2-"),
		sg.Button("Submit", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0,font=smallFont, key="-SUBMIT2-")
	]	
]


	playlist=""
	songs=spot
	for i in range(0, len(local)):
		songs.append(local[i])
	window2 = sg.Window("Select Playlist", layout, background_color="#ccccdc", border_depth=None)
	while True:
		event2, values2 = window2.read()

		if event2 == "-PLAYLISTS-":
			if values2["-PLAYLISTS-"][0] == "---create new---":


				Left = [
				[
						sg.Text("Songs", justification="center", font=defaultFont,background_color="#ccccdc", expand_x=True)
					],
					[
						sg.Listbox(values=songs, auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-SONGS3-")
					]
				]
				Right = [
				[
						sg.Text("Selected", justification="center", font=defaultFont,background_color="#ccccdc", expand_x=True)		
					],
					[
						sg.Listbox(values=selected, auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", no_scrollbar=False, size=(25,10), enable_events=True,  expand_y=True, expand_x=True, key="-SELECTED3-")
					]
				]

				# Create new window layout
				layout2 = [
					[
						sg.Column(Left, background_color="#ccccdc", expand_y=True, expand_x=True),
						sg.VSeparator(color=None),
						sg.Column(Right, background_color="#ccccdc", expand_y=True, expand_x=True)
					],
					[
						sg.Input(font=defaultFont, text_color="#ffffff", background_color="#aabbcf", enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=False, visible=True, key="-SEARCH2-"),					

						sg.Button("CANCEL", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0,font=smallFont, key="-CANCEL3-"),
						sg.Button("SUBMIT", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, font=smallFont,key="-SUBMIT3-")
					]
				]
				window3 = sg.Window("Create Playlist", layout2, background_color="#ccccdc", border_depth=None, finalize=True)
				
				
				while True:
					event3, values3 = window3.read()

					if event3 == "-SONGS3-":
						valid=1						
						selected.append(str(len(selected)) + ": " + values3["-SONGS3-"][0])
						window3["-SELECTED3-"].update(values=selected)

					if event3 == "-SELECTED3-" and len(selected) > 0:
						del selected[int(values3["-SELECTED3-"][0][0:1])]
						for i in range(0,len(selected)):
							selected[i] = str(i) + ": " + selected[i][3:]
						window3["-SELECTED3-"].update(values=selected)

					if event3 == "-SUBMIT3-" and len(selected) > 0:
						layout3=[
						[
							sg.Text("Name: ", justification="center", font=defaultFont,background_color="#ccccdc", expand_x=True),
							sg.Input(font=defaultFont, text_color="#ffffff", background_color="#aabbcf", enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=False, visible=True, key="-NAME4-"),
							sg.Button("Create", enable_events=True, font=defaultFont,button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-CREATE4-")
						]
						]
						window4 = sg.Window("Create Playlist", layout3, background_color="#ccccdc", border_depth=None, finalize=True)
				
						name=""
						while True:
							event4, values4 = window4.read()
							
							if event4 == "-NAME4-":
								name=values4["-NAME4-"]

							if event4 == "-CREATE4-":
								window4.close()
								break

						if len(name) > 0:
							f = open("/home/seth/.navi/navify/playlists/" + name, 'w')
							content=""							
							for i in range(0, len(selected)):
								content = content + selected[i][len(str(i))+2:] + "\n"
							f.write(content)
							f.close()
							window3.close()
							files=["---create new---"]
							temp=next(walk("/home/seth/.navi/navify/playlists/"), (None, None, []))[2]
							for i in range(0,len(temp)):
								files.append(temp[i])
							window2["-PLAYLISTS-"].update(values=files)

							break

					if event3 == "-CANCEL3-":
						window3.close()
						break

					if event3 == "-SEARCH2-":
						newList=[]
						for i in range(0, len(songs)):
							if values3["-SEARCH2-"].lower() in songs[i].lower():
								newList.append(songs[i])
						window3["-SONGS3-"].update(values=newList)

		if event2 == "-PLAYLISTS-":
			playlist=values2["-PLAYLISTS-"][0]
		#print(event2)

		if event2 == "-SUBMIT2-" and len(playlist) > 0:
			f = open("/home/seth/.navi/navify/playlists/" + playlist)
			selected=[]			
			while True:
				#print("a")
				line = f.readline()
				if not line:
					break
				if "\n" in line:
					line=line[0:len(line) - 1]
				selected.append(line)
			#print(selected)
			window2.close()
			break

		if event2 == "-CANCEL2-":
			window2.close()
			break
	#print(selected)
	return selected
#main(["test", "test2", "test3"], ["local1"])
