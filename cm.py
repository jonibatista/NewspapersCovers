#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3
import os
import datetime
from datetime import timedelta
import urllib.request
import sys
from bs4 import BeautifulSoup
import string


## DEF CONSTANTS
G_MAX_COVERS = 15
G_PARAM_DIR = "root_dir"
G_PARAM_SHARED="share_src"
G_PARAM_SRC="src"
G_FILENAME_SUFFIX = "cm" # number are not allowed!!!

## BEGIN
print ("Starting the Correio da Manhã covers update on ", datetime.datetime.now())

# The Correio da Manhã provides the lastest G_MAX_COVERS newspapers covers
coversUrl = [ 0 for i in range(G_MAX_COVERS)]

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
    srcFolder = params[G_PARAM_DIR] + "/" + "cm/"

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


if len(listCovers) == 0:
    # directory is empty. We have to make a full download since page G_LIMIT_MAX_PAGES
    # starting at X days ago... Full download.
    lastDownload = datetime.date.today() - timedelta(days=(G_MAX_COVERS-1))
else:
    listCovers.sort()
    for n in reversed(range(len(listCovers))):
        lastDownload = ""
        
        for i in listCovers[n]:
            if i.isdigit():
                lastDownload = lastDownload + i

        if G_FILENAME_SUFFIX in listCovers[n]: 
            break

    try:
        year = abs(int(lastDownload)/10000) #YYYY.mmdd
        month = int(lastDownload)%10000 #yyyy.MMDD
        month = int(month)/100 #MM.dd
        day = int(lastDownload)%100 #yyyymm.DD

        lastDownload = datetime.date(int(year), int(month), int(day))
    except:
        # We aren't able to determinate what was the last cover downloaded.
        # starting at X days ago... Full download.
        lastDownload = datetime.date.today() - timedelta(days=(G_MAX_COVERS-1))
    

# starting loop until all covers are downloaded
lackingDays = (datetime.date.today() - lastDownload).days

if lackingDays < 1:
    print("Nothing new. No covers to download....")

# We must change the page
url = "http://www.cmjornal.xl.pt/capa.aspx?channelid=00000020-0000-0000-0000-000000000020"

# Create http request to get the new page source html content
html = urllib.request.urlopen(url).read()

# load the page into the DOM parser
soup = BeautifulSoup(html)

# parse the html to extract the covers IDs
td = soup.findAll("td", {"class": "stk_ccc"}) # get image thumbnails container

for n in range(len(td)):
    # date of the current cover
    date = datetime.date.today() - timedelta(days=n)

    uri = td[n].a['href'] # web page uri of the day today()-n
    
    url = "http://www.cmjornal.xl.pt/" + uri

    # load page html to memory
    html = urllib.request.urlopen(url).read()
    
    # parse the html to extract the image url
    soup = BeautifulSoup(html)

    html = soup.find("div", {"class": "blockPageNews"})

    # image uri of the cover today()-n
    uri = html.img['src']

    print ("Downloading record newspaper cover of " + str(date) + "...", end=" ")
    sys.stdout.flush()
  
    # create desdination filename 'YYYYMMDD.jpeg'
    filename = str(date).replace("-", "") + "_" + G_FILENAME_SUFFIX + ".jpeg"
   
    # create destination file
    f = open(srcFolder + filename, 'wb')

    # download image and write it HDD
    f.write(urllib.request.urlopen(uri).read())
    f.close()

    print ("ok!")

print ("Correio da Manhã covers was successfully updated on ", datetime.datetime.now())
# EDN OF SCRIPT