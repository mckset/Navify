# Navify GUI 

import pickle
import subprocess
import random
import os
import sys
import re
from os.path import exists
from os import walk
from multiprocessing import Process

import PySimpleGUI as sg

import navify
import popup
import playlist
import settings

defaultFont="Inter 40"
smallFont="Inter 32"

# Set to 0 to only list files in the playCache folder
includeCache=1
cacheI=-1

loc=[]
spotID=[]
spotList=[]
combinedList=[]
ID=[]
listed=[]
localList=[]
localID=[]
noName=0
track = ""
name=""
trackID=0
tempID=[]
likes=[]
currentTrack=""
folders=[]
locID=[]
inFolder=0


if exists("/home/seth/.navi/navify/GUI/isPlaying.txt"):
    os.remove("/home/seth/.navi/navify/GUI/isPlaying.txt")

def Play(x):
    track=ID[x]
    trackID=ID[x]    
    vol=100

    if exists("/home/seth/.navi/navify/settings.pkl"):
            f = open('/home/seth/.navi/navify/settings.pkl', 'rb')
            settings = pickle.load(f)
            f.close()
            vol=settings[0]

    subprocess.run(["mpv","--no-video", "--input-ipc-server=/tmp/mpvsocket", "--volume=" + str(vol), track])
    if exists("/home/seth/.navi/navify/GUI/isPlaying.txt"):
        os.remove("/home/seth/.navi/navify/GUI/isPlaying.txt")


subprocess.run(["clear"])


def upDesktop(x):
    global currentTrack

    # Dumps the info so the desktop can read it
    valid=0
    name=listed[x]
    print("Now Playing: " + name)
    print(ID[x])

    if "\n" in name:
        name=name[:len(name)-1]
    fname=name
    name = re.sub(r'[^\x00-\x7f]',r'', name)

    if len(name) > 16:
        name = str(name)[0:len(name)] + " | "

    for i in range(0,len(loc)):
        
        if listed[x] == loc[i][0]:
            valid=1
            info = [fname, "", loc[i][1], name]
            f = open('/home/seth/.navi/navify/info.pkl', 'wb')
            pickle.dump(info, f)
            f.close()
            currentTrack=(str(loc[i][1]))
            for c in range(0,len(likes)):
                if (loc[i][1] == likes[c]):
                    window["-LIKE-"].update(image_filename="/home/seth/.navi/navify/icons/like.png")
                    break          
            break
    if valid == 0:
        currentTrack = "none"
        info = [fname, "", "", name]
        f = open('/home/seth/.navi/navify/info.pkl', 'wb')
        pickle.dump(info, f)
        f.close()

def updateLocal(select):
    global inFolder

    newList=["..."]    
    if select != "All":
        tempList=next(walk("/home/seth/.navi/navify/playCache/" + select + "/"), (None, None, []))[2]
        for i in range(0,len(tempList)):
            newList.append(subprocess.Popen(["cat", "/home/seth/.navi/navify/playCache/" + select + "/" + tempList[i]], stdout=subprocess.PIPE, text=True).communicate()[0])
        for x in range(0,len(tempList)+1):
            if '\n' in newList[x]:
                newList[x]=newList[x][0:len(newList[x])-1]
        window["-LOCAL-"].update(values=newList)
        inFolder=True
    else:
        newList=["..."]
        for i in range(0,len(localList)):
            newList.append(localList[i])
        window["-LOCAL-"].update(values=newList)
        inFolder=True

