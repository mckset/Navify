#!/bin/bash
echo '{"command": ["cycle", "pause"]}' | socat - /tmp/mpvsocket
state=$(cat '/home/seth/.navi/navify/icons/state.txt')
echo $state
if [ "$state" == "1" ]; then
    cp /home/seth/.navi/navify/icons/pause.png /home/seth/.navi/navify/icons/state.png 
    echo 2 > /home/seth/.navi/navify/icons/state.txt
fi
if [ "$state" == "2" ]; then
    cp /home/seth/.navi/navify/icons/play.png /home/seth/.navi/navify/icons/state.png 
    echo 1 > /home/seth/.navi/navify/icons/state.txt
fi
