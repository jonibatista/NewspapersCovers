#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3

import json
import os
import datetime
from datetime import timedelta
import urllib.request
import sys


## DEF CONSTANTS
G_SRC_FOLDER =  "/Users/jbatista/Pictures/record/"
G_ROWS_NUMBER = 3
G_COLUMNS_NUMBER = 4
G_TOTAL_PAGES = 10
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
    print("Error! ", sys.exc_info()[0])
    exit()

if len(listCovers) == 0:
    # directory is empty. We have to make a full download since page G_TOTAL_PAGES
    # starting at X days ago... Full download.
    lastDownload = datetime.date.today() - timedelta(days=(G_TOTAL_PAGES*G_TOTAL_COVERS_PER_PAGE-1))
    startPage = G_TOTAL_PAGES
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
        lastDownload = datetime.date.today() - timedelta(days=(G_TOTAL_PAGES*G_TOTAL_COVERS_PER_PAGE-1))
        startPage = G_TOTAL_PAGES
    

# starting loop until all covers are downloaded
lackingDays = (datetime.date.today() - lastDownload).days
for i in reversed(range(lackingDays)):

    currentPage = int(i/G_TOTAL_COVERS_PER_PAGE) # Current page number
    coversInThisPage = i - G_TOTAL_COVERS_PER_PAGE*currentPage# total covers to download in this current page
    row = int(coversInThisPage / G_COLUMNS_NUMBER)
    column = coversInThisPage - row * G_COLUMNS_NUMBER
    #print ("page:", currentPage +1, "[", row, "] [", column, "]")

    coversPerPage[row][column] = datetime.date.today() - timedelta(days=i)

    temp = coversPerPage[row][column]
    print ("page:", currentPage +1, "[", row, "] [", column, "] => ", temp)


