import pickle
import sys
from os.path import exists 

if not exists('/home/seth/.navi/navify/icons/start.txt'):
    f = open("/home/seth/.navi/navify/info.pkl", 'rb')
    current = pickle.load(f)
    f.close()

    f = open("/home/seth/.navi/navify/blacklist/" + str(current[2]) , "w")
    f.write(str(current[0]) + " - " + str(current[1]))
    f.close()
