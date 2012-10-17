#!/usr/bin/python
import json
import os
import datetime
from datetime import timedelta

## load configuration from file
file = open('config.txt', 'r') #specify file to open

jsonObj = ""
for item in file.readlines():
	item =  item.replace("\t", "")
	jsonObj = jsonObj + item.replace("\n", "")

##print jsonObj

##print json.dumps(jsonObj)


## get last cover downloaded
listCovers = os.listdir('/Users/jbatista/Pictures/abola/')
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

lastDate = datetime.date(year, month, day)

## get the curent date
timestamp = datetime.datetime.now()
now = datetime.date(timestamp.year, timestamp.month, timestamp.day)

i = 7 # the abola newspaper only allow us to backward 7 days  
while(now > lastDate and i > 0):
	
	print "Downloading abola newspaper cover of ", str(now), "..."
	# done, lets go back one more day
	now -= timedelta(days=1)
	i -=1


