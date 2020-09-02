import requests
from bs4 import BeautifulSoup
import download_item_data
import db_connect
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
    db = db_connect.connection()
    con = db.cursor()
    #con.execute("select * from Item;")
    #x = con.fetchall()
    #print(x)
    pages = ['', '?page=2', '?page=3', '?page=4', '?page=5']
    i = 0
    for page in pages: 
        result = grabStoreResults(page)
        del result[0]
        
        print(result)
        for item in result: 
            print("Attempting donwload of ", item, '\n')
            print('This is item ', i)
            data = download_item_data.grabData(item)
            # Parse out that data into variables to send to database
            y = 0 
            for x in data: 
                print(y)
                print(x)
                print('\n')     
                y += 1
            height = data[0][0]
            print(type(height))
            width = data[0][1]
            depth = data[0][2]
            seatHeight = data[0][3]
            about = data[1]
            print(type(about))
            price = data[2]
            setsize = data[3]
            print(type(setsize))
            if(setsize == None):
                setsize = "NULL"
            pictureList = data[4]
            pictures = ""
            pictures = pictures.join(pictureList)
            print(height, '\n', width, '\n', depth, '\n', about, '\n')
            name = "null"
            itemtype = "null"
           
            #stmt = """INSERT INTO `Item` (`itemID`, `name`, `price`, `height`, `width`, `depth`, `about`, `setsize`, `pictureList`, `itemtype`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""" % (None, name, price, height, width, depth, about, setsize, pictureList, itemtype)
            #stmt = "INSERT INTO `Item` (`itemID`, `name`, `price`, `height`, `width`, `depth`, `about`, `setsize`, `pictureList`, `itemtype`) VALUES (0, 'Did this actually work?',0,0,0,0,0,0,0,0);"
            
            stringTest = ('This is a test')
            print(type(stringTest))
            
            stmt = "INSERT INTO `Item` (`itemID`, `name`, `price`, `height`, `width`, `depth`, `about`, `setsize`, `pictureList`, `itemtype`) VALUES ({}, {}, {}, {}, {}, {}, '{}', {}, '{}', {});".format(0, name, price, height, width, depth, about, setsize, pictures, itemtype)
            con.execute(stmt)
            db.commit() 
            print(data)
            i += 1

downloadItems()