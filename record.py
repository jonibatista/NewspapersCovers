#!/usr/bin/python
import json
import os
import datetime
from datetime import timedelta
import urllib.request

## DEF CONSTANTS
G_SRC_FOLDER = "C:/Users/INOV2073/Documents/record/" #"/Users/jbatista/Pictures/abola/"
G_ROWS_NUMBER = 3
G_COLUMNS_NUMBER = 4
G_TOTAL_PAGES = 10
G_TOTAL_COVERS_PER_PAGE = G_ROWS_NUMBER * G_COLUMNS_NUMBER


# Each html page have X newspaper covers, where x = G_COLUMNS_NUMBER * G_ROWS_NUMBER.
# This is represented by a html table with G_ROWS_NUMBER rows and G_COLUMNS_NUMBER columns.
# I use a Matrices to represent that table, where each cell will contain the cover ID.
# All position are initiated with the value 0. This means that at this position we'll not download the cover.
coversPerPage = [ [ 0 for i in range(G_COLUMNS_NUMBER) ] for j in range(G_ROWS_NUMBER) ]

## get last cover downloaded
listCovers = os.listdir(G_SRC_FOLDER) 

if len(listCovers) == 0:
    # directory is empty. We have to make a full download since page G_TOTAL_PAGES
    # starting at X days ago...
    lastDownload = datetime.date.today() - timedelta(days=(G_TOTAL_PAGES*G_TOTAL_COVERS_PER_PAGE-1))
    startPage = G_TOTAL_PAGES
else:
    lastDownload = ""
    listCovers.sort()
    ## get the date of the last cover
    for i in listCovers[-1]:
            if i.isdigit():
                    lastDownload = lastDownload + i

    year = abs(int(lastDownload)/10000) #YYYY.mmdd
    month = int(lastDownload)%10000 #yyyy.MMDD
    month = int(month)/100 #MM.dd
    day = int(lastDownload)%100 #yyyymm.DD

    lastDownload = datetime.date(int(year), int(month), int(day))
    
# starting loop until all covers are downloaded
lackingDays = (datetime.date.today() - lastDownload).days
for i in reversed(range(lackingDays)):

    # Current page number
    currentPage = int(i/G_TOTAL_COVERS_PER_PAGE)+1
    row = int((G_TOTAL_COVERS_PER_PAGE*currentPage-i)/4)
    column = 0
    print ("page:", currentPage, " row", row, " column:", column )


for d1 in range(3):
    for d2 in range(4):
        coversPerPage[d1][d2]= d1*4 + d2
print (coversPerPage)

