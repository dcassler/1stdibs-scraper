import download_item_data
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
# Store page url
# https://www.1stdibs.com/dealers/mid-century-antiques/shop/furniture/


# search for: application/ld+json

def grabStoreResults(addition):

    url = 'https://www.1stdibs.com/dealers/mid-century-antiques/shop/furniture/' + addition
    response = requests.get(url)
    result = BeautifulSoup(response.text, "html.parser")
    return condenseResult(result)

def condenseResult(result):
    neededChunk = result.find('script', attrs={'type':'application/ld+json'})
    neededChunk = str(neededChunk)
    parsedChunkByURL = neededChunk.split('url":"')
    itemPages = []
    for url in parsedChunkByURL:
        url = url.split('"')
        #print('url', url[0])
        itemPages.append(url[0])
    del itemPages[0]
    
    return itemPages

def downloadItems():
    pages = ['', '?page=2', '?page=3', '?page=4', '?page=5']
    i = 0
    for page in pages: 
        result = grabStoreResults(page)
        del result[0]
        
        print(result)
        for item in result: 
            print("Attempting donwload of ", item, '\n')
            print('This is item ', i)
            print(download_item_data.grabData(item))
            i += 1

