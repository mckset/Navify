#!/bin/bash
if [ "$1" == "C" ]; then
    echo '{ "command": ["get_property", "playback-time"] }' | socat - /tmp/mpvsocket
fi
if [ "$1" == "D" ]; then
    echo '{ "command": ["get_property", "duration"] }' | socat - /tmp/mpvsocket
fi
if [ "$1" == "T" ]; then
  echo '{ "command": ["set_property", "playback-time", '$2'] }' | socat - /tmp/mpvsocket > /dev/null
fi
if [ "$1" == "V" ]; then
  echo '{"command": ["set_property", "volume", '$2']}' | socat - /tmp/mpvsocket > /dev/null
fi

