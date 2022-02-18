import subprocess

process = subprocess.Popen(["/home/seth/.navi/navify/scripts/display/killmpv.sh"], stdout=subprocess.PIPE, text=True)
process=process.communicate()[0][4:]
for i in range(0,len(process)):
    if not " " in process[i:i+1]:
        process=process[i:]
        break
for i in range(0, len(process)):
    if " " in process[i:i+1]:
        process=process[0:i]
        break
subprocess.run(["kill", process])        
print(process)
