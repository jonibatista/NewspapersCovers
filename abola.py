#!/usr/bin/python
import json
import os
import datetime
from datetime import timedelta

## DEF CONSTANTS
G_SRC_FOLDER = "C:/Users/INOV2073/Documents/abola" #"/Users/jbatista/Pictures/abola/"

## load configuration from file
file = open('config.txt', 'r') #specify file to open

jsonObj = ""
for item in file.readlines():
	item =  item.replace("\t", "")
	jsonObj = jsonObj + item.replace("\n", "")

##print jsonObj

##print json.dumps(jsonObj)


## get last cover downloaded
listCovers = os.listdir(G_SRC_FOLDER)
listCovers.sort()
lastDownload = ""

## get the date of the last cover
for i in listCovers[-1]:
	if i.isdigit():
		lastDownload = lastDownload + i

year = abs(int(lastDownload)/10000) #YYYY.mmdd
month = int(lastDownload)%10000 #yyyy.MMDD
month = int(month)/100 #MM.dd
day = int(lastDownload)%100 #yyyymm.DD

lastDate = datetime.date(int(year), int(month), int(day))

## get the curent date
today = datetime.date.today()
#now = datetime.date(today.year, today.month, today.day)

i = 7 # the abola newspaper only allow us to backward 7 days  
while(today > lastDate and i > 0):
	
	print ("Downloading abola newspaper cover of ", str(today), "...")
	# done, lets go back one more day
	today -= timedelta(days=1)
	i -=1


