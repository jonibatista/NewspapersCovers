#!/Library/Frameworks/Python.framework/Versions/3.3/bin/python3.3
import urllib.request
import datetime
from bs4 import BeautifulSoup

root_dir='/Users/jbatista/Pictures/newspapers/'
sports='sports/'
news='news/'
abola='A Bola'
record='Record'
jogo='O Jogo'

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

print ("[{}] Downloading the today's nespapers covers...".format(datetime.datetime.now()))
for key in urls:
    # create destination filename 'YYYYMMDD_newspapper.jpeg'
    today = datetime.date.today()
    filename = str(today).replace("-", "") + "_" + key.replace(' ', '_') + ".jpeg"

    path = root_dir
    if key == abola or key == record or key == jogo:
        path += sports
    else:
        path += news

    # create destination file
    f = open(path + filename, 'wb')

    # download image and write it HDD
    f.write(urllib.request.urlopen(urls[key]).read())

    f.close()

    print ('Download complete: ' + str(key))

print ("done!")

