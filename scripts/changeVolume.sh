#!/bin/bash
if [ "$1" == "1" ]; then
    echo '{"command": ["add", "volume", 5]}' | socat - /tmp/mpvsocket > /dev/null
else
    echo '{"command": ["add", "volume", -5]}' | socat - /tmp/mpvsocket > /dev/null
fi
