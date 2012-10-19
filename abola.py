#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3


import json
import os
import datetime
from datetime import timedelta
import urllib.request

## DEF CONSTANTS
G_SRC_FOLDER =  "/Users/jbatista/Pictures/abola/"
G_DAYS_OF_WEEK = ['wseg', 'wter', 'wqua', 'wqui', 'wset', 'wsab', 'wdom']

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
lastDownload = ""

## get the date of the last cover
if len(listCovers) > 0:

	listCovers.sort()
	for i in listCovers[-1]:
		if i.isdigit():
			lastDownload = lastDownload + i


	try:
		year = int(lastDownload)/10000 #YYYY.mmdd
		month = int(lastDownload)%10000 #yyyy.MMDD
		month = int(month)/100 #MM.dd
		day = int(lastDownload)%100 #yyyymm.DD

		lastDate = datetime.date(int(year), int(month), int(day))

	except:
		#download all covers, a complete week....
		lastDate = datetime.date.today() - timedelta(days=7)

else:
		#download all covers, a complete week....
		lastDate = datetime.date.today() - timedelta(days=7)


## get the curent date
today = datetime.date.today()
#now = datetime.date(today.year, today.month, today.day)

if today == lastDate:
	print("Nothing new. No covers to download....")

i = 7 # the abola newspaper only allow us to backward 7 days  
while(today > lastDate and i > 0):
	
	print ("Downloading abola new spaper cover of " + str(today) + "...")

	# build the URL of the cover link
	url = 'http://www.abola.pt/' + G_DAYS_OF_WEEK[today.weekday()] + '/wfotosdia/wdiag.jpg'

	# create desdination filename 'YYYYMMDD.jpeg'
	filename = str(today.year) + str(today.month) + str(today.day)  + ".jpeg"
        
	# create destination file
	f = open(G_SRC_FOLDER + filename, 'wb')

	# download image and write it HDD
	f.write(urllib.request.urlopen(url).read())
	f.close()

	print ("done!")
	
	# done, lets go back one more day
	today -= timedelta(days=1)
	i -=1

# EDN OF SCRIPT