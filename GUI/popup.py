import subprocess
from os.path import exists
from urllib import request, parse
import requests
import os
import sys
import io
from os import walk

from PIL import Image

from os.path import exists


import PySimpleGUI as sg

defaultFont="Inter 40"
smallFont="Inter 32"

def main():
    header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
    results=[]

    temp=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[1]
    temp.sort()
    folders=["---create new---"]

    for i in range(0,len(temp)):
        folders.append(temp[i])

    # Main Window layout

    # Song List
    Search = [
        [
        sg.Text("Search For Song: ", font=defaultFont,justification="center", background_color="#ccccdc", expand_x=True),
        sg.Input(font=defaultFont, text_color="#ffffff", background_color="#aabbcf", enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True,  visible=True, key="-YOUTUBESEARCH-"),
        sg.Button("Search", font=defaultFont,enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-ENTER-")
        ]
    ]
    Results = [
    [
        sg.Text("Results:", font=defaultFont,justification="center", background_color="#ccccdc", expand_x=True)
    ],
    [
        sg.Listbox(values=results, auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", size=(25,1), no_scrollbar=True,disabled=True, enable_events=True,  expand_y=True, expand_x=True, key="-RESULTS-")]
    ]

    Name = [
    [

        sg.Text("Name: ", font=defaultFont,justification="center", background_color="#ccccdc", expand_x=True),
        sg.Input(font=defaultFont, text_color="#ffffff", background_color="#aabbcf", enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=True, visible=True, key="-NAME-"),
        sg.Button("Submit", font=defaultFont,enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-SUBMIT-", disabled=True)
    ]
    ]

    layout = [

    [
        sg.Column(Search, background_color="#ccccdc", expand_y=True, expand_x=True)
    ],
    [
        sg.Column(Results, background_color="#ccccdc", expand_y=True, expand_x=True)
    ],
    [
        sg.Column(Name, background_color="#ccccdc", expand_y=True, expand_x=True)
    ],
    [
        sg.Listbox(values=folders, auto_size_text=True, background_color="#99aabf", font=defaultFont, text_color="#ffffff", size=(25,1), no_scrollbar=True,disabled=False, enable_events=True,  expand_y=True, expand_x=True, key="-CREATE-"),
        sg.VSeparator(color=None),
        sg.Button("Cancel", font=defaultFont,enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-CANCEL-"),
        sg.Button("Open", font=defaultFont,enable_events=True, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-OPEN-", disabled=True),
        sg.VSeparator(color=None),
        sg.Image(source=None, size=(256,192), key="-IMAGE-")
    ]
    ]

    layout2 = [

    ]

    window = sg.Window("Add Song", layout, background_color="#ccccdc", border_depth=None)
    search=""
    video=[]
    img=[]
    links=[]
    selected=""
    text=[]
    sfolder=""
    content=""
    name=""
    while True:
        event, values = window.read()
        
        if event == "-YOUTUBESEARCH-": 
            search=values["-YOUTUBESEARCH-"]   
       
        if event == "-ENTER-":
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
            #print(url)
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

                        #print(vid)
                        text.append("Unknown")
                        for a in range(i,i+1000):
                            if "\"title\":" in data[a:a+8]:
                                #print("title")
                                for y in range(a,i+1000):
                                    if "\"}]" in data[y:y+3]:
                                        #print("end")
                                        #print(data[a+26:y]) 
                                        text[len(text)-1] = data[a+26:y]
                                        break
                                break  

            #print(video)
            window["-RESULTS-"].update(disabled=False)
            window["-RESULTS-"].update(values=links)
            window["-NAME-"].update(search)
            window["-NAME-"].update(disabled=False)
            name=search

        if event == "-NAME-":
            content=values["-NAME-"]

        if event == "-RESULTS-":
            window["-OPEN-"].update(disabled=False)
            window["-SUBMIT-"].update(disabled=False)
            selected=values["-RESULTS-"][0]
            for i in range(0,len(links)):
                if links[i] == values["-RESULTS-"][0]:
                    #print(img[i])
                    response = requests.get(img[i])
                    
                    pil_image = Image.open(io.BytesIO(response.content))
                    png_bio = io.BytesIO()
                    #pil_image.resize((2,2), resample=None)
                    pil_image.save(png_bio, format="PNG")
                    png_data = png_bio.getvalue()


                    response.raw.decode_content = True
                    window["-IMAGE-"].update(data=png_data, size=(256,192), subsample=2)        
                    window["-NAME-"].update(text[i])
                    name=video[i]
                    content=text[i]

        if event == "-CREATE-":
            if values["-CREATE-"][0] != "---create new---":
                sfolder=values["-CREATE-"][0]
            else:
                sfolder=""
                fname=""
                layout2 = [
                [
                    sg.Text("Create A New Folder ", font=defaultFont,justification="center", background_color="#ccccdc", expand_x=True)
                ],
                [
                    sg.Text("Name: ", justification="center",font=defaultFont, background_color="#ccccdc", expand_x=True),
                    sg.Input(font=defaultFont, text_color="#ffffff", background_color="#aabbcf", enable_events=True, size=(25,1), focus=True, border_width=0, expand_x=True, disabled=False, visible=True, key="-NAME2-"),
                    sg.Button("Create", enable_events=True,font=defaultFont, button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-CREATE2-", disabled=True),
                    sg.Button("Cancel", enable_events=True, font=defaultFont,button_color="#99aabf", mouseover_colors=("","#67778f"), border_width=0, key="-CANCEL2-", disabled=False)
                ]
                ]
                window2 = sg.Window("New Folder", layout2, background_color="#ccccdc", border_depth=None)
                while True:
                    event2, values2 = window2.read()

                    if event2 == "-CREATE2-" and len(fname) > 0:
                        subprocess.run(["mkdir", "/home/seth/.navi/navify/playCache/" + fname])
                        window2.close()
                        break
                        
                    if event2 == "-NAME2-":
                        fname=values2["-NAME2-"]
                        if len(fname) > 0:
                            window2["-CREATE2-"].update(disabled=False)
                        else:
                            window2["-CREATE2-"].update(disabled=True)
                        
                    if event2 == "-CANCEL2-":
                        window2.close()
                        break
                temp=next(walk("/home/seth/.navi/navify/playCache/"), (None, None, []))[1]
                folders=["---create new---"]
                temp.sort()
                for i in range(0,len(temp)):
                    folders.append(temp[i])
                window["-CREATE-"].update(values=folders)
            
                

        if event == "-OPEN-":
            subprocess.run(["gio", "open", selected])

        if len(name) > 0 and len(sfolder) > 0:
            window["-SUBMIT-"].update(disabled=False)
        else:
            window["-SUBMIT-"].update(disabled=True)

        if event == "-SUBMIT-":
            if not exists("/home/seth/.navi/navify/playCache/" + sfolder + "/" + name):
                subprocess.run(["touch", "/home/seth/.navi/navify/playCache/" + sfolder + "/" + name])
            f = open("/home/seth/.navi/navify/playCache/" + sfolder + "/" + name, 'w')
            f.write(content)
            f.close()
            window.close()
            break

        if event == "-CANCEL-":    
            window.close()
            break
