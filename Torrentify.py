#Torrentifty V.2
#NeonPinkQuartz -- Aidan


import os
from torrentool.api import Torrent
from qbittorrent import Client
import urllib.request

#Location of the directory you want to make a torrent mirror of
location = ""

skippedTorrents = 0
newTorrents = 0
dntOrder = 0
seedingError = 0
missingFiles = 0

#File you want the torrents to be saved in (/desktop/)
dataSource = ""
#Above file with the save file name added (/desktop/torrents)
dataReturn = ""

try:
    #WebUI IP
    qb = Client('')
    #Username, Password
    qb.login('', '')
except:
    print("ERROR (Offline): You are trying to access a web UI that is offline or not working. Close the application, relaunch the wub UI, and try again")
    input()

print("Version")
print(qb.qbittorrent_version)
print("API Version")
print(qb.api_version)

input("Press enter to begin...")

def urlGather():
    urls = []
    #Reads a public list of the top 20 Trackers, add your own to the second append line seperated with commas
    for line in urllib.request.urlopen("https://ngosang.github.io/trackerslist/trackers_best.txt"):
        urls.append(line.decode('utf-8').replace("\n",""))
        urls.append("udp://tracker.openbittorrent.com:80")
    return urls

#Get all files

def gatherFiles():
    fileTempList = open("temp.txt","a")
    for r, d, f in os.walk(location):
        for item in f:
            fileTempList.write(os.path.join(r, item).replace("\\","/") + "\n")
    fileTempList.close()

def launchSeed(activeTorrent):
    torrentDownload = open(activeTorrent, 'rb')
    qb.download_from_file(torrentDownload, savepath=activeDownload)
    print(f"Seeding {activeTorrent}")


#Create torrents

urls = urlGather()
gatherFiles()

fileTempList = open("temp.txt","r")
fileErrorList = open("ErrorLog.txt", "r+")
cycles = 0
running = True

activeList = fileTempList.readlines()

while True:
    try:
        activeFile = activeList[cycles]
        activeFile = activeFile.replace("\n","")
        ##Debug
        #print(activeFile)
        #input()
        ##
    except:
        break
    if "." in activeFile:
    	fileName, fileExt = os.path.splitext(activeFile)
    	newEXT = fileExt.replace(".","(") + ")"
    	activeTorrent = activeFile.replace(dataSource,dataReturn).replace(fileExt, newEXT) + ".torrent"
    else:
        activeTorrent = activeFile.replace(dataSource,dataReturn) + ".torrent"
    tempList = activeFile.split("/")
    fileName = tempList[-1]
    ##Debug
    #print(activeTorrent)
    #input()
    ##
    if os.path.exists(activeTorrent):
        print("Skipping existing torrent...")
        skippedTorrents += 1
    elif fileName[0:3] == "DNT":
        dntOrder += 1
        cycles += 1
        print("ERROR (DNT Order)")
        continue
    elif fileName[0:2] == "._":
        cycles += 1
        print("ERROR (Unix file)")
        continue
    elif os.path.getsize(activeFile) == 0:
        os.remove(activeFile)
        missingFiles += 1
        continue
    else:
        activeDownload = activeFile.split("/")
        downloadLength = len(activeDownload)
        activeDownload = activeDownload[:downloadLength - 1]
        activeDownload = "/".join(activeDownload)
        activePath = activeDownload.replace(dataSource,dataReturn)
        try:
            ##Debug
            #print(activePath)
            #input()
            ##
            os.makedirs(activePath)
        except:
            print("Folder Exists, Skipping...")
        activeFile = os.path.normpath(activeFile)
        activeTorrent = os.path.normpath(activeTorrent)
        ##Debug
        #print(activeFile)
        #input()
        ##
        GlassTorrent = Torrent.create_from(activeFile)
        GlassTorrent.announce_urls = urls
        GlassTorrent.comment = "Torrent created by the GlassLibrary"
        ##Debug
        #print(activeTorrent)
        #input()
        ##
        GlassTorrent.to_file(activeTorrent)
        print(f"Made {activeTorrent}")
        newTorrents += 1
        try:
            launchSeed(activeTorrent)
        except:
            try:
                launchSeed(activeTorrent)
            except:
                print(f"ERROR (seeding) on {activeTorrent}")
                fileErrorList.write(activeTorrent)
                fileErrorList.write("\n")
                seedingError += 1
    cycles += 1

fileTempList.close()
fileErrorList.close()
os.remove("temp.txt")
print("\n\n------------------------------")
print(f"{skippedTorrents} Skipped; {newTorrents} Made")
print(f"{dntOrder} Torrents blocked; {seedingError} Failed to seed")
print(f"{missingFiles} Removed due to having 0 bytes")
input("Press enter to close...")
