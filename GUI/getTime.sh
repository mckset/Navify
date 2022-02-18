#!/bin/bash
if [ "$1" == "1" ]; then
    echo '{ "command": ["get_property", "duration"] }' | socat - /tmp/mpvsocket
fi
if [ "$1" == "2" ]; then
    echo '{ "command": ["get_property", "playback-time"] }' | socat - /tmp/mpvsocket
fi