def genList(): 
    global spotID
    global spotList
    global combinedList
    global ID
    global listed
    global localList
    global localID
    global tempID
    global loc
    global likes 
    global folders   
    global inFolder
    global locID

    loc=[]       
    ID=[]
    locID=[]
    sortID=[]
    sortListed=[]
    
    inFolder=False

    # ALL METHOD
    # Lists only tracks in the playCache folder
    folders=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[1]
    ID=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[2]
    locID=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[2]
    for i in range(0,len(folders)):
        tempID=(next(walk("/home/seth/.navi/navify/playCache/" + str(folders[i])), (None, None, []))[2])
        for x in range(0,len(tempID)):
            locID.append("playCache/" + str(folders[i]) + "/" + tempID[x])            
            ID.append("https://www.youtube.com/watch?v=" + tempID[x])            
    listed=[]

    for i in range(0,len(locID)):
        listed.append(subprocess.Popen(["cat", "/home/seth/.navi/navify/" + locID[i]], stdout=subprocess.PIPE, text=True).communicate()[0])
            
    #listed[len(listed)-1]=listed[len(listed)-1][0:len(listed[len(listed)-1])-1]        
    tempID=[]
    sortID=[]
    sortListed=[]


    # Lists tracks in the Cache folder
    tempID=next(walk("/home/seth/.navi/navify/cache/"), (None, None, []))[2]
    for i in range(0,len(tempID)):
            currentFile = subprocess.Popen(["cat", "/home/seth/.navi/navify/cache/" + tempID[i]], stdout=subprocess.PIPE, text=True).communicate()[0]
            if ";" in currentFile:
                length=int(currentFile[len(currentFile)-3:])
                sortID.append(currentFile[0:length])
                sortListed.append((currentFile[length+1:len(currentFile)-3]))
                loc.append([(currentFile[length+1:len(currentFile)-3]), tempID[i]])

    localID=ID
    localList=listed    
    oldID=ID
    oldListed=listed
    spotID=[]
    spotList=[]
    combinedList=[]
    ID=[]
    listed=[]

    folders.append("All")    
    folders.sort()

    for i in range(0,len(sortID)):
        combinedList.append([sortListed[i],sortID[i]])    
    combinedList.sort()
    cacheI=len(combinedList)-1   
    for i in range(0, len(sortID)):
        ID.append(combinedList[i][1])
        listed.append(combinedList[i][0])   
    spotID=ID
    spotList=listed
    x=0
    for i in range(0,len(oldID)):
        x=x+1
        ID.append(oldID[i])
        listed.append(oldListed[i])   
    spotList=spotList[0:len(spotList)-x]      
    r=len(localList)
    #print(spotList)
    for i in range(0,r):
        if "\n" in localList[i]:
            localList[i]=localList[i][0:len(localList[i])-1]
    for i in range(0,len(listed)):
        if "\n" in listed[i]:
            listed[i]=listed[i][0:len(listed[i])-1]

    if exists("/home/seth/.navi/navify/icons/likes.pkl"):
        f = open('/home/seth/.navi/navify/icons/likes.pkl', 'rb')
        likes = pickle.load(f)
        f.close()
        #print(likes)



genList()


# Main Window layout

# Song List
SongList = [
    [
    sg.Button(image_filename="/home/seth/.navi/navify/icons/search.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-SEARCH-"),
    sg.Text("Songs", justification="center", background_color="#ccccdc",font=defaultFont,  expand_x=True),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/edit.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-EDIT-")
],
    [sg.Listbox(values=spotList, background_color="#99aabf", font=defaultFont, text_color="#ffffff", no_scrollbar=True, size=(25,1), enable_events=True,  expand_y=True, expand_x=True, key="-SONGS-")], 
    [sg.Input(font=defaultFont, text_color="#ffffff", background_color="#aabbcf", enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, visible=True, key="-INSEARCH-")]
]

