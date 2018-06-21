#! /usr/bin/env python3
# ------ NASA's Astronomy Picture of the Day ------
# -------- Random wallpaper by Wiktor Flis --------
#
import os
import sys
import re
import __main__

import platform
import datetime
import random
import subprocess
import requests
from PIL import Image


def getValidDate():
    now = datetime.datetime.now()
    now = datetime.date(now.year, now.month, now.day)
    year = random.randint(2004, now.year)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    try:
        randomDate = datetime.date(year, month, day)
        if(randomDate > now):
            year = year - 1
            randomDate = datetime.date(year, month, day)
    except ValueError :
        day = day - 3
        randomDate = datetime.date(year, month, day)
    randomDate = datetime.date.strftime(randomDate, "%y%m%d")
    return randomDate

def getLink(date):
    return "https://apod.nasa.gov/apod/ap" + str(date) + ".html"

def getImgLinkFromURL(url):
    try:
        html_page = requests.get(url)
        html_page = html_page.text
        imglink = re.search(r"href=[\\'\"]?([^\'\" >]+)?(.jpg|.jpeg|.png)", html_page)
        if imglink:
            imglink = imglink.group(0)[6:]
            #url += imglink
            return "https://apod.nasa.gov/apod/" + imglink
        else:
            return -1  
    except:
        return -1  

def getimgLink():
    photofound = False
    while(not photofound):
        link1 = getLink(getValidDate())
        link2 = getImgLinkFromURL(link1)
        if (link2 != -1):
            photofound = True
    return link2

def downloadImage(url, destination_path):
    file_name = url.split('/')[-1]
    r = requests.get(url, stream=True)
    size = r.headers.get('Content-Length')
    size = int(size)
    filepath = destination_path + '/' + file_name

    with open(filepath, 'wb') as file:
        download = 0
        for chunk in r.iter_content(256):
            download += len(chunk)
            file.write(chunk)
            sys.stdout.write("Done: %d / %d bytes\r" % (download, size))
            sys.stdout.flush()

    return file_name

def createPreview(file):
    thumbnail_path = '../Previews/'
    size = (233, 133)
    outfile = file.split('/')[-1]
    outfile = os.path.join(thumbnail_path, outfile)
    outfile = outfile + ".mini.jpg"
    if file != outfile:
        try:
            imsize = os.path.getsize(file)
            print('Creating preview - Compressing image of size '+ str(imsize))
            im = Image.open(file)
            im.resize(size)
            im.save(outfile, "JPEG", optimize=True,quality=20)
            outsize = os.path.getsize(outfile)
            deltasize = ((imsize - outsize)/imsize)*100
            print("Output file size is {} , delta size (in %): {}".format(str(outsize), str(deltasize)))
        except IOError:
            print("cannot create thumbnail for", file)

def getPlatform():
    return platform.system()

def newWallpaper(path):
    while(True):
        try:
            imglink = getimgLink()
            break
        except Exception as e:
            print("Exception: {}".format(str(e)))

    print("Downloading wallpaper")
    wallpaper = downloadImage(imglink, path)
    print("Downloaded")
    return wallpaper

def getPath(platform):
    if platform == 'Windows':

        pass
    else:
        wallpaper_path = os.path.expanduser('~/Pictures/') +  'Astropaper/'
        if not os.path.exists(wallpaper_path):
            os.makedirs(wallpaper_path)        

    return wallpaper_path


def wallpaperSetup(current_system, wallpaper, wallpaper_path):
    if current_system == "Windows":
        try:
            import ctypes
            SPI_SETDESKTOPWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKTOPWALLPAPER, 0, wallpaper_path, 0)
            return 0
        except:
            print("Ctypes not installed")

    if current_system == "Darwin":
        try:
            wallpaper_path += wallpaper
            setWallpaperCommand = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + wallpaper_path + "\"'"
            #print(setWallpaperCommand)
            os.system(setWallpaperCommand)

            # subprocess
            #subprocess.call(setWallpaperCommand, shell=True)

            return 0
        except:
            print("Appscript may be not installed.")

    if current_system == "Linux":
        try:
            os.system("gsettings set org.gnome.desktop.background picture-uri file:///" + wallpaper_path)
            return 0
        except:
            print("gsettings not working")
    return -1

class Astropaper():
    def __init__(self):
        self.platform = getPlatform()
        self.path = getPath(self.platform)
    def setPath(self, path):
        self.path = path
    def getNewWallpaper(self):
        self.wallpaper = newWallpaper(self.path)
    def setup(self):
        wallpaperSetup(self.platform,self.wallpaper,self.path)

def main():
    astropaper = Astropaper()
    astropaper.getNewWallpaper()
    print("" + str(astropaper.wallpaper))
    astropaper.setup()
    

if __name__ == "__main__":
    main()
