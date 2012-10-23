#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3
import os
import datetime
from datetime import timedelta
import urllib.request
import sys
from bs4 import BeautifulSoup
import string


## DEF CONSTANTS
G_ROWS_NUMBER = 3
G_COLUMNS_NUMBER = 4
G_LIMIT_MAX_PAGES = 10
G_TOTAL_COVERS_PER_PAGE = G_ROWS_NUMBER * G_COLUMNS_NUMBER
G_PARAM_DIR = "root_dir"
G_PARAM_SHARED="share_src"
G_PARAM_SRC="src"
G_FILENAME_SUFFIX = "record" # number are not allowed!!!

## BEGIN
print ("Starting the Record covers update on ", datetime.datetime.now())

# Each html page have X newspaper covers, where x = G_COLUMNS_NUMBER * G_ROWS_NUMBER.
# This is represented by a html table with G_ROWS_NUMBER rows and G_COLUMNS_NUMBER columns.
# I use a Matrices to represent that table, where each cell will contain the cover ID.
# All position are initiated with the value 0. This means that at this position we'll not download the cover.
coversPerPage = [ [ 0 for i in range(G_COLUMNS_NUMBER) ] for j in range(G_ROWS_NUMBER) ]

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
    lastDownload = datetime.date.today() - timedelta(days=(G_LIMIT_MAX_PAGES*G_TOTAL_COVERS_PER_PAGE-1))
    startPage = G_LIMIT_MAX_PAGES
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
        lastDownload = datetime.date.today() - timedelta(days=(G_LIMIT_MAX_PAGES*G_TOTAL_COVERS_PER_PAGE-1))
        startPage = G_LIMIT_MAX_PAGES
    

# starting loop until all covers are downloaded
lackingDays = (datetime.date.today() - lastDownload).days

if lackingDays < 1:
    print("Nothing new. No covers to download....")

isPageChange = bool(1)
for i in reversed(range(lackingDays)):

    currentPage = int(i/G_TOTAL_COVERS_PER_PAGE) # Current page number
    coversInThisPage = i - G_TOTAL_COVERS_PER_PAGE*currentPage# total covers to download in this current page
    row = int(coversInThisPage / G_COLUMNS_NUMBER)
    column = coversInThisPage - row * G_COLUMNS_NUMBER

    #coversPerPage[row][column] = datetime.date.today() - timedelta(days=i)
    day = datetime.date.today() - timedelta(days=i)
    
    if isPageChange:
        # We must change the page
        url = "http://www.record.xl.pt/capas/default.aspx?page=" + str(currentPage + 1)
        # Create http request to get the new page source html content
        html = urllib.request.urlopen(url).read()
        # load the page into the DOM parser
        soup = BeautifulSoup(html)

        # parse the html to extract the covers IDs
        divs = soup.findAll("div", {"class": "CartoonBox cursorPointer"}) # get image thumbnails container
        for n in range(len(divs)):

            # We want the first line of each thumbnail container
            # 1st line: <div> class="CartoonBox cursorPointer" onclick="PagerSetContent(&pageNumber, &coverID)">
            # the cover ID is the 2nd argument of the javascript function 
            line = divs[n].prettify()
            lines = line.split('\n') 
            temp = lines[0].split('PagerSetContent') 
            temp = temp[1].split(', ')
            temp = temp[1].split(")")
            coversPerPage[int(n/G_COLUMNS_NUMBER)][n - int(n/G_COLUMNS_NUMBER) * G_COLUMNS_NUMBER]=temp[0]

        # we just need to download the html when the page change, not to every cover in the current page
        isPageChange = bool(0)

    # Download the cover in the table(row, column) position
    #print (day, "-", coversPerPage[row][column])
    
    print ("Downloading record newspaper cover of " + str(day) + "...", end=" ")
    sys.stdout.flush()

    # build the URL to the render the page that contains the cover's image (size big)
    url = 'http://www.record.xl.pt/capas/default.aspx?page=' + str(currentPage+1) + '&content_id=' + str(coversPerPage[row][column]) 
  
    # load page html to memory
    html = urllib.request.urlopen(url).read()
    
    # parse the html to extract the image url
    soup = BeautifulSoup(html)
   
    coverDiv = soup.find("div", {"class": "capa-grande-container"})
    img = coverDiv.img['src']
    urlImg = 'http://www.record.xl.pt' + str(img)

    # create desdination filename 'YYYYMMDD.jpeg'
    filename = str(day).replace("-", "") + "_" + G_FILENAME_SUFFIX + ".jpeg"
   
    # create destination file
    f = open(srcFolder + filename, 'wb')

    # download image and write it HDD
    f.write(urllib.request.urlopen(urlImg).read())
    f.close()

    print ("ok!")


    # All covers of the current page are downloaded. It's time to change to the next page
    if coversInThisPage == 0:
        isPageChange = bool(1)
        coversPerPage = [ [ 0 for i in range(G_COLUMNS_NUMBER) ] for j in range(G_ROWS_NUMBER) ]

print ("Record's covers was successfully updated on ", datetime.datetime.now())
# EDN OF SCRIPT