# Navify
A music streaming software for Linux that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if they show up first. As a result, a method has been implimented to edit the tracks url if needed.

Installation
------------
Navify requires that you setup a spotify developer app and change the settings to match your account. 

About
-----
Navify is a music player written in Python that can be used either through the terminal or the graphical interface. When ran in the terminal, the player requests a list of up to 50 recommended songs from Spotify and streams them directly from Youtube using youtube-dl and mpv. Streamed songs have their URL's cached so it can be accessed again if needed. The player picks the first song on Youtube when searching Spotify's results and caches that, though there is a method to edit the file if needed.  

Running
-------



Questions
-----
**Why does this exists?**
One day I thought it would be great to integrate a Spotify player in my desktops taskbar. I went so far as to make the whole player and get the program to fetch songs when I realized that Spotify wanted me to buy a premium account to stream songs directly to my desktop. After some rough work arounds, I decided that since I can already pull the recommended songs, I should be able to play them through Youtube, and sure enough it worked.

**Why not have an option to stream from Spotify?**
Though the player was supposed to only stream from Spotify, I'm too lazy to purchase a premimum membership and try. Maybe one day I will add the option. 

Potential Updates
-----------------
- Support to stream from Spotify
- Ablity to edit playlists
- Make the Navify button not freeze the player
- Windows support
- Ability to edit the song, their url, and their volume in one window
- Local search
- Ability to add new paths to the local songs section
- More settings

Known Issues
------------
- The [TRACKS] marker still shows up in folders with files even though they are not music files
