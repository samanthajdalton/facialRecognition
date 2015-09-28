
import cv2
import sys
from findtools.find_files import (find_files, Match)
import json
import exifread
from facepp import API, File
import os
import json


api = API('b40d3ea28aad1f2c2aa939dec674abff', '_gYS77zBAL0U60gtv_qebqwRmRWJz4c1')

faceCascade = cv2.CascadeClassifier('/Users/dev01/Documents/Docs/haarcascade_frontalface_default.xml')

sh_files_pattern = Match(filetype='f', name='im*.jpeg')
found_files = find_files(path='/Users/dev01/Downloads', match=sh_files_pattern)

for found_file in found_files:

    imgpath = found_file 

    image = cv2.imread(imgpath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    if len(faces) > 0:
        print "found faces"
        
        result = api.detection.detect(img = File(found_file))
        #print repr(result)
        #data = json.loads(str(result))
        print json.dumps(result)
        #print result

    else:
        print "no faces"
        #delete image
