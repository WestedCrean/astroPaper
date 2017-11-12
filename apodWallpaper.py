import datetime
import random
from selenium import webdriver
from calendar import monthrange # so I don't have to deal with leap years
#what's fucked in this code? Well when does nasa updates its apod page?
#timezone difference sux
#maybe just leave today's apod, there's still plenty of images
#generate random date
random.seed()
now = datetime.datetime.now()
random_date = 000000
may_be_current_date = False
temp = random.randint(7, now.year % 100) #7-17
if temp == now.year % 100 :
    may_be_current_date = True
print("year: %d", temp)
random_date += temp * 10000
if may_be_current_date == True :
    temp = random.randint(1, now.month)
    if temp != now.month:
        may_be_current_date = False
else:
    temp = random.randint(1, 12)
    print("month: %d", temp)
random_date += temp * 100
if may_be_current_date == True :
    temp = random.randint(1, now.day)
else:
    month_range = monthrange(now.year, now.month)
    temp = random.randint(month_range[0], month_range[1])
print("day : %d", temp)
random_date += temp
#convert to string
random_date = str('%06d' % random_date)
_apod_url = "https://apod.nasa.gov/apod/ap" + random_date + ".html"
driver = webdriver.Chrome()                                 #instance of Chrome WebDriver is created
driver.get(_apod_url)