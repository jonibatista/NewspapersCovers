#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3
import os
import datetime
from datetime import timedelta
import urllib.request
import sys


## DEF CONSTANTS
G_DAYS_OF_WEEK = ['wseg', 'wter', 'wqua', 'wqui', 'wset', 'wsab', 'wdom']
G_FILENAME_SUFFIX = "abola" # number are not allowed!!!
G_PARAM_DIR = "root_dir"
G_PARAM_SHARED="share_src"
G_PARAM_SRC="src"

## BEGIN
print ("Starting the Abola covers update on ", datetime.datetime.now())

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
	srcFolder = params[G_PARAM_DIR] + "/" + "abola/"

## get last cover downloaded
try:
	if not os.path.exists(params[G_PARAM_DIR]):
		print ("The " + params[G_PARAM_DIR] + " doen't exists")
		exit()
	elif not os.path.exists(srcFolder):
		os.makedirs(srcFolder)

	listCovers = os.listdir(srcFolder) 
except:
    print("Error! ", srcFolder, " - ", sys.exc_info()[0])
    exit()


## get the date of the last cover
if len(listCovers) > 0:

	listCovers.sort()
	for n in reversed(range(len(listCovers))):
		lastDownload = ""

		for i in listCovers[n]:
			if i.isdigit():
				lastDownload = lastDownload + i

		if G_FILENAME_SUFFIX in listCovers[n]: 
			break

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
	exit()

i = 7 # the abola newspaper only allow us to backward 7 days  
while(today > lastDate and i > 0):
	
	print ("Downloading abola newspaper cover of " + str(today) + "...", end=" ")
	sys.stdout.flush()

	# build the URL of the cover link
	url = 'http://www.abola.pt/' + G_DAYS_OF_WEEK[today.weekday()] + '/wfotosdia/wdiag.jpg'

	# create desdination filename 'YYYYMMDD.jpeg'
	filename = str(today).replace("-", "") + "_" + G_FILENAME_SUFFIX + ".jpeg"
	
	# create destination file
	f = open(srcFolder + filename, 'wb')

	# download image and write it HDD
	f.write(urllib.request.urlopen(url).read())
	f.close()

	print ("done!")
	
	# done, lets go back one more day
	today -= timedelta(days=1)
	i -=1

print ("Abola's covers was successfully updated on ", datetime.datetime.now())
# EDN OF SCRIPT