# Navify (For Windows)
A Windows port of Navify that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure. See the source branch for the source code.

Requirements
------------
- MPV
- Youtube-dl
- Python3
- Spotify developer app - must be setup by the user (https://developer.spotify.com/documentation/web-api/quick-start/#:~:text=To%20do%20that%2C%20simply%20sign%20up%20at%20www.spotify.com.,complete%20your%20account%20set%20up.%20Register%20Your%20Application)

Python Dependencies (Install with PIP)
--------------------------------------
- Pillow
- PySimpleGUI
- Spotipy

The Actual Player
-----------------
![alt text](https://github.com/mckset/Navify/blob/source/Navify.png)

Features
--------
- Grab a list of recommended songs from Spotify based off of your choice of liked songs (up to 5 can be picked to filter recommendations)
- Play songs from either YouTube or your local music folder
- Caches songs from Spotify to save time searching for them again (~75 bytes per song)
- Ability to edit cached songs names and where the player looks to play the song (YouTube or the path to the song on your PC)
- Ability to add songs from YouTube
- A list of local songs from any folder of your choice to play (~/Music is the default)
- Settings to change the color scheme and volume of the player
- Ability to create and edit a playlist of both local and cached music
- Setting to edit blacklisted songs
- Supports mutliple languages (see known bugs and notes)

Installation and Running
------------------------
Download the zip file and run

```
python -Xuft8 navify.py
```
from the command prompt. The -Xutf8 flag must be used if you plan to play songs with titles from a different language. Without it, the player crashes.

Usage
-----
- The '+' button adds a song
- The folder button adds a playlist
- the magnifying glass searches for a cached song
- The pencil edits a song (both cached and local)
- The 'N' button searches for recommended songs
- Right click the 'N' button to list playlists from Spotify
- The  '...' opens the setting

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
- The player checks for songs in your selected local folder and all folders in it. It is not recommended to select a folder with a large amount of files that are not music files as it will slow the player down.
- The player only lists songs ending in .mp3, .wav, .ogg, and .mid. Other song formats are technically supported but, the player will not be able to find them. 
- The Windows build is very new and might have multiple bugs that have not been discovered yet

Updates
-------
- Added functionally to get playlists from Spotify
- Fixed issue with blacklisting a song leaving a blank at the top of the player
- Fixed issue where setting a cached songs location to a local file screwed up the songs name
- Fixed other languages crashing the player (again)
- Added Windows support (See windows branch, might be a bit buggy)
- Fixed liked songs not being cached if there are more than 20 
- Fixed Navify event returning errors preventing it from being used
- Added input window for Spotify settings (Terminal no longer needed)
- Changed skipping songs to be a bit faster

Potential Updates
-----------------
- Support to stream from Spotify
- Local search
- Settings to change keyboard shortcut
- Condensing source code to be faster

Known Bugs
------------
- Songs with longer names resize certain windows past the display size

Known Issues
------------ 
- The main window freezes when a subwindow is opened, but continues when the window is closed (Prevents the player from going to the next song in the queue when open). It is unable to be fixed at the moment (perhaps a different GUI kit would be better)
- Sometimes that player will automatically grab a link to a full album instead of the song if the album has the same name
