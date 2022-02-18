#!/bin/bash
valid=0

if [ $valid" == "0" ]; then
  echo '{"command": ["set_property", "volume", '$1']}' | socat - /tmp/mpvsocket > /dev/null
fi
