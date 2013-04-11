#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3
import os
import datetime
from datetime import timedelta
import urllib.request
import sys


## DEF CONSTANTS
G_DAYS_OF_WEEK = ['wseg', 'wter', 'wqua', 'wqui', 'wset', 'wsab', 'wdom']
G_FILENAME_SUFFIX = "abola" # number are not allowed!!!
ABOLA = 'A Bola'

# load configuration from config.txt
configs = {}
f = open('config.txt', 'r')
for line in f.readlines():
    line = line.replace('\n', '')
    if not line.startswith('#') and line != '':
        temp = line.split('=')
        configs[temp[0]] = temp[1]

# set download paths
root_dir = configs['root_dir']
if not configs['share_src'].lower() == 'true':
    root_dir += configs[ABOLA]

if not os.path.exists(root_dir):
    os.makedirs(root_dir)


## get last cover downloaded
listCovers = os.listdir(root_dir)

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

print ("[{}] Downloading A Bola newspaper front pages...".format(datetime.datetime.now()))

## get the curent date
today = datetime.date.today()
if today == lastDate:
	print("Nothing new. No covers to download....")
	exit()

i = 7 # the abola newspaper only allow us to backward 7 days
while(today > lastDate and i > 0):

	print ("Downloading A Bola newspaper's front page of " + str(today) + "...", end=" ")
	sys.stdout.flush()

	# build the URL of the cover link
	url = 'http://www.abola.pt/' + G_DAYS_OF_WEEK[today.weekday()] + '/wfotosdia/wdiag.jpg'

	# create desdination filename 'YYYYMMDD.jpeg'
	filename = str(today).replace("-", "") + "_" + ABOLA.replace(' ', '_') + ".jpeg"

	# create destination file
	f = open(root_dir + filename, 'wb')

	# download image and write it HDD
	f.write(urllib.request.urlopen(url).read())
	f.close()

	print ("done!")

	# done, lets go back one more day
	today -= timedelta(days=1)
	i -=1

print ("[{}] done!".format(datetime.datetime.now()))

