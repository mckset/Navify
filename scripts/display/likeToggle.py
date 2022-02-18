import pickle
import sys
from os.path import exists    

pic="elike.png"
if not exists("/home/seth/.navi/navify/icons/start.txt"):
    likes=[]
    if exists("/home/seth/.navi/navify/icons/likes.pkl") and exists("/home/seth/.navi/navify/info.pkl"):
        f = open("/home/seth/.navi/navify/info.pkl", 'rb')
        current = pickle.load(f)
        f.close()
        
        f = open("/home/seth/.navi/navify/icons/likes.pkl", 'rb')
        likes = pickle.load(f)
        f.close()

        #print(current[2])
        #print(likes)

        liked=0
        for i in range(0, len(likes)):
            if likes[i] == current[2]:
                likes.remove(current[2])
                liked=1 
                break
        if liked==0:
            likes.append(current[2])
            pic='like.png'
        f = open('/home/seth/.navi/navify/like.pkl', 'wb')
        pickle.dump(liked, f)
        f.close()
        f = open('/home/seth/.navi/navify/icons/likes.pkl', 'wb')
        pickle.dump(likes, f)
        f.close()  
print("/home/seth/.navi/navify/icons/" + pic)
