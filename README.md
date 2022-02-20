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
