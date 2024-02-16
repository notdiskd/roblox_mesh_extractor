import os
import re
import codecs
import requests
import subprocess

#----------------------- settings -----------------------

#set True if you want to export .mesh files
export_mesh = True
#set True if you want to export .ktx and .png files
export_ktx = True

#C:\Users\User\AppData\Local\Temp\Roblox\http
robloxhttp = os.getenv('LOCALAPPDATA')+"\Temp\Roblox\http"
#PVRTexTool CLI path
extract = f"{os.path.dirname(os.path.abspath(__file__))}\extract.exe"

#folder for .mesh
meshpath = f"{os.path.dirname(os.path.abspath(__file__))}\mesh"
#folder for .ktx
ktxpath = f"{os.path.dirname(os.path.abspath(__file__))}\ktx"
#folder for .png, converted from .ktx folder
pngpath = f"{os.path.dirname(os.path.abspath(__file__))}\png"

#--------------------------------------------------------

if export_mesh:
    if not os.path.exists(meshpath):
        os.makedirs(meshpath)
if export_ktx:
    if not os.path.exists(ktxpath):
        os.makedirs(ktxpath)
    if not os.path.exists(pngpath):
        os.makedirs(pngpath)


meshindex = 0
ktxindex = 0

for filename in os.listdir(robloxhttp):
    try:
        fileObj = codecs.open(os.path.join(robloxhttp, filename), "r", "latin-1" )
        text = fileObj.read()
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        URL = urls[0]
        r = requests.get(URL, timeout=1.5)
        if ((r.content).decode('latin-1')).startswith("version") and export_mesh:
            with open(f"{meshpath}\{meshindex}.mesh", 'wb') as f:
                f.write(r.content)     
            print(filename, f'{meshpath}\{meshindex}.mesh')
            meshindex+=1
        elif ((r.content).decode('latin-1')).startswith("«KTX 11»") and export_ktx:
            with open(f"{ktxpath}\{ktxindex}.ktx", 'wb') as f:
                f.write(r.content)     
            print(filename, f'{ktxpath}\{ktxindex}.ktx')
            png = subprocess.run([extract, "-i", f"{ktxpath}\{ktxindex}.ktx", "-d", f"{pngpath}\{ktxindex}.png", "-noout"], timeout=5, check=True)
            ktxindex+=1
    except Exception as a:
        print(a)