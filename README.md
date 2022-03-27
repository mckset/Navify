# Navify
A music streaming software for Linux that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure. See the source branch for the source code.

Requirements
------------
- MPV
- Youtube-dl
- Python3
- Socat
- Spotify developer app - must be setup by the user (https://developer.spotify.com/documentation/web-api/quick-start/#:~:text=To%20do%20that%2C%20simply%20sign%20up%20at%20www.spotify.com.,complete%20your%20account%20set%20up.%20Register%20Your%20Application)

The Actual Player
-----------------
![player](https://1drv.ms/u/s!AmUq8Rl7UdBdlUogk-cvFVLsLwBr)

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
- Right click the 'N' button to play the "Discover Weekly" playlist from Spotify
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
- If you plan on playing songs with titles in different languages, you might need install a font that supports it
- The player checks for songs in your selected local folder and all folders in it. It is not recommended to select a folder with a large amount of files that are not music files as it will slow the player down.
- The player only lists songs ending in .mp3, .wav, .ogg, and .mid. Other song formats are technically supported but, the player will not be able to find them. 
- Navify requires a terminal at least for the setup process. Without it, Spotify might need an input before the player starts and the program will hang.

Updates
-------
- Made the player more stable over all
- Set the player to try and play a song 3 times before skipping to the next in the queue (in case of a timeout)
- Added a settings to edit songs that are blacklisted
- Fixed problem that prevented the scrolling when searching through cached songs
- Stopped the player from taking keyboard inputs for listed songs
- Applied small optimization to retrieving cached song data
- Added option to get discover weekly playlist
- Fixed local songs not being able to be played after pushing the 'N' button. (If this happens anywhere else, clicking all on the local page should fix it)
- Condensed code in various places
- Added check to make sure the 'icons' folder is in the player directory

Potential Updates
-----------------
- Support to stream from Spotify
- Windows support (maybe some day)
- Local search
- Settings to change keyboard shortcut
- A way to bring Spotify playlists to the player
- Condensing source code to be faster

Known Bugs
------------
- The XFCE desktop seems to have an issue with running the player if there isn't a font that supports the language
- Songs with longer names resize certain windows past the display size
- When blacklisting a song, sometimes the player leaves a blank at the top of the listed songs and prevents all cached songs from playing. Restarting the player resolves the issue but it is unsure how it is caused at the moment.

Known Issues
------------ 
- The main window freezes when a subwindow is opened, but continues when the window is closed (Prevents the player from going to the next song in the queue when open)
- Sometimes that player will automatically grab a link to a full album instead of the song if the album has the same name
