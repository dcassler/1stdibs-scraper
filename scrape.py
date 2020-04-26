import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

url = 'https://www.1stdibs.com/furniture/seating/club-chairs/pair-of-modern-style-club-chairs/id-f_18808132/'
response = requests.get(url)
print(response)
result = BeautifulSoup(response.text, "html.parser")




# Grab all images in carousel
pictureGroup = result.find('ul', attrs={'data-tn':'carousel-list-wrapper'})
parsedGroup = pictureGroup.contents

# Parse pictures to array
i = 0
picList = [] # Array of all pictures
while i < len(parsedGroup):
    temp = str(pictureGroup.contents[i].find('img'))
    if temp != 'None':
        x = temp.split('src="')
        picURL = x[1].replace('"/>', '')
        #print(picURL)
        #print(i, '-0--------')
        picList.append(picURL)
    i += 1

# Fix first entry to grab largest picture
parsedOutput = picList[0].split(', ')

fixedFirst = parsedOutput[len(parsedOutput) - 1].split(' ')
finalFirst = fixedFirst[0]

picList[0] = finalFirst



