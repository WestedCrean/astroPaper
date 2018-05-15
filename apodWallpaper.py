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
    randomDate = '{}-{}-{}'.format(year,month,day)
    try:
        checkDate = lambda rdate : datetime.datetime.strptime(rdate, '%Y-%m-%d')
        checkDate(randomDate)
        print("Valid date!")
        randomDate = randomDate.split('-')
        #here

        randomDate = ''.join(randomDate)
        print(str(randomDate[2:]))
        return randomDate[2:]

    except ValueError:
        print("Invalid date!")
        return getValidDate()

def getLink(date):
    return "https://apod.nasa.gov/apod/ap" + str(date) + ".html"

def crawlURL(url):
    print("Trying to crawl url: " + url)
    directlink = "https://apod.nasa.gov/apod/"
    imglink = ""
    success = False
    while(not success):
        try:
            print("Inside while loop")
            html_page = urllib.request.urlopen(url)#sometime this line throws urllib2.HTTPError: HTTP Error 404: Not Found
            success = True
        except urllib.error.HTTPError:
            print("Crawl Failed, retrying ((crawlURL().exception.HTTPError))")
            return -1
    html_page = str(html_page.read())
    
    imglink = re.search(r"href=[\\'\"]?([^\'\" >]+)?(.jpg|.jpeg|.png)", html_page)
    if imglink:
        imglink = imglink.group(0)[6:]
        directlink += imglink
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
    
def getPlatform():
    current_system = platform.system()
    #print("Current system: ", current_system)

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
    wallpaper = ""
    mainRoutine()
    
    wallpaperSetup(current_system, currentRandomWallpaper)
    print("Done")
    


if __name__ == "__main__":
    main()
