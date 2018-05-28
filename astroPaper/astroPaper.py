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
#import cv2
import numpy as np

def getValidDate():
    d = datetime.datetime.now()
    year = random.randint(2004, d.year)
    month = random.randint(1, 12)
    day = random.randint(1, 31)
    randomDate = datetime.date(year, month, day)
    try:

        checkDate = lambda rdate : datetime.datetime.strptime(rdate, "%y%m%d")
        print("Valid date!")
        checkDate(randomDate)
        randomDate = datetime.date.strftime(randomDate, "%y%m%d")
        return randomDate

    except ValueError:
        print("Invalid date!")
        return getValidDate()

def getLink(date):
    return "https://apod.nasa.gov/apod/ap" + str(date) + ".html"

def getImgLinkFromURL(url):
    print("Trying to crawl url: " + url)
    success = False
    while(not success):
        try:
            print("Inside while loop")
            html_page = urllib.request.urlopen(url)#sometime this line throws urllib2.HTTPError: HTTP Error 404: Not Found
            success = True
        except urllib.error.HTTPError:
            print("404 getImgLinkFromURL()")
            return -1
    html_page = str(html_page.read())
    
    imglink = re.search(r"href=[\\'\"]?([^\'\" >]+)?(.jpg|.jpeg|.png)", html_page)
    if imglink:
        imglink = imglink.group(0)[6:]
        #url += imglink
    return "https://apod.nasa.gov/apod/" + imglink

def getimgLink():
    date = getValidDate()
    link = getLink(date)
    imgURL = getImgLinkFromURL(link)
    return imgURL

def downloadImage(url):
    global currentRandomWallpaper
    file_name = url.split('/')[-1]
    currentRandomWallpaper = file_name
    print("Downloading " + file_name)
    try:
        #with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        #       shutil.copyfileobj(response, out_file)
        #       return file_name
        return urllib.request.urlretrieve(url, '/code/astroPaper/' + currentRandomWallpaper)
    except urllib.error.HTTPError:
        print("Request Failed, (downloadImage().exception.HTTPError)")
    except Exception:
        print("Request Failed, (downloadImage().exception)")

def getPlatform():
    return platform.system()

def newWallpaper():
    validFileFound = False
    downloadSuccess = False
    while(not downloadSuccess):
        while(not validFileFound):
            imglink = getimgLink()
            if(imglink != -1):
                validFileFound = True
        wallpaper = downloadImage(imglink)
        downloadSuccess = True
    return wallpaper

def getPath(wallpaper):
    #TODO make folder for photographs in another place
    wallpaper_path = os.path.abspath(__file__)
    wallpaper_path = re.sub(__file__, '', wallpaper_path)
    wallpaper_path = str(wallpaper_path) + str(wallpaper)
    print("Current random wallpaper absolute path : " + wallpaper_path)
    return wallpaper_path

def wallpaperSetup(current_system, wallpaper):
    print("wallpaperSetup")
    wallpaper_path = getPath(wallpaper)
    #setting up the wallpaper, depending on a system
    if current_system == "Windows":
        #windows set up
        print("Windows script")
        try:
            import ctypes
            SPI_SETDESKTOPWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKTOPWALLPAPER, 0, wallpaper_path, 0)
            print("Wallpaper set up!")
        except:
            print("Ctypes not installed")

    if current_system == "Darwin":
        print("MacOS script")
        try:
            setWallpaperCommand = "osascript -e 'tell application \"Finder\" to set desktop picture to POSIX file \"" + wallpaper_path + "\"'"
            os.system(setWallpaperCommand)
            print("Wallpaper set up!")
        except:
            print("Appscript not installed.")
        #macos set up

    if current_system == "Linux":
        print("Linux script")
        try:
            os.system("gsettings set org.gnome.desktop.background picture-uri file:///" + wallpaper_path)
            print("Wallpaper set up!")
        except:
            print("gsettings not working")

def main():
    current_system = getPlatform()
    wallpaper = newWallpaper()
    wallpaperSetup(current_system, wallpaper)
    print("Done")
    


if __name__ == "__main__":
    main()
