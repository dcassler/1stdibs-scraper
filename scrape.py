import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re

# Data used: 
# picList = array of pictures
# dimInch, dimCen, dimensions of obj 
# aboutData = about





url = 'https://www.1stdibs.com/furniture/seating/club-chairs/pair-of-modern-style-club-chairs/id-f_18808132/'
response = requests.get(url)
print(response)
result = BeautifulSoup(response.text, "html.parser")




# Grab all images in carousel
pictureGroup = result.find('ul', attrs={'data-tn':'carousel-list-wrapper'})
parsedPictureGroup = pictureGroup.contents

# Parse pictures to array
i = 0
picList = [] # Array of all pictures
while i < len(parsedPictureGroup):
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

# Grab Item Details

# Dimensions
dimDetailGroup = result.find('div', attrs={'data-tn':'pdp-spec-dimensions'})
dimpullOutData = str(dimDetailGroup)
dimpullOutData = dimpullOutData.split('span>')
tempDimInch = dimpullOutData[1]
tempDimCen = dimpullOutData[4]
dimInch = tempDimInch.replace('</', '')
dimCen = tempDimCen.replace('</', '')
#print(dimInch, dimCen)

# About
aboutDetailGroup = result.find('span', attrs={'data-tn':'pdp-item-description-content'})
aboutPullOutData = str(aboutDetailGroup)
aboutPullOutData = aboutPullOutData.split('>')
aboutData = aboutPullOutData[1].replace('</span', '')
print(aboutData)
