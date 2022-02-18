#!/bin/bash
if [ "$1" == "1" ]; then
    echo '{"command": ["set_property", "pause", true]}' | socat - /tmp/mpvsocket > /dev/null
else
    echo '{"command": ["set_property", "pause", false]}' | socat - /tmp/mpvsocket > /dev/null
fi


