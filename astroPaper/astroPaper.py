#! /usr/bin/env python3
# ------ NASA's Astronomy Picture of the Day ------
# -------- Random wallpaper by Wiktor Flis --------

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
import cv2
import numpy as np


#TODO: make clearOldWallpapers() method clear every image except the last one
#TODO: set Linux wallpaper, probably only gnome and unity
#TODO: check if downloaded wallpaper is ok
#TODO: if downloaded wallpaper is a panorama (for example) and image ratio is not right,
#have it filled with black spaces
#TODO: make slideshow like transformations from one wallpaper to another
#TODO: UI and "add to favourites" button

#generate random date

current_system = platform.system()

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# astropaper 2.0

def getValidDate():
    random.seed()
    randomDate = 000000 # TODO: delet dis
    may_be_current_date = False
    now = datetime.datetime.now()

    year = random.randint(7, now.year % 100)
    if year == now.year % 100:
        may_be_current_date = True
    randomDate += year * 10000
    if(may_be_current_date):
        month = random.randint(1,now.month)
    else:
        month = random.randint(1,13)
    randomDate += month * 100
    if(may_be_current_date):
        day = random.randint(1, now.day)
    else:
        if(month == 2):
            if(abs(year - 16) % 4 == 0):
                day = random.randint(1, 29)
            else:
                day = random.randint(1, 28)
        else:
            if(month < 8):
                if(not month%2):
                    day = random.randint(1, 31)
                else:
                    day = random.randint(1, 30)
            else:
                if(month%2):
                    day = random.randint(1, 31)
                else:
                    day = random.randint(1, 30)
    randomDate += day
    print("random date: " + str(randomDate))
    return randomDate

def getLink(date):
    return "https://apod.nasa.gov/apod/ap" + str(date) + ".html"

def crawlURL(url):
    directlink = "https://apod.nasa.gov/apod/"
    imglink = ""
    success = False
    while(not success):
        try:
            html_page = urllib.request.urlopen(url)#sometime this line throws urllib2.HTTPError: HTTP Error 404: Not Found
            success = True
            print("Crawled sucessfuly")
        except urllib.error.HTTPError:
            print("Crawl Failed, retrying ((crawlURL().exception.HTTPError))")
            return -1
    html_page = str(html_page.read())
    
    imglink = re.search(r"href=[\\'\"]?([^\'\" >]+)?(.jpg|.jpeg|.png)", html_page)
    if imglink:
        imglink = imglink.group(0)[6:]
        directlink += imglink
    print("Image direct link: " + directlink)
    return directlink

def downloadImage(url):
    global currentRandomWallpaper
    file_name = url.split('/')[-1]
    currentRandomWallpaper = file_name
    print("Downloading " + url + " ...")
    try:
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                return
    except urllib.error.HTTPError:
        print("Request Failed, trying again. (downloadImage().exception.HTTPError)")
    except Exception:
        print("Request Failed, trying again. (downloadImage().exception)")
        pass
    return currentRandomWallpaper
    

def rollAWallpaper():
    date = getValidDate()
    link = getLink(date)
    check = crawlURL(link)
    return check

def mainRoutine():
    validFileFound = False
    downloadSuccess = False
    while(not downloadSuccess):
        while(not validFileFound):
            check = rollAWallpaper()
            if(check != -1):
                validFileFound = True
        url = check

        wallpaper = downloadImage(url)
        downloadSuccess = True
        

#def addToFavourites():
'''
pseudocode:
if there is a lot of text:
    downlaod another image
if image_width < screen_width
    use opencv to flip it sideways, resolution is ok so it's just about it
now just cut the most interesting spot on the image into screen_height*screen_width resolution and voila
'''
def isWallpaperPretty(currentRandomWallpaper):
    #-------------
    # here will go openCV code for deciding if image is "pretty" (suitable for a wallpaper)
    #-------------
    img = cv2.imread(currentRandomWallpaper, 1)
    img_height, img_width = img.shape[0], img.shape[1] #not working well
    screen_width = root.winfo_screenwidth() #tolerance
    screen_height = root.winfo_screenheight() #tolerance
    print("Current screen's width: " + str(screen_width))
    print("Current screen's height: " + str(screen_height))
    print("Image width: " + str(img_width))
    print("Image height: " + str(img_height))
    if(img_width < screen_width or img_height < screen_height):
        # image resolution is smaller than target resolution
        print("Image resolution is smaller than target resolution")
        return False
    if(img_height > img_width):
        #rotate
        print("Rotating!")

        np.transpose(img)
    return True

def wallpaperSetup(current_system, wallpaper_path):
    print("wallpaperSetup")
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
            setWallpaperScript = """/usr/bin/osascript<<END tell application "Finder" set desktop picture to POSIX file "{}" end tell END"""
            os.system(setWallpaperScript.format(wallpaper_path))
            print("Wallpaper set up!")
        except:
            print("osascript not working")
        #macos set up

    if current_system == "Linux":
        print("Linux script")
        try:
            os.system("gsettings set org.gnome.desktop.background picture-uri file:///" + wallpaper_path)
            print("Wallpaper set up!")
        except:
            print("gsettings not working")

def getPath(wallpaper):
    #TODO make folder for photographs in another place
    wallpaper_path = os.path.abspath(__file__)
    print("Wallpaper path: " + str(wallpaper_path))
    wallpaper_path = re.sub(r'astroPaper.py', '', wallpaper_path)
    wallpaper_path = str(wallpaper_path) + str(wallpaper)
    print("Current random wallpaper absolute path : " + wallpaper_path)
    return wallpaper_path

def clearOldWallpapers(dir, lastWallpaperName): #add global wallpaper save folder string
    for file in os.listdir(dir):
        if(file != "apodWallpaper.py" or file != maxfile):
            if file.endswith('.jpg' or '.png'):
                os.remove(os.path.join(dir, file))
'''
def main():

    path = "/Users/WestedCrean/Pictures/"
    wallpaper = ""
    mainRoutine()
    
    wallpaperSetup(current_system, currentRandomWallpaper)
    print("Done")



if __name__ == "__main__":
    main()
'''