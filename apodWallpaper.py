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
print("Current system: ", current_system)
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print("Current screen's width: " + str(screen_width))
print("Current screen's height: " + str(screen_height))

# astropaper 2.0

def getValidDate():
    random.seed()
    random_date = 000000 # TODO: delet dis
    may_be_current_date = False
    now = datetime.datetime.now()

    year = random.randint(7, now.year % 100 + 1)
    if year == now.year % 100:
        may_be_current_date = True
    random_date += year * 10000
    if(may_be_current_date):
        month = random.randint(1,now.month + 1)
    else:
        month = random.randint(1,13)
    random_date += month * 100
    if(may_be_current_date):
        day = random.randint(1, now.day + 1)
    else:
        if(month == 02):
            if(abs(year - 16) % 4 == 0):
                day = random.randint(1, 30)
            else:
                day = random.randint(1, 29)
        else:
            if(month < 8):
                if(not month%2):
                    day = random.randint(1, 32)
                else:
                    day = random.randint(1, 31)
            else:
                if(month%2):
                    day = random.randint(1, 32)
                else:
                    day = random.randint(1, 31)
    random_date += day
    return random_date

def getLink(date):
    return "https://apod.nasa.gov/apod/ap" + date + ".html"

def crawlURL(url):
    directlink = "https://apod.nasa.gov/apod/"
    imglink = ""
    try:
        html_page = urllib.request.urlopen(url)#sometime this line throws urllib2.HTTPError: HTTP Error 404: Not Found
    except urllib.error.HTTPError:
        print("Request Failed, trying again with different link")
    try:
        html_page = str(html_page.read())
        iframe = re.search(r"iframe", html_page)
        if(iframe):
            return -1
        imglink = re.search(r"href=[\\'\"]?([^\'\" >]+)?(.jpg|.jpeg|.png)", html_page)
        if imglink:
            directlink += imglink
        else:
            return -1
    return directlink

def downloadImage(url, path):
    currentWallpaperPath = ""
    file_name = url.split('/')[-1]
    currentRandomWallpaper = file_name
    print("Downloading ...")
    try:
        with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                return
    except urllib.error.HTTPError:
        print("Request Failed, trying again.")
    except urllib.request.http.client.BadStatusLine:
        print("Request Failed, trying again.")
    except:
        print("_get_apod() fucked up")

    return currentWallpaperPath

def rollAWallpaper():
    date = getValidDate()
    link = getLink(date)
    check = crawlURL(link)
    return check

def mainRoutine(path):
    validFileFound = False
    while(not validFileFound):
        check = rollAWallpaper()
        if(check not -1):
            validFileFound = True
    url = check

    return downloadImage(url, path) 

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

def wallpaperSetup(current_system, wallpaperPath):
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
            from appscript import app, mactypes
            app('Finder').desktop_picture.set(mactypes.File(wallpaper_path))
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

def getPath(wallpaper):
    #TODO make folder for photographs in another place
    wallpaper_path = os.path.abspath(__file__)
    wallpaper_path = re.sub(r'apodWallpaper.py', '', wallpaper_path)
    wallpaper_path = str(wallpaper_path) + str(wallpaper)
    print("Current random wallpaper absolute path : " + wallpaper_path)
    return wallpaper_path

def clearOldWallpapers(dir, lastWallpaperName): #add global wallpaper save folder string
    for file in os.listdir(dir):
        if(file != "apodWallpaper.py" or file != maxfile):
            if file.endswith('.jpg' or '.png'):
                os.remove(os.path.join(dir, file))

def main():
    path = "/Users/WestedCrean/Pictures/"
    wallpaper = mainRoutine(path)
    wallpaperSetup(wallpaper)
    print("Done")


if __name__ == "__main__":
    main()
