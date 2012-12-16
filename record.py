#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3
import os
import datetime
from datetime import timedelta
import urllib.request
import sys
from bs4 import BeautifulSoup
import string


## DEF CONSTANTS
G_PARAM_DIR = "root_dir"
G_PARAM_SHARED="share_src"
G_PARAM_SRC="src"
G_FILENAME_SUFFIX = "record" # number are not allowed!!!

## BEGIN
print ("Starting the Record covers update on ", datetime.datetime.now())

## load configuration from file
file = open('config.txt', 'r') #specify file to open


params = {}
# parse the configuration file parameters
for item in file.readlines():
    temp = item.replace('\n', '').split('=')
    params[str(temp[0])] = str(temp[1])

# set the directory folder
if params[G_PARAM_SHARED] == 'true':
    srcFolder = params[G_PARAM_DIR] + "/" + params[G_PARAM_SRC] + "/"
else:
    srcFolder = params[G_PARAM_DIR] + "/" + "record/"    

# url of the today's cover 
url = "http://www.record.xl.pt/capas/default.aspx?page=1"

# Create http request to get the new page source html content
html = urllib.request.urlopen(url).read()

# load the page into the DOM parser
soup = BeautifulSoup(html)

# get the cover container
coverDiv = soup.find("div", {"class": "capa-grande-container"})

# get the image uri
img = coverDiv.img['src']
urlImg = 'http://www.record.xl.pt' + str(img)

# create desdination filename 'YYYYMMDD.jpeg'
date = str(datetime.date.today())
filename = str(date).replace("-", "") + "_" + G_FILENAME_SUFFIX + ".jpeg"
   
# create destination file
f = open(srcFolder + filename, 'wb')

# download image and write it HDD
f.write(urllib.request.urlopen(urlImg).read())
f.close()

print ("ok!")

print ("Record's covers was successfully updated on ", datetime.datetime.now())
# EDN OF SCRIPT
