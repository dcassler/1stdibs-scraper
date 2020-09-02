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
            
            height = data[0][0]
       
            width = data[0][1]
            depth = data[0][2]
            seatHeight = data[0][3]
            about = data[1]
         
            price = data[2]
            setsize = data[3]
      
            if(setsize == None):
                setsize = "NULL"
            pictureList = data[4]
            pictures = ""
            pictures = pictures.join(pictureList)
            print('Height', height, '\n', 'width', width, '\n', 'depth', depth, '\n', about, '\n')
            if(depth == None):
                depth == 'NULL'
            name = data[6]
            itemtype = data[5]
            print(type(itemtype))
            
            
            stmt = "INSERT INTO `Item` (`itemID`, `name`, `price`, `height`, `width`, `depth`, `about`, `setsize`, `pictureList`, `itemtype`) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(0, name, price, height, width, depth, about, setsize, pictures, itemtype)
            con.execute(stmt)
            db.commit() 
            print(data)
            i += 1

downloadItems()