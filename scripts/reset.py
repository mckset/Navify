import os
import sys
from os.path import exists

if exists("/home/seth/.navi/navify/prev.txt"):
    os.remove("/home/seth/.navi/navify/prev.txt")
if exists("/home/seth/.navi/navify/like.pkl"):
    os.remove("/home/seth/.navi/navify/like.pkl")
os.remove("/home/seth/.navi/navify/pause.txt")
