#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3

import json
import os
import datetime
from datetime import timedelta
import urllib.request
import sys
from bs4 import BeautifulSoup
import string


## DEF CONSTANTS
G_SRC_FOLDER =  "/Users/jbatista/Pictures/record/"
G_ROWS_NUMBER = 3
G_COLUMNS_NUMBER = 4
G_LIMIT_MAX_PAGES = 10
G_TOTAL_COVERS_PER_PAGE = G_ROWS_NUMBER * G_COLUMNS_NUMBER



## BEGIN

# Each html page have X newspaper covers, where x = G_COLUMNS_NUMBER * G_ROWS_NUMBER.
# This is represented by a html table with G_ROWS_NUMBER rows and G_COLUMNS_NUMBER columns.
# I use a Matrices to represent that table, where each cell will contain the cover ID.
# All position are initiated with the value 0. This means that at this position we'll not download the cover.
coversPerPage = [ [ 0 for i in range(G_COLUMNS_NUMBER) ] for j in range(G_ROWS_NUMBER) ]

## get last cover downloaded
try:
    listCovers = os.listdir(G_SRC_FOLDER) 
except:
    print("Error! ", G_SRC_FOLDER, " - ", sys.exc_info()[0])
    exit()

if len(listCovers) == 0:
    # directory is empty. We have to make a full download since page G_LIMIT_MAX_PAGES
    # starting at X days ago... Full download.
    lastDownload = datetime.date.today() - timedelta(days=(G_LIMIT_MAX_PAGES*G_TOTAL_COVERS_PER_PAGE-1))
    startPage = G_LIMIT_MAX_PAGES
else:
    lastDownload = ""
    listCovers.sort()
    ## get the date of the last cover
    for i in listCovers[-1]:
            if i.isdigit():
                    lastDownload = lastDownload + i

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
    exit()

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
        # we just need to download the html when the page change, not to every cover in the current page
        isPageChange = bool(0)

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

    # Download the cover in the table(row, column) position
    #print (day, "-", coversPerPage[row][column])
    
    print ("Downloading record newspaper cover of " + str(day) + "...", end=" ")
    sys.stdout.flush()

    # build the URL of the cover link
    #coverUrl = 'http://www.record.xl.pt/capas/default.aspx?page=' + str(currentPage+1) + '&content_id=' + str(coversPerPage[row][column]) 

    # create desdination filename 'YYYYMMDD.jpeg'
    filename = str(day).replace("-", "") + ".jpeg"
   
    # create destination file
    #f = open(G_SRC_FOLDER + filename, 'wb')

    # download image and write it HDD
    #f.write(urllib.request.urlopen(coverUrl).read())
    #f.close()

    print ("ok!")


    # All covers of the current page are downloaded. It's time to change to the next page
    if coversInThisPage == 0:
        isPageChange = bool(1)
        coversPerPage = [ [ 0 for i in range(G_COLUMNS_NUMBER) ] for j in range(G_ROWS_NUMBER) ]


# PRINT VAlUES - DEBUG        
#for i in range(totalPages):
    #temp = pages[i]
    #for j in range(3):
        #for x in range(4):
            #print ("[", i, "]", temp[j][x])

