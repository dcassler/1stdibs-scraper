import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
import shutil
import os
from tqdm import tqdm
import os.path
from os import path

def grabURL(url):

    #url = 'https://www.1stdibs.com/furniture/seating/swivel-chairs/pair-of-barrel-back-swivel-chairs/id-f_18807992/'
    response = requests.get(url)
    result = BeautifulSoup(response.text, "html.parser")
    return result

def grabPicturesFromItem(result, itemType):
    # Grab all images in carousel
    pictureGroup = result.find('ul', attrs={'data-tn':'carousel-list-wrapper'})
    parsedPictureGroup = pictureGroup.contents

    # Parse pictures to array
    i = 0
    picList = [] # Array of all pictures
    picListNames = []
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

    # Download all of the images

    pathname = 'images/' + itemType
    if not os.path.isdir(pathname):
            os.makedirs(pathname)
    for image_url in picList:
        filename = image_url.split("/")[-1] 
        filename = filename.split("?")[0]
        filename = filename.split(".jpg")[0]
        filename = filename.split(".JPG")[0]
        filename += ".jpeg"
        filename = os.path.join(pathname, filename)
        if True != os.path.exists(filename):
            r = requests.get(image_url, stream = True)
            # Check if the image was retrieved successfully
            if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
                with open(filename,'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                
                print('Image sucessfully Downloaded: ',filename)
                picListNames.append(filename)
            else:
                print('Image Couldn\'t be retreived')
        else: 
            print('Image already sucessfully Downloaded: ',filename)
            picListNames.append(filename)
    return picListNames

# Grab Item Details
def grabItemDetails(result):
    dimDetailGroup = result.find('div', attrs={'data-tn':'pdp-spec-dimensions'})
    dimpullOutData = str(dimDetailGroup)
    dimpullOutData = dimpullOutData.split('span>')
    dimensions = [grabHeight(dimpullOutData), grabWidth(dimpullOutData), 
    grabDepth(dimpullOutData), grabSeatHeight(dimpullOutData)]
    # print(dimensions)
    return dimensions
def grabHeight(dimpullOutData):
    tempDimHeight = dimpullOutData[1]
    dimHeight= tempDimHeight.replace('</', '')
    return dimHeight

def grabSeatHeight(dimpullOutData):
    try: 
        tempSeatHeight = dimpullOutData[10]
        dimSeat = tempSeatHeight.replace('</','')
        return dimSeat
    except IndexError:
        return None
def grabWidth(dimpullOutData):
    tempDimWidth = dimpullOutData[4]
    dimWidth = tempDimWidth.replace('</', '')
    return dimWidth

def grabDepth(dimpullOutData):
    try: 
        tempDimDepth = dimpullOutData[7]
        dimDepth = tempDimDepth.replace('</', '')
        return dimDepth
    except: 
        return None




def grabAboutSection(result):
    # About Section: Holds data from the about section to store in each item descripton
    aboutDetailGroup = result.find('span', attrs={'data-tn':'pdp-item-description-content'})
    aboutPullOutData = str(aboutDetailGroup)
    aboutPullOutData = aboutPullOutData.split('>')
    aboutData = aboutPullOutData[1].replace('</span', '')
    return aboutData

def grabPriceDetail(result):
    # Price 
    priceDetailGroup = result.find('span', attrs={'data-tn':'price-amount'})
    pricePullOutData = str(priceDetailGroup)
    pricePullOutData = pricePullOutData.split('>')
    priceData = pricePullOutData[1].replace('</span', '')
    return priceData

def grabSetSize(result):
    # Set Size
    try: 
        setSizeDetailGroup = result.find('div', attrs={'data-tn': 'pdp-spec-sold-as'})
        setSizeDetailGroup = setSizeDetailGroup.find('span', attrs={'data-tn': 'pdp-spec-detail-setSize'})
        setSizePullOutData = str(setSizeDetailGroup)
        setSizePullOutData = setSizePullOutData.split('>')
        setSizeData = setSizePullOutData[2].replace('</span', '')
        return setSizeData
    except: 
        return None

def grabData(url):
    # Feed url of item to get page data
    result = grabURL(url)
    # download photos from result 
    itemType = grabItemType(result)
    pictures = grabPicturesFromItem(result, itemType) 
    dimensions = grabItemDetails(result)
    aboutData = grabAboutSection(result)
    priceData =  grabPriceDetail(result)
    setData = grabSetSize(result)
    
    return [dimensions, aboutData, priceData, setData, pictures]

def grabItemType(result):
    try: 
        setItemType = result.find('ol', attrs={'data-tn': 'breadcrumbs'})
        setItemType = str(setItemType)
        setItemType = setItemType.split('breadcrumb-item')
        setItemType = setItemType[-1].split('/">')
        setItemType = setItemType[1].split('</a')
        itemType = str(setItemType[0])
        return itemType
    except: 
        return None