# Local Files
Local = [
    [
    sg.Button(image_filename="/home/seth/.navi/navify/icons/add.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-ADD-"),
    sg.Text("Local", justification="center", background_color="#ccccdc", font=defaultFont, expand_x=True),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/playlist.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-PLAYLIST-")

    ],
    [sg.Listbox(values=folders, auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", no_scrollbar=True, size=(1,1), enable_events=True, expand_y=True, expand_x=True, key="-LOCAL-")] 
]

Queue = [
    [
    sg.Button(image_filename="/home/seth/.navi/navify/icons/navi.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-NAVIFY-"),
    sg.Text("Queue", justification="center", background_color="#ccccdc", font=defaultFont, expand_x=True),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/settings.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-SETTINGS-")
    ],
    [sg.Listbox(values=[], auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", no_scrollbar=True, size=(1,1), enable_events=True, key="-QUEUE-", expand_y=True, expand_x=True)] 
]

# Play Bar
BottomBar = [
    [
    sg.Text(text="Now Playing: Nothing", size=(1,1), font=smallFont, expand_x=True, background_color="#99aabf", key="-PLAYING-"),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/nrepeat.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-REPEAT-"),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/blacklist.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-BLACKLIST-"),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/prev.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/play.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-PLAY-"),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/next.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-SKIP-"),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/elike.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-LIKE-"),
    sg.Button(image_filename="/home/seth/.navi/navify/icons/nshuffle.png", enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-SHUFFLE-"),
    sg.Text("0:00/0:00", justification="right", font=smallFont, size=(1,1), expand_x=True, background_color="#99aabf", key="-TIME-")    
    ]
]

#[sg.ProgressBar(max_value=1, bar_color=("#22dddd","#67778f"), expand_x=True, key="-BAR-")],
layout = [
    [
    sg.Column(Local, background_color="#ccccdc", expand_y=True, expand_x=True),
    sg.VSeparator(color=None),
    sg.Column(SongList, background_color="#ccccdc",expand_y=True, expand_x=True),
    sg.VSeparator(color=None),
    sg.Column(Queue, background_color="#ccccdc",expand_y=True, expand_x=True)
    ],
    [sg.Slider(range=(0,1), default_value=0, enable_events=True, background_color="#99aabf", trough_color="#99aabf", orientation='h', disable_number_display=True, border_width = 0, expand_x=True, key="-BAR-")],    
    [sg.Column(BottomBar, background_color="#ccccdc", justification="center", expand_x=True)]
]


# Create the window
window = sg.Window("Navify", layout, keep_on_top=False, force_toplevel=False, no_titlebar=False, resizable=True, auto_size_text=True, use_default_focus=True, alpha_channel=0.8, background_color="#ccccdc", border_depth=None)


# Create an event loop

print(loc)
print(localList)

def player():
    queue=[] # Queued songs
    isPlaying=0 # Is there a song playing now
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

    global inFolder

    while True:
        if repeat == 1:
            print(prequeue)
        event, values = window.read(timeout=100)

        # Progress bar stuff
        if isPlaying == 1:
            try:
                duration = subprocess.Popen(["/home/seth/.navi/navify/GUI/getTime.sh", "1"], stdout=subprocess.PIPE, text=True)
                current = subprocess.Popen(["/home/seth/.navi/navify/GUI/getTime.sh", "2"], stdout=subprocess.PIPE, text=True)
                duration=duration.communicate()[0][8:]
                current=current.communicate()[0][8:]
                
                for i in range(0, len(duration)):
                    if duration[i:i+1] == ",":
                        duration=float(duration[0:i])
                        break
                for i in range(0, len(current)):
                    if current[i:i+1] == ",":
                        current=float(current[0:i])
                        break
                #print(str(current) + " " + str(duration))
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
        if event == "-BAR-" and isPlaying==1:
            time=200
            subprocess.Popen(["/home/seth/.navi/navify/GUI/setTime.sh", str(values["-BAR-"]/100)])

        # Resets after the song is finished
        if isPlaying==1 and not exists("/home/seth/.navi/navify/GUI/isPlaying.txt"):
            p.join()
            window["-LIKE-"].update(image_filename="/home/seth/.navi/navify/icons/elike.png")
            isPlaying=0

        # Checks if a song is playing   
        if exists("/home/seth/.navi/navify/GUI/isPlaying.txt") and isPlaying == 0:
            isPlaying=1


        # END OF SONG WITH NO QUEUE EVENT    
        if len(queue) == 0 and isPlaying == 0:          
            if repeat == 1:
                queue = list(prequeue)
            window["-PLAY-"].update(image_filename="/home/seth/.navi/navify/icons/play.png")
            window["-PLAYING-"].update("Now Playing: Nothing")
            window["-TIME-"].update("0:00/0:00")
            window["-BAR-"].update(0, range=(0,1))
            play=False


        # LOCAL SONG EVENT
        if event == "-LOCAL-": 
            # Opens Folders
            if edit == False and inFolder == False:
                updateLocal(values["-LOCAL-"][0])

            # Plays a song if the player is in a folder
            if edit == False and inFolder == True: 
               
                if values["-LOCAL-"][0] != "...":
                    print(listed)
                    print(values["-LOCAL-"][0])
                    for i in range(0, len(listed)):
                        if (str(listed[i]) == str(values["-LOCAL-"][0])):
                            queue.append(listed[i])
                            if repeat == 1:
                               prequeue.append(listed[i])
                            window["-QUEUE-"].update(values=queue)
                            break
                else:
                    window["-LOCAL-"].update(values=folders)
                    inFolder=False

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
                # Checks if the song needs to be added to queue
                for i in range(0, len(listed)):
                    if (str(listed[i]) == str(values["-SONGS-"][0])):
                        queue.append(listed[i])
                        if repeat == 1:
                            prequeue.append(listed[i])
                        window["-QUEUE-"].update(values=queue)
                        break      
            if edit == True:
                window["-INSEARCH-"].update(disabled=False)
                window["-INSEARCH-"].update(str(values["-SONGS-"][0]))
                for i in range(0, len(listed)):
                    if (str(listed[i]) == str(values["-SONGS-"][0])):
                        editI=i
                        break

        # QUEUE Event
        if event == "-QUEUE-":
            #print(values["-QUEUE-"][0])
            for i in range(0,len(queue)):
                if queue[i] == str(values["-QUEUE-"][0]):
                    del queue[i]
                    if (repeat == 1):
                        for x in range(0,len(prequeue)):
                            if (prequeue[x] == queue[i]):
                                del prequeue[x]
                    window["-QUEUE-"].update(values=queue)
                    break

        # Checks if there are songs queued
        if len(queue) > 0 and isPlaying == 0:
            valid=0
            a=0

            if shuffle == 1 and len(queue) > 1:
                a = random.randrange(0,len(queue))

            for i in range(0, len(listed)):
                if (str(listed[i]) == str(queue[a])):
                    valid=1
                    subprocess.call(["/home/seth/.navi/navify/GUI/createPlaying.sh"])                
                    window["-PLAYING-"].update("Now Playing: " + listed[i])
                    upDesktop(i)
                    p = Process(target=Play, args=(i,), daemon=True)
                    p.start()
                    playing=queue[a]
                    del queue[a]              
                    window["-QUEUE-"].update(values=queue)
                    play=True
                    window["-PLAY-"].update(image_filename="/home/seth/.navi/navify/icons/pause.png")                
                    break
            if valid==0:
                del queue[a]
                window["-QUEUE-"].update(values=queue)

        # Add song event
        if event == "-ADD-":
            popup.main()
            genList()
            window["-LOCAL-"].update(values=folders)
            
        # BUTTON EVENTS

        # Repeat
        if event == "-REPEAT-":
            if repeat == 0:
                window["-REPEAT-"].update(image_filename="/home/seth/.navi/navify/icons/repeat.png")
                repeat=1
                if isPlaying == 1:
                    prequeue.append(playing)
                    for i in range(0,len(queue)):
                        prequeue.append(queue[i])
            else:
                window["-REPEAT-"].update(image_filename="/home/seth/.navi/navify/icons/nrepeat.png")
                repeat=0
                prequeue=[]

        # Shuffle
        if event == "-SHUFFLE-":
            if shuffle == 0:
                window["-SHUFFLE-"].update(image_filename="/home/seth/.navi/navify/icons/shuffle.png")
                shuffle=1
            else:
                window["-SHUFFLE-"].update(image_filename="/home/seth/.navi/navify/icons/nshuffle.png")
                shuffle=0
        # BLACKLIST
        if event == "-BLACKLIST-" and isPlaying == 1 and currentTrack !="none":
            subprocess.Popen(["mv", "/home/seth/.navi/navify/cache/" + currentTrack, "/home/seth/.navi/navify/blacklist/" ])
            event="-SKIP-"
            genList()
            window["-SONGS-"].update(values=spotList)

        # Like
        if event == "-LIKE-" and isPlaying == 1 and currentTrack != "none":
            if exists("/home/seth/.navi/navify/icons/likes.pkl"):
                f = open('/home/seth/.navi/navify/icons/likes.pkl', 'wb')
                liked=1            
                #print(currentTrack)
                for i in (range(0,len(likes))):
                    if currentTrack == likes[i]:
                        liked=0
                        window["-LIKE-"].update(image_filename="/home/seth/.navi/navify/icons/elike.png")
                        navify.unlike(currentTrack)
                        del likes[i]
                        break
                if liked == 1:  
                    likes.append(current)
                    navify.like(currentTrack)
                    window["-LIKE-"].update(image_filename="/home/seth/.navi/navify/icons/like.png")            
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
                #print(len(spotList))
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
                                #print(spotSID)
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
                        for i in range(0, len(locID)):                
                            if link in locID[i]:
                                if exists("/home/seth/.navi/navify/" + locID[i]):
                                    f=open("/home/seth/.navi/navify/" + locID[i], 'w')               
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
                                    inFolder=False
                                    break

        # PLAYLIST BUTTON EVENT
        if event == "-PLAYLIST-":
            temp=[]
            temp=playlist.main(spotList, localList)
            for i in range(0,len(temp)):
                queue.append(temp[i])
            window["-QUEUE-"].update(values=queue)

        # Search Box
        if event == "-INSEARCH-":
            #print(values["-INSEARCH-"])
            if edit == False:
                newList=[]
                for i in range(0, len(spotList)):
                    if values["-INSEARCH-"].lower() in spotList[i].lower():
                        newList.append(spotList[i])
                window["-SONGS-"].update(values=newList)
            if edit == True:
                editName=str(values["-INSEARCH-"])

        # NAVIFY EVENT
        if event == "-NAVIFY-": 
            tempList = navify.genRec()
            genList()
            print(tempList)
            window["-SONGS-"].update(values=spotList)
            window["-PLAY-"].update(image_filename="/home/seth/.navi/navify/icons/pause.png")
            for i in range(0,len(tempList)):
                for x in range(0,len(ID)):
                    if tempList[i] == ID[x]:                
                        queue.append(listed[x])
                        if (repeat == 1):
                            prequeue.append(listed[x])
                        break
            window["-QUEUE-"].update(values=queue)

        # SETTINGS        
        if event == "-SETTINGS-":
            settings.main()

        # PLAYALL
        if event == "-LAYALL-":
            for i in range(0,len(listed)):
                queue.append(listed[i])

        # Skip/Next
        if event == "-SKIP-" and isPlaying == 1:
            os.remove("/home/seth/.navi/navify/GUI/isPlaying.txt")
            process = subprocess.Popen(["/home/seth/.navi/navify/scripts/display/killmpv.sh"], stdout=subprocess.PIPE, text=True)
            process=process.communicate()[0][4:]
            window["-PLAY-"].update(image_filename="/home/seth/.navi/navify/icons/pause.png")
            play=True
            for i in range(0,len(process)):
                if not " " in process[i:i+1]:
                    process=process[i:]
                    break
            for i in range(0, len(process)):
                if " " in process[i:i+1]:
                    process=process[0:i]
                    break
            subprocess.run(["kill", process])        
            #print(process)

        # PLAY/PAUSE
        if event == "-PLAY-":    
            if play == True:
                subprocess.run(["/home/seth/.navi/navify/scripts/display/pause.sh", "1"])
                play = False
                window["-PLAY-"].update(image_filename="/home/seth/.navi/navify/icons/play.png")   
            else:
                subprocess.run(["/home/seth/.navi/navify/scripts/display/pause.sh", "2"])
                play = True
                window["-PLAY-"].update(image_filename="/home/seth/.navi/navify/icons/pause.png")   

        if event == sg.WIN_CLOSED:
            break
        
        if time != 0:
            time=time-100
player()
window.close()

process = subprocess.Popen(["/home/seth/.navi/navify/scripts/display/killmpv.sh"], stdout=subprocess.PIPE, text=True)
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
print(process)





