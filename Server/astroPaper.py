#! /usr/bin/env python3
# ------ NASA's Astronomy Picture of the Day ------
# -------- Random wallpaper by Wiktor Flis --------
#
import datetime
import random
import platform
import re
import urllib.request
import urllib.error
import urllib.parse
import tkinter as tk
import struct
import subprocess
import os
import shutil
import __main__
import numpy as np
import requests
import sys

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
    #print(url)
    try:
        html_page = urllib.request.urlopen(url)
        html_page = str(html_page.read())
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

def downloadImage(url):
    global currentRandomWallpaper
    file_name = url.split('/')[-1]
    file_name
    r = requests.get(url, stream=True)
    size = r.headers.get('Content-Length')
    size = int(size)
    os.path.abspath(__file__)
    path = os.path.abspath(__file__)
    path = re.sub(__file__, '', path)


    with open(path + '/' + file_name, 'wb') as file:
        download = 0
        for chunk in r.iter_content(256):
            download += len(chunk)
            file.write(chunk)
            sys.stdout.write("Done: %d / %d bytes\r" % (download, size))
            sys.stdout.flush()
    return file_name

def getPlatform():
    return platform.system()

def newWallpaper():
    imglink = getimgLink()
    while True:
        try:
            wallpaper = downloadImage(imglink)
            break
        except Exception as e:
            print("Exception:")
            print(e)
    return wallpaper

def getPath(wallpaper):
    #TODO make folder for photographs in another place
    wallpaper_path = os.path.abspath(__file__)
    wallpaper_path = re.sub(__file__, '', wallpaper_path)
    wallpaper_path = str(wallpaper_path) + str(wallpaper)
    #print("Current random wallpaper absolute path : " + wallpaper_path)
    return wallpaper_path

def wallpaperSetup(current_system, wallpaper):
    wallpaper_path = getPath(wallpaper)
    #setting up the wallpaper, depending on a system
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
            setWallpaperCommand = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + wallpaper_path + "\"'"
            os.system(setWallpaperCommand)
            return 0
        except:
            print("Appscript not installed.")
        #macos set up

    if current_system == "Linux":
        try:
            os.system("gsettings set org.gnome.desktop.background picture-uri file:///" + wallpaper_path)
            return 0
        except:
            print("gsettings not working")
    return -1

def main():
    current_system = getPlatform()
    wallpaper = newWallpaper()
    #print(wallpaper)
    wallpaperSetup(current_system, wallpaper)
    #print(wallpaper)

if __name__ == "__main__":
    main()
