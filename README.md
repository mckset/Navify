# Navify
A music streaming software for Linux that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure. See the source branch for the source code.

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
- Supports mutliple languages

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

Key Bindings
------------
- Space: pause/play
- Up: volume up
- Down: volume down
- Left: seek -5 seconds 
- Right: seek 5 seconds
- '<' or ',': previous
- '>' or '.': skip

Notes
-----
- Navify creates and looks for files from the directory it is accessed from. If the program is accessed from a different folder than where the program is located, it will create and expect files like the 'icons' folder to be in that location.
- If you plan to play songs with titles in different languages, you might need to change

Updates
-------
- The player now pre-caches liked songs
- Text for the playing song now scrolls if there isn't enough room on the screen (adjustable in the theme window)
- Reset the way the player handles play events (The other method broke on slower machines for some reason)
- Removed check for another player running (It cause more problems than solved)
- Added more keys as shortcuts

Potential Updates
-----------------
- Support to stream from Spotify
- Windows support (maybe some day)
- Local search
- Getting Spotify's discover weekly playlist

Known Issues
------------
- The XFCE desktop seems to have an issue with running the player if there isn't a font that supports the language
- Songs with longer names resize certain windows past the display size
- The main window freezes when a subwindow is opened, but continues when the window is closed (Prevents the player from going to the next song in the queue when open)
