# Navify
A music streaming software for Linux (See Windows branch for a Windows version) that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure (Use the edit button to change the URL if this happens).

Requirements
------------
- mpv
- youtube-dl
- python3
- socat
- Spotify developer app - must be setup by the user (https://developer.spotify.com/documentation/general/guides/authorization/app-settings/)

Additional Requirements (If you want to run the source code)
------------------------------------------------------------
- Spotipy
- Pillow
- PySimpleGUI

Installation and Running
------------------------
```
git clone --branch *Arch/Ubuntu* https://github.com/mckset/Navify.git
cd Navify
chmod +x navify
./navify
```

The Actual Player
-----------------
![alt text](https://github.com/mckset/Navify/blob/main/Navify.png)

Features
--------
- Grab a list of recommended songs from Spotify based off of your choice of liked songs (up to 5 can be picked to filter recommendations)
- Play songs from either YouTube or your local music folder
- Caches songs from Spotify to save time searching for them again (~175 bytes per song)
- Ability to edit cached songs names and where the player looks to play the song (Can be a YouTube link or a path to the song on your PC)
- Ability to add songs from YouTube to a local cache
- A list of local songs from any folder of your choice to play (~/Music is the default)
- Settings to change the color scheme of the player
- Ability to create and edit a playlist of both local and cached music, inluding music files
- Support for mutliple languages
- Play YouTube livestreams 
- Manually cache songs via Spotify or YouTube (YouTube cache is stored in the Local Cache folder)
- Sort by name, artist, recommended, duration, year, and play count
- Fine tune the volume of individual songs

Usage
-----
- The '+' button adds a song
- The folder button adds a playlist
- the magnifying glass searches for a cached song
- The pencil edits a song (both cached and local)
- The 'N'/Navify button searches for recommended songs
- Right click the 'N'/Navify button to list playlists from Spotify
- The  '...' opens the setting
- Right click the cached songs list to bring up a menu to sort by
- If you want to run Navify only in offline mode, append "--offline" when starting it from the terminal

Key Bindings
------------
- Space: pause/play
- Up: volume up
- Down: volume down
- Left: seek -5 seconds 
- Right: seek +5 seconds
- '<' or ',': previous
- '>' or '.': skip
- '/' or '?': Move the last queued song to the top of the list (Basically play next)
- ESCAPE: Move to the top of the song list and reset edit and search functions

Notes
-----
- *FOR UPDATE 3.0 ONLY* Because more information is being stored on songs than before, all previously cached and Spotify songs will need to be recached to work properly with the player
- Navify does *NOT* download songs from YouTube or Spotify. It only caches a unique ID that it can use to find the YouTube URL or local path to the song
- Navify creates and looks for files from the directory it is accessed from. If the program is accessed from a different folder than where the program is located, it will create and expect files like the 'icons' folder to be in that location.
- If you plan on playing songs with titles in different languages, you might need a font that supports it
- The player checks for songs in your selected local folder and all folders in it. It is not recommended to select a folder with a large amount of files that are not music files as it will slow the player down
- The player only lists songs ending in .mp3, .wav, .ogg, and .mid. Other song formats are technically supported but the player will not be able to find them. 
- Any streaming options requires an internet connection. Slower internet speeds will most likely result in choppy or low quality sound
- Songs that are greater than 40 minutes long are considered to long for the player to cache via automatic caching methods (to prevent the player from pulling full albums). Longer songs can still be manually cached or the url can be edited to match that of the proper song.
- If a local song is renamed and is part of a playlist, the player will not be able to find the local song and will remove it from the playlist. This does not affect cached and Spotify songs
- Updates are going to slow down for a while unless something major needs to be fixed
- The windows branch is basically dead at this point. I have no reason to continue developing it, escpecially because of how far behind it is

Updates
-------
- Added an offline mode (Note: songs cached from Spotify are not playable in this mode even if they link to a local song)
- Added sort options (Right click the songs list)
- Added indicator to show how many songs are being cached during the Navify event or when getting a playlist
- Added check for livestream content and changed the progress bars behavior match it
- Added a check that hids duplicate Spotify entries (Usually happens when a song changes its ID)
- Added key binding to move the last song in the queue to the top to act as a play next button
- Added key binding to quickly exit the search and edit functions
- Added delete button to the edit window for all song types
- Added a counter to songs to keep track of how many times they were played (counts at the 50 second mark or when played if the song is shorter)
- Added options in the edit window for changing the start and end times of a song (Spotify and cache only)
- Added song information to be displayed on the edit window for Spotify songs
- Added volume slider in the edit window to control the volume of the selected song (Spotify and cache only)
- Added display for album/thumbnail art when editing a song
- Changed the layout for when the player runs in offline mode
- Changed how the playlist function locates songs to be able to tell when a cached or Spotify song has been renamed
- Changed how the player stores information on cached songs to help prevent songs with the same name from causing problems
- Changed how the player handles queuing a song to speed up the process
- Changed the way repeating songs works to match the new method of locating songs
- Fixed cached songs with the same name as a local song being sent to the editor as the local song
- Fixed playlists crashing the player when a song is no longer valid
- Fixed search results being reset after closing a subwindow even though text remained in the search box
- Fixed settings window being slow to open
- Fixed player crashing when trying to edit the "--create new---" option in the playlist menu
- Fixed bug where local songs with a '/' would cause the player to be unable to locate them
- Fixed (probably) the problem where the player grabs full albums instead of a song
- Fixed progress bar being stuck on livestream mode
- Fixed progress bar not jumping to the right times when dragged
- Fixed local and cached songs playing Spotify songs if they have the exact same name
- Fixed the previous button getting stuck on one song

Potential Updates
-----------------
- Support to stream from Spotify
- Settings to change keyboard shortcut

Troubleshooting
---------------
- The Spotify Values window keeps opening:
	
	Make sure your Spotify client id, secret id, and uri are correct. If they are, check your internet connection

- The player says it was unable to add a song:
	
	You can check for the song in the cache directory and attempt to fix it or you can just delete the song. It's most likely the player was stopped in the middle of the caching process and never finished writing the file or the file could have been edited and is no longer compatible with the player

- The Caching Liked Songs window got stuck on a song:
	
	You can either wait until it finishes finding the song or you close it and it will recache that song

- The player won't load my playlist:
	
	Check to make sure there aren't any greyed out songs in your playlist and it is under 100 songs. Spotify doesn't like those two things for some reason

- The player crashed, what do I do:
	
	You can restart Navify and it should sync back up with any song that is currently playing, If you want to report a bug, please run the music player from a terminal as it will output the error that the player gives, then open an issue on the GitHub page

Known Issues
------------ 
- Sometimes the player grabs random videos from YouTube instead of the song. It's very rare and not clear how this happens

