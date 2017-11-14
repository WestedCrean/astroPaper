import datetime
import random
import platform
from BeautifulSoup import BeautifulSoup
import re
import urllib2
import struct
from appscript import app, mactypes
import subprocess
import os
import ctypes
from calendar import monthrange # so I don't have to deal with leap years
#what's fucked in this code? Well when does nasa updates its apod page?
#timezone difference sux
#maybe just leave today's apod, there's still plenty of images
#TODO: check for leap years because sometimes it isn't working
#generate random date
current_system = platform.system()
print("Current system: ", current_system)
def _random_apod_link():
    random.seed()
    now = datetime.datetime.now()
    random_date = 000000
    #safety net so we won't get a date from the future
    may_be_current_date = False

    #rolling year
    temp = random.randint(7, now.year % 100) #7-17
    if temp == now.year % 100 :
        may_be_current_date = True
    random_date += temp * 10000

    #rolling month
    if may_be_current_date:
        #if current year
        temp = random.randint(1, now.month)
        #here we get rid of the flag, for sure it's legit
        if temp != now.month:
            may_be_current_date = False
    else:
        temp = random.randint(1, 12)
    random_date += temp * 100

    #rolling day
    if may_be_current_date:
        temp = random.randint(1, now.day - 1)
    else:
        month_range = monthrange(now.year, now.month)
        temp = random.randint(month_range[0], month_range[1])
        #print "day : ", temp
    random_date += temp
    #convert to string
    random_date = str('%06d' % random_date)
    #print("rolled date: " + random_date)
    _apod_url = "https://apod.nasa.gov/apod/ap" + random_date + ".html"
    return _apod_url

def _get_image_link():
    html_page = urllib2.urlopen(_random_apod_link())
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a', attrs={'href': re.compile("\b*?image/")}):
        link.get('href')
        templink = link.get('href')
    directlink = "https://apod.nasa.gov/apod/" + templink
    return directlink
    
def _get_apod():
    global currentRandomWallpaper
    url = _get_image_link()
    file_name = url.split('/')[-1]
    currentRandomWallpaper = file_name
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

_get_apod()
print("Suck a dick!")

#setting up the wallpaper, depending on a system

if current_system == "Windows":
    #windows set up
    printf("Whaddup")
if current_system == "Darwin":
    #macos set up
    wallpaper_path = os.path.abspath(__file__)
    wallpaper_path = re.sub(r'apodWallpaper.py', '', wallpaper_path)
    wallpaper_path = str(wallpaper_path) + str(currentRandomWallpaper)
    print "Current random wallpaper abspath : " , wallpaper_path #
    app('Finder').desktop_picture.set(mactypes.File(wallpaper_path))