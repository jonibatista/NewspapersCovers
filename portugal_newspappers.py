#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4
import urllib.request
import datetime
import os
from bs4 import BeautifulSoup

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
if configs['share_src'].lower() == 'true':
    is_share_folder = True
else:
    is_share_folder = False

# get request html page
response = urllib.request.urlopen('http://www.tvtuga.com').read()
soup = BeautifulSoup(response)
html = soup.find(id='subfooter-inner')

# urls' covers
urls = {}
for newspapper in html.find_all('div', class_='img'):
    desc = newspapper.find('div', class_='desc')
    url = newspapper.a.get('href')
    urls[desc.text] = url

print ("[{}] Downloading the today's newspapers front pages...".format(datetime.datetime.now()))
for key in urls:
    # create destination filename 'YYYYMMDD_newspapper.jpeg'
    today = datetime.date.today()
    filename = str(today).replace("-", "") + "_" + key.replace(' ', '_') + ".jpeg"

    path = root_dir
    if not is_share_folder:
        try:
            path += configs[key]
        except:
            print("Error when downloading the ", filename)
            continue

    # create destination file
    if not os.path.exists(path):
        os.makedirs(path)
    f = open(path + filename, 'wb')

    # download image and write it HDD
    f.write(urllib.request.urlopen(urls[key]).read())

    f.close()

    print ('Download complete: ' + str(key))

print ("[{}] done!".format(datetime.datetime.now()))

