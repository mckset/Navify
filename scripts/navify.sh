#!/bin/bash
#sleep .25
cd /home/seth/.navi/navify/scripts
valid=0

if [ "$1" == "-be" ] || [ "$1" == "-bedit" ]; then
	valid=1
	python eBlacklist.py
fi 

if [ "$1" == "-c" ] || [ "$1" == "--clean" ]; then
	valid=1
	python clearCache.py
fi


if [ "$1" == "-e" ] || [ "$1" == "--edit" ]; then
	valid=1
    	python edit.py
fi


if [ "$1" == "-l" ] || [ "$1" == "--lookup" ]; then
	valid=1
    	python lookup.py
fi

if [ "$1" == "-s" ] || [ "$1" == "--settings" ]; then
	valid=1
	sudo python3 setup.py
fi

if [ "$1" == "-p" ] || [ "$1" == "--play" ]; then
	valid=1
	echo "$2" > /home/seth/.navi/navify/playing.txt
	echo "pause" > /home/seth/.navi/navify/pause.txt
	python /home/seth/.navi/navify/scripts/display/killmpv.py
	python /home/seth/.navi/navify/scripts/play.py
	python /home/seth/.navi/navify/scripts/reset.py
fi

if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
	valid=1
	echo "Valid commands:"
	echo "	-be, --bedit		Edits the blacklist cache"
	echo "	-c, --clean		Removes cache that is also blacklisted"
	echo "	-e, --edit		Edits which songs are cached"
	echo "	-l, --lookup		Searches for a cached song"
	echo "	-h, --help		Displays this message"
	echo "	-o, --old		Runs the command line version" 
	echo "	-p, --play 		Plays a song/link"
	echo "	-pl, --playlist		Plays a playlist"
	echo "	-s, --settings		Opens the settings for the spotify player"
	echo "	-u, --update		Updates the liked cache"
	echo " "
fi

if [ "$1" == "-o" ] || [ "$1" == "--old" ]; then
	valid=1
	python ~/.navi/navify/navify.py
fi

if [ "$valid" == "0" ]; then
    alacritty -e python ~/.navi/navify/GUI/checkSpotify.py
	python ~/.navi/navify/GUI/player.py
fi



