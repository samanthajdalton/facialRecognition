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

import simplejson
import tmpFB
import time
import codecs
import ast

api = API('b40d3ea28aad1f2c2aa939dec674abff', '_gYS77zBAL0U60gtv_qebqwRmRWJz4c1')


def get_face_meta_url(found_files, api, club):

    facesMeta = pd.DataFrame()
    facesMetaList = []
    noFaces = []

    for idx, imgpath in enumerate(found_files):
        try:
            result = api.detection.detect(url = imgpath,  attribute="pose,age,gender,race,smile")
            r_dump = json.dumps(result)
            result2=yaml.safe_load(r_dump)
            if idx % 100 == 0:
                print('still going')
            if len(result['face']) > 0:
                for face in result['face']:
                    tempDict = face
                    tempDict['url'] = imgpath
                    tempDict['img_width'] = result['img_width']
                    tempDict['img_height'] = result['img_height']
                    facesMetaList.append(tempDict)
                    temp = json_normalize(tempDict)
                    facesMeta = pd.concat([facesMeta, temp], axis=0, ignore_index = True)
            if len(result['face']) == 0:
                noFaces.append(imgpath)
        except:        
            time.sleep(60)
            print('sleeping at' + str(idx))

    facesMeta.to_pickle("./data/facesMeta" + club + "_" + time.strftime("%Y%m%d")  + ".pkl")

    return(facesMeta, facesMetaList)
