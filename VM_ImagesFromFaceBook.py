import json 
from pyvirtualdisplay import Display
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
from selenium.webdriver.common.keys import Keys


#Connect to mongo
conn = pymongo.MongoClient()
db = conn.faces
collection = db.urlClubPhotos

display = Display(visible=0, size=(800, 600))
display.start()

#setup selenium webdriver
service_log_path = "/home/dm/chromedriver.log"
service_args = ['--verbose', '--display :99']
driver = webdriver.Chrome('/usr/local/bin/chromedriver',
        service_args=service_args,
        service_log_path=service_log_path)

#Set toScroll = False for testing & fbPageName is name of club's fb page
def getPicUrls(fbPageName, toScroll):
    #driver = webdriver.Chrome()
    driver.get('https://www.facebook.com/' + fbPageName + '/photos_stream?')
    listOfImageUrls = []
    listOfUrls = []
    pg = 0
    url = 'https://www.facebook.com/' + fbPageName
    r = requests.get(url)
    facebookID = r.text.split('"pageID":"')[1].split('"')[0]
    #print r.headers
    #print r.text.encode('utf-8')
    try:
        svid = '5|' + r.text.encode('utf-8').split('actorid":"')[1].split('"')[0]
	print svid
    except:
        svid = ''
        print "couldn't get id of facebook page"       
    #Get thumbnails of images    
    scroll = True
    while scroll and pg <= 40:
        a = len(listOfUrls)
        pg += 1
    	print(fbPageName + str(pg))
    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
   	for i in driver.find_elements_by_xpath("//*[@class='uiMediaThumb _6i9 uiMediaThumbMedium']"):
       	    try:
	    	tempDict = {}
            	tempDict['thumbUrl'] = i.get_attribute("href")
	    	tempDict['_id'] = tempDict['thumbUrl']
	    	tempDict['svid'] = svid
	    	tempDict['state'] = 0
            	listOfUrls.append(tempDict['thumbUrl'])
            	r = requests.get(tempDict['thumbUrl'])
            	tree = html.fromstring(r.text)
	   	for htmlObject in tree.xpath("//img[@class='fbPhotoImage img']"): 
            	    tempDict['urlOfImage'] = htmlObject.attrib['src']
            	    listOfImageUrls.append(tempDict['urlOfImage'])
            	for htmlObject2 in tree.xpath("//abbr"):  
             	    tempDict['albumTitle'] = htmlObject2.attrib['title']
            	    tempDict['uploadTime'] = htmlObject2.attrib['data-utime']
            	    tempDict['fbPageName'] = fbPageName
            	collection.insert(tempDict)
            except:
		None

        scroll = toScroll
        b = len(listOfUrls)
        
        if a == b:
            scroll = False



#Get club pics

#clubs = ['opiumbarcelona', 'PachaBarcelona', 'shokobarcelona', 'SalaApolo', 'salarazzmatazz', 'mojitoclubbcn', 'CDLCBarcelona', 
clubs = ['GrupoArena']

for club in clubs:
    getPicUrls(club,True)
