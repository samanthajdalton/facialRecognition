from __future__ import division
from facepp import API, File
import json
from pandas.io.json import json_normalize
import pandas as pd
import time
import cv2
from pandas import compat
from findtools.find_files import (find_files, Match)
import codecs
from pandas import compat
import ast, json
from pandas import DataFrame
import yaml
import numpy as np
import pymongo

import simplejson
import tmpFB
import time
import codecs
import ast

api = API('b40d3ea28aad1f2c2aa939dec674abff', '_gYS77zBAL0U60gtv_qebqwRmRWJz4c1')


conn = pymongo.MongoClient()
db = conn.faces
collection = db.urlClubPhotos
collection1 = db.facesMeta


def get_face_meta_url(api):
    counter = 0
    facesMeta = pd.DataFrame()
    facesMetaList = []
    noFaces = []
    cursor1 = collection.find({'state': 0})
    
    for record in cursor1:
        
        counter += 1  
        try:
            result = api.detection.detect(url = record['urlOfImage'],  attribute='pose,age,gender,race,smiling')
            r_dump = json.dumps(result)
            result2 = yaml.safe_load(r_dump)

            if counter % 100 == 0:
                print('still going')

            if len(result['face']) > 0:
                collection.update({'urlOfImage': record['urlOfImage']}, {'$set': {'state': 1}})
                z = collection.find({},  {'state':1, '_id':0})
                for face in result['face']:
                    tempDict = face
                    tempDict['url'] = record['urlOfImage']
                    tempDict['img_width'] = result['img_width']
                    tempDict['img_height'] = result['img_height']
                    tempDict['svid'] = record['svid']
                    tempDict['fbPageName'] = record['fbPageName']
                    collection1.insert(tempDict)               
                    facesMetaList.append(tempDict)

            if len(result['face']) == 0:
                noFaces.append(record['urlOfImage'])
                collection.update({'urlOfImage': record['urlOfImage']}, {'$set': {'state': 1}})
        except Exception as x:
            print('e')
            if x.code == 432:
                failedLinks.append(record['urlOfImage'])
            elif x.code == 502:
                time.sleep(60)
                print(idx)
            else:
                print(record['urlOfImage'])
            failedLinks.append(record['urlOfImage'])    
            
get_face_meta_url(api)            