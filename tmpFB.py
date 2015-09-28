import json 
import time
import requests
import urllib, urllib2
from lxml import html
from lxml import etree
import locale
import random
import pymongo
from selenium import webdriver  
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Connect to mongo
conn = pymongo.MongoClient()
db = conn.faces
collection = db.urlClubPhotos

def getPicUrls(fbPageName, toScroll):
    driver = webdriver.Chrome()
    driver.get('https://www.facebook.com/' + fbPageName + '/photos_stream?')

    url = 'https://www.facebook.com/' + fbPageName
    r = requests.get(url)
    facebookID = r.text.split('"pageID":"')[1].split('"')[0]
       
   
    db.drop_collection('temp')
    db.create_collection('temp')
    #Get thumbnails of images    
    scroll = True
    while scroll:
        a = len(listOfUrls)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        for i in driver.find_elements_by_xpath("//*[@class='uiMediaThumb _6i9 uiMediaThumbMedium']"):
            tempDict = {}
            tempDict['thumbUrl'] = i.get_attribute("href")
            r = requests.get(thumbUrl)
            tree = html.fromstring(r.text)
            for htmlObject in tree.xpath("//img[@class='fbPhotoImage img']"): 
                tempDict['urlOfImage'] = htmlObject.attrib['src']
                listOfImageUrls.append(urlOfImage)
            for htmlObject2 in tree.xpath("//abbr"):  
                tempDict['albumTitle'] = htmlObject2.attrib['title']
                tempDict['uploadTime'] = htmlObject2.attrib['data-utime']
                tempDict['fbPageName'] = fbPageName
            collection.insert(tempDict)
            
            scroll = toScroll

        b = len(listOfUrls)

        
        if a == b:
            scroll = False

#getPicUrls('opiumbarcelona', False)