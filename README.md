# Navify
A music streaming software for Linux (See Windows branch for a Windows version) that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure (Use the edit button to change the URL if this happens).

Requirements
------------
- mpv
- youtube-dl
- python3
- socat
- Spotify developer app - must be setup by the user (https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)

The Actual Player
-----------------
![alt text](https://github.com/mckset/Navify/blob/main/Navify.png)

Features
--------
- Grab a list of recommended songs from Spotify based off of your choice of liked songs (up to 5 can be picked to filter recommendations)
- Play songs from either YouTube or your local music folder
- Caches songs from Spotify to save time searching for them again (~75 bytes per song)
- Ability to edit cached songs names and where the player looks to play the song (Can be a YouTube link or a path to the song on your PC)
- Ability to add songs from YouTube to a local cache
- A list of local songs from any folder of your choice to play (~/Music is the default)
- Settings to change the color scheme of the player
- Ability to create and edit a playlist of both local and cached music, inluding music files
- Support for mutliple languages
- Play YouTube livestreams 
- Manually cache songs via Spotify or YouTube (YouTube cache is stored in the Local Cache folder)

Installation and Running
------------------------
```
git clone --branch *Arch/Ubuntu* https://github.com/mckset/Navify.git
cd Navify
./navify
```

Usage
-----
- The '+' button adds a song
- The folder button adds a playlist
- the magnifying glass searches for a cached song
- The pencil edits a song (both cached and local)
- The 'N'/Navify button searches for recommended songs
- Right click the 'N'/Navify button to list playlists from Spotify
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
- Navify does *NOT* download songs from YouTube or Spotify. It only caches a unique ID that it can use to find the YouTube URL or local path to the song
- Navify creates and looks for files from the directory it is accessed from. If the program is accessed from a different folder than where the program is located, it will create and expect files like the 'icons' folder to be in that location.
- If you plan on playing songs with titles in different languages, you need a font that supports it if you want to view the title
- The player checks for songs in your selected local folder and all folders in it. It is not recommended to select a folder with a large amount of files that are not music files as it will slow the player down.
- The player only lists songs ending in .mp3, .wav, .ogg, and .mid. Other song formats are technically supported but, the player will not be able to find them. 
- Any streaming options requires an internet connection. Slower internet speeds will most likely result in choppy songs

Updates
-------
- Added extra checks to attempt to prevent Spotify from crashing the player when it cannot establish a connection
- Added ability for the player to retrieve the title of a song after a crash (if it does crash)
- Added check to prevent playlists with greyed out songs from stopping the 'N'/Navify button from functioning
- Added limit to displayed title length when manually caching Spotify songs
- Added a check to prevent player events from causing a crash when triggered while a subwindow is opened
- Fixed generating the recommended song file listing random letters and numbers
- The player now disables the edit button after closing the edit window

Potential Updates
-----------------
- A proper icon
- Support to stream from Spotify
- Local search
- Settings to change keyboard shortcut
- Condensing source code to be faster

Troubleshooting
---------------
- The Spotify Values window keeps opening:
	Make sure your Spotify client id, secret id, and uri are correct. If they are, check your internet connection

- The Caching Liked Songs window got stuck on a song:
	You can either wait until it finishes finding the song or you close it and it will recache that song

- The 'N'/Navify button is stuck white/disabled:
	This is most likely happens when the player is first installed as you will have very little songs cached that will be recommended to you. It just takes some time to cache all 50 new songs.

- The player won't load my playlist:
	Check to make sure there aren't any greyed out songs in your playlist and it is under 100 songs. Spotify doesn't like those two things for some reason

- The player crashed, what do I do:
	You can restart Navify and it should sync back up with any song that is currently playing, If you want to report a bug, please run the music player from a terminal as it will output the error that the player gives, then open an issue on the GitHub page

Known Issues
------------ 
- The main window freezes when a subwindow is opened, but continues when the window is closed (Prevents the player from going to the next song in the queue when open). It is unable to be fixed at the moment (perhaps a different GUI kit would be better)
- Sometimes that player will automatically grab a link to a full album instead of the song if the album has the same name
