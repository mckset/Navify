# Navify
A music streaming software for Linux that uses Spotify's recommendations and streams it from Youtube. Streamed songs are then cached on the users PC for future access. Keep in mind, when a new song is added, Navify uses the **First** video that shows up on youtube when you search for the song and the artist. You may receive videos unrelated to the songs or of bad quality if the song is obscure.

Requirements
------------
- MPV
- Youtube-dl or an equivelant
- Spotipy
- Spotify developer app (https://developer.spotify.com/documentation/web-api/quick-start/#:~:text=To%20do%20that%2C%20simply%20sign%20up%20at%20www.spotify.com.,complete%20your%20account%20set%20up.%20Register%20Your%20Application)

Running
-------
    python navify.py

Questions
-----
**Why does this exists?**
One day I thought it would be great to integrate a Spotify player in my desktops taskbar. I went so far as to make the whole player and get the program to fetch songs when I realized that Spotify wanted me to buy a premium account to stream songs directly to my desktop. After some rough work arounds, I decided that since I can already pull the recommended songs, I should be able to play them through Youtube, and sure enough it worked.

**Why not have an option to stream from Spotify?**
Though the player was supposed to only stream from Spotify, I'm too lazy to purchase a premimum membership and try. Maybe one day I will add the option. 

**Can I download songs?**
No. Navify is not setup to download songs from anywhere. Though it can play songs that you download, there is no option to download songs and there are no plans to add it either. 

Potential Updates
-----------------
- Support to stream from Spotify
- Ablity to edit playlists
- Windows support
- Ability to edit the song and their url
- Local search
- Ability to add new paths to the local songs section
- More settings
- Ability to edit local songs
- Support to cache songs from Spotify
