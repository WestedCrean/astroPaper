import datetime
import random
from BeautifulSoup import BeautifulSoup
import re
import urllib2
import scrapy
from selenium import webdriver
from calendar import monthrange # so I don't have to deal with leap years
#what's fucked in this code? Well when does nasa updates its apod page?
#timezone difference sux
#maybe just leave today's apod, there's still plenty of images
#TODO: check for leap years because sometimes it isn't working
#generate random date
def _random_apod_link():
    random.seed()
    now = datetime.datetime.now()
    random_date = 000000
    may_be_current_date = False
    temp = random.randint(7, now.year % 100) #7-17
    if temp == now.year % 100 :
           may_be_current_date = True
    #print("year: "" temp)
    random_date += temp * 10000
    if may_be_current_date:
        temp = random.randint(1, now.month)
        if temp != now.month:
            may_be_current_date = False
    else:
        temp = random.randint(1, 12)
    print "month: ", temp
    random_date += temp * 100
    if may_be_current_date:
        temp = random.randint(1, now.day)
    else:
        month_range = monthrange(now.year, now.month)
        temp = random.randint(month_range[0], month_range[1])
        #print("day : " temp)
    random_date += temp
    #convert to string
    random_date = str('%06d' % random_date)
    print("rolled date: " + random_date)
    _apod_url = "https://apod.nasa.gov/apod/ap" + random_date + ".html"
    return _apod_url
def dive_and_get_image():
    html_page = urllib2.urlopen(_random_apod_link())
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a', attrs={'href': re.compile("\b*?image/")}):
        link.get('href')
        templink = link.get('href')
    directlink = "https://apod.nasa.gov/apod/" + templink
    print directlink
dive_and_get_image()