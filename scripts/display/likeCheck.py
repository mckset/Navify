import pickle
import sys
from os.path import exists  

liked=[]

if exists("/home/seth/.navi/navify/icons/likes.pkl") and exists("/home/seth/.navi/navify/info.pkl"):
        f = open("/home/seth/.navi/navify/icons/likes.pkl", 'rb')
        liked = pickle.load(f)
        f.close()
        
        f = open("/home/seth/.navi/navify/info.pkl", 'rb')
        current = pickle.load(f)
        f.close()
        
        for i in range(0, len(liked)):
            if liked[i] == current[2]:
                print("/home/seth/.navi/navify/icons/like.png")          
                sys.exit()
print("/home/seth/.navi/navify/icons/elike.png")
