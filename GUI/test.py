from urllib import request, parse

header={'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Forefox/23.0'}
req=request.Request("https://youtube.com/results?search_query=delain", headers=header)
U = request.urlopen(req)
data = U.read().decode('utf-8')

print("searching...")
for i in range(0,len(data)):
    if "videoid" in data[i:i+7].lower() and not "videoids" in data[i:i+8].lower():
        vid=data[i+10:i+1000]
        print(vid)
        for x in range(10,1000):
            if "\"title\":" in vid[x:x+8]:
                for y in range(x,1000):
                    if "\"}]" in vid[y:y+3]:
                        print(vid[x+26:y])   
                print("yes")
        break
