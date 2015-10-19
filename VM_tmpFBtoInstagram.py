import json 
import time
import requests
import urllib, urllib2
from lxml import html
from lxml import etree
import locale
import random

def getFBtoInstagramUrls(fbPageName):
    #Get FB place id
    url = 'https://www.facebook.com/' + fbPageName
    r = requests.get(url)
    facebookID = r.text.split('"pageID":"')[1].split('"')[0]

    instagramAPIUrl = 'https://api.instagram.com/v1/locations/search?facebook_places_id={0}&client_id=1b724eef0ecc4bd58e63cab65576bec5'

    url = instagramAPIUrl.format(facebookID)
    r = requests.get(url)
    data = json.loads(r.text)
    instagramID = data['data'][0]['id']
    instagramMediaUrl = 'https://api.instagram.com/v1/locations/{0}/media/recent?client_id=1b724eef0ecc4bd58e63cab65576bec5'
    
    url = instagramMediaUrl.format(instagramID)

    r = requests.get(url)
    data = json.loads(r.text)
    

    allImageUrls = []

    #Grabbing image urls for std resolution pics    
    for item in data['data']:
        imageUrl = item['images']['standard_resolution']['url']

        allImageUrls.append(imageUrl)
        

    loopThroughPages = True

    while loopThroughPages:

        if data['pagination']:
            nextPageUrl = data['pagination']['next_url']
            r = requests.get(nextPageUrl)
            data = json.loads(r.text)

            for item in data['data']:
                imageUrl = item['images']['standard_resolution']['url']
                allImageUrls.append(imageUrl)
                with open('./data/imageUrlList_FB2instagram_' + fbPageName + '_' + facebookID + '.txt','w') as filename:
                    filename.write(str(allImageUrls))
                
        else:
            loopThroughPages = False

    return allImageUrls
    

#print facebookID
