import datetime
import random
import platform
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.error
import urllib.parse
import lxml
import tkinter as tk
import struct
import subprocess
import os
import shutil
import __main__
import ctypes
from calendar import monthrange 


#TODO: make clearOldWallpapers() method clear every image except the last one
#TODO: set Linux wallpaper, probably only gnome and unity
#TODO: check if downloaded wallpaper is ok

#generate random date
current_system = platform.system()
print("Current system: ", current_system)
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print("Current screen's width: " + str(screen_width))
print("Current screen's height: " + str(screen_height))

#-------------
# getting image functions
#-------------
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
        month_range = monthrange(year, month) #to be sure
        day = random.randint(month_range[0], month_range[1])
        #print "day : ", temp
    random_date += day
    #convert to string
    random_date = str('%06d' % random_date)
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
                    print("Request Failed, trying again with different link")
    #urllib2.HTTPError: HTTP Error 404: Not Found
            try:
                soup = BeautifulSoup(html_page, "lxml")
            except:
                print("lxml not found, using built-in html.parser")
                soup = BeautifulSoup(html_page, "html.parser")
            for link in soup.findAll('a', attrs={'href': re.compile("\b*?image/")}):
                link.get('href')
                templink = link.get('href')
            directlink = "https://apod.nasa.gov/apod/" + templink #sometimes this line throws 
            #UnboundLocalError: local variable 'templink' referenced before assignment
            # THIS IS CAUSED when link is not an image
            break
        except UnboundLocalError:
            print("Link isn't an image, trying again with different one.")
    return directlink
    
def _get_apod():
    global currentRandomWallpaper
    url = _get_image_link()
    file_name = url.split('/')[-1]
    currentRandomWallpaper = file_name
    print("Downloading ...")
    while True:
        try:
            with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
                return 
            break
        except urllib.error.HTTPError:
            print("Request Failed, trying again.")

#-------------
# here will go openCV code for deciding if image is "pretty" (suitable for a wallpaper)
#-------------
'''
pseudocode:
if imageResolution < screen_width*screen_height:
    download another image
if there is a lot of text:
    downlaod another image
if image_width < screen_width
    use opencv to flip it sideways, resolution is ok so it's just about it
now just cut the most interesting spot on the image into screen_height*screen_width resolution and voila
'''
# ------------
# here will go openCV code for cutting wallpaper
#-------------


def wallpaperSetup(current_system):


    print("Setting up the wallpaper")
    wallpaper_path = os.path.abspath(__file__)
    wallpaper_path = re.sub(r'apodWallpaper.py', '', wallpaper_path)
    wallpaper_path = str(wallpaper_path) + str(currentRandomWallpaper)
    print("Current random wallpaper absolute path : " + wallpaper_path)

    #setting up the wallpaper, depending on a system
    if current_system == "Windows":
        #windows set up
        print("Windows script")
        SPI_SETDESKTOPWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKTOPWALLPAPER, 0, wallpaper_path, 0)
        print("Desktop background set up")
        
    if current_system == "Darwin":
        print("MacOS script")
        try:
            from appscript import app, mactypes
        except:
            print("Appscript not installed.")
        #macos set up
        app('Finder').desktop_picture.set(mactypes.File(wallpaper_path))
    
    if current_system == "Linux":
        print("Linux script")

def getPath():
    wallpaper_path = os.path.abspath(__file__)
    wallpaper_path = re.sub(r'apodWallpaper.py', '', wallpaper_path)
    return wallpaper_path

def clearOldWallpapers(dir, lastWallpaperName): #add global wallpaper save folder string
    for file in os.listdir(dir):
        if file != lastWallpaperName:    
            if file.endswith('.jpg'):
                os.remove(os.path.join(dir, file))

def main():
    while True:
        try:
            _get_apod()
            break
        except urllib.request.http.client.BadStatusLine:
            print("Request Failed, trying again.")
    print("Downloaded") #checking if function did it's job
    #cleanOtherWallpapers
    #editWallpaper
    
    wallpaperSetup(current_system)
    clearOldWallpapers(getPath(), currentRandomWallpaper)
    #waitForAnotherRound
    pass
main()
'''
if __name__ == "__main__":
    main(sys.argv)
'''