# Navify
A music streaming software for Linux that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure.

Requirements
------------
- MPV
- Youtube-dl
- Python3
- Socat
- Spotify developer app - must be setup by the user (https://developer.spotify.com/documentation/web-api/quick-start/#:~:text=To%20do%20that%2C%20simply%20sign%20up%20at%20www.spotify.com.,complete%20your%20account%20set%20up.%20Register%20Your%20Application)

Features
--------
- Grab a list of recommended songs from Spotify based off of your choice of liked songs (up to 5 songs at a time)
- Play songs from either YouTube or your local music folder
- Caches songs from Spotify to save time searching for them again (~75 bytes per song)
- Ability to edit cached songs names and where the player looks to play the song (YouTube or the path to the song on your PC)
- Ability to add songs from YouTube
- A list of local songs in your 'Music' folder to play
- Settings to change the color scheme and volume of the player
- Ability to create and edit a playlist of both local and cached music
- Supports mutliple languages (I haven't tested them all)

Installation and Running
------------------------
```
git clone https://github.com/mckset/Navify.git
./navify
```

Usage
-----
- The '+' button adds a song
- The folder button adds a playlist
- the magnifying glass searches for a cached song
- The pencil edits a song (both cached and local)
- The 'N' button searches for recommended songs
- The  '...' opens the settings

Notes
-----
Navify creates and looks for files from the directory it is accessed from. If the program is accessed from a different folder than where the program is located, it will create and expect files like the 'icons' folder to be in that location. 

Potential Updates
-----------------
- Ability to change fonts and font sizes
- Ability to change the location for browsing local music files
- Support to stream from Spotify
- Windows support
- Local search
- More settings
- Pre-caching liked songs

Known Issues
------------
- Certain characters in the name of a song can crash the player when attempting to search it on YouTube
- Songs with 10 seconds at the end of the time is shown as being X:010 (Fixed but it was not commited)
- Songs with longer names resize certain windows past the display size
- Leaving the search field empty when searching for Spotify songs crash the player
- The main window freezes when a subwindow is opened, but continues when the window is closed
- If the theme is changed while the player is searching for recommended songs, the recommended button can be pressed again and will override the first search request
- Whenever the player crashes while a song is playing, the song continues to play until the end. (The song can be stopped by opening the player again, playing a song, and clicking the skip button a couple of times)
