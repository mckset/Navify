import pickle
from os.path import exists

text=" *** waiting ***"

    
if exists('/home/seth/.navi/navify/info.pkl'):     
    f = open('/home/seth/.navi/navify/info.pkl', 'rb')
    info = pickle.load(f)
    f.close()
    fText=str(info[3])
    if len(fText) > 16:
        text=fText[0:16]
        info[3]=fText[1:] + fText[0:1]
        
        f = open('/home/seth/.navi/navify/info.pkl', 'wb')
        pickle.dump(info, f)
        f.close()
    else:
        if len(fText) < 16:
            if len(fText) == 15:
                text = " " + fText
            else:
                for i in range(len(fText), 16):
                    fText=fText+" "
                text=fText
            info[3]=text
            f = open('/home/seth/.navi/navify/info.pkl', 'wb')
            pickle.dump(info, f)
            f.close()
        else:
            text=fText
print(text)

