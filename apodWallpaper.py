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
#TODO: check if it's image or just catch exceptions
#TODO: clear old wallpapers
#TODO: do Windows and Linux wallpaper
#TODO: get target os resolution and crop image according to it

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
    html_page = urllib2.urlopen(_random_apod_link()) #sometime this line throws
    #urllib2.HTTPError: HTTP Error 404: Not Found
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a', attrs={'href': re.compile("\b*?image/")}):
        link.get('href')
        templink = link.get('href')
    directlink = "https://apod.nasa.gov/apod/" + templink #sometimes this line throws 
    #UnboundLocalError: local variable 'templink' referenced before assignment
    # THIS IS CAUSED when link is not an image
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
for x in range(1,100):
    _get_image_link()
print("Downloaded") #checking if function did it's job
'''
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
#setting up the wallpaper, depending on a system
'''