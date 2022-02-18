#!/bin/bash
echo '{"command": ["set_property", "volume", '$1']}' | socat - /tmp/mpvsocket > /dev/null

