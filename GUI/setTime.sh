#!/bin/bash
echo '{ "command": ["set_property", "playback-time", '$1'] }' | socat - /tmp/mpvsocket > /dev/null

