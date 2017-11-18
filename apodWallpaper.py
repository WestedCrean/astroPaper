import datetime
import random
import platform
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse
import urllib.error
import subprocess
import os
import __main__
import ctypes
from calendar import monthrange 
#TODO: clear old wallpapers
#TODO: do Windows and Linux wallpaper
#TODO: get target os resolution and crop image according to it
print("Start in debug mode?")
print("y/n")
debugMode = False
userInput = input()
if userInput.lower() == "y" :
    debugMode = True
#generate random date
current_system = platform.system()
if debugMode:
    print("Current system: ", current_system)
def _random_apod_link():
    random.seed()
    now = datetime.datetime.now()
    random_date = 000000
    #safety net so we won't get a date from the future
    may_be_current_date = False

    #rolling year
    year = random.randint(7, now.year % 100) #7-17
    if year == now.year % 100 :
        may_be_current_date = True
    random_date += year * 10000
    
    #rolling month
    if may_be_current_date:
        #if current year
        month = random.randint(1, now.month)
        #here we get rid of the flag, for sure it's legit
        if month != now.month:
            may_be_current_date = False
    else:
        month = random.randint(1, 12)
    
    random_date += month * 100

    #rolling day
    if may_be_current_date:
        day = random.randint(1, now.day - 1)
    else:

        month_range = monthrange(year, month)#setting up the wallpaper, depending on a systemr, month) #to be sure
        day = random.randint(month_range[0], month_range[1])
        #print "day : ", temp
    random_date += day
    #convert to string
    random_date = str('%06d' % random_date)
    if debugMode:
        print("Date: " + random_date)
    _apod_url = "https://apod.nasa.gov/apod/ap" + random_date + ".html"
    return _apod_url

def _get_image_link():
    while True:
        try:
            while True:
                try:
                    html_page = urllib.request.urlopen(_random_apod_link()) #sometime this line throws
                    break
                except urllib.error.HTTPError:
                    if debugMode:
                        print("Request Failed, trying again with different link")
    #urllib2.HTTPError: HTTP Error 404: Not Found
            soup = BeautifulSoup(html_page, "lxml")
            for link in soup.findAll('a', attrs={'href': re.compile("\b*?image/")}):
                link.get('href')
                templink = link.get('href')
            directlink = "https://apod.nasa.gov/apod/" + templink #sometimes this line throws 
            #UnboundLocalError: local variable 'templink' referenced before assignment
            # THIS IS CAUSED when link is not an image
            break
        except UnboundLocalError:
            if debugMode:
                print("Link isn't an image, trying again with different one.")
    return directlink
    
def _get_apod():
    global currentRandomWallpaper
    url = _get_image_link()
    file_name = url.split('/')[-1]
    currentRandomWallpaper = file_name
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()

    f.close()

_get_apod()
if debugMode:
    print("Downloaded") #checking if function did it's job
    print("Setting up the wallpaper")

wallpaper_path = os.path.abspath(__file__)
wallpaper_path = re.sub(r'apodWallpaper.py', '', wallpaper_path)
wallpaper_path = str(wallpaper_path) + str(currentRandomWallpaper)
if debugMode:
    print("Current random wallpaper absolute path : " + wallpaper_path)

#setting up the wallpaper, depending on a system
if current_system == "Windows":
     #windows set up
    if debugMode:
        print("Whaddup")
if current_system == "Darwin":
    try:
        from appscript import app, mactypes
    except:
        if debugMode:
            print("Appscript not installed.")
    #macos set up
    app('Finder').desktop_picture.set(mactypes.File(wallpaper_path))