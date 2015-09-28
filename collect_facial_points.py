import cv2
from facepp import API, File
import pandas as pd
import time
from pandas.io.json import json_normalize

from pandas import compat


compat.PY3 = True

def create_crops_points(found_files, outfile_path):

    api = API('b40d3ea28aad1f2c2aa939dec674abff', '_gYS77zBAL0U60gtv_qebqwRmRWJz4c1')

    allFaces = []
    allFaces2 = pd.DataFrame()
    facesMeta = pd.DataFrame()
    print(len(found_files))
    for idn,found_file in enumerate(found_files):
        imgpath = found_file
        print(imgpath)
        print(idn)
        result = api.detection.detect(img = File(found_file),  attribute="pose,age,gender,race")
        print(result)
        if len(result['face']) > 0:
            if facesMeta.empty == 'True':
                facesMeta = json_normalize(result['face'])
            else:
                facesMeta = pd.concat([facesMeta,json_normalize(api.detection.detect(img = File(found_file))['face'])],axis=0)


        allfacePts = []
        if len(result['face']) > 0:

            print(str(len(result['face']))+" faces found")

            for idx,face in enumerate(result["face"]):

                r2 = api.detection.landmark(face_id = face["face_id"], type = "83p")
                faces2 = json_normalize(r2["result"][0]["landmark"])
                faces2['face_id'] =  face["face_id"]

                image = cv2.imread(imgpath)

                if allFaces2.empty == 'True':
                    allFaces2 = faces2
                else:
                    allFaces2 = pd.concat([allFaces2,faces2],axis=0)
                
                #Mark key facial points on photo
                for key,value in r2["result"][0]["landmark"].iteritems():
                    pid=key
                    cx=value["x"]/100*result['img_width']
                    cy=value["y"]/100*result['img_height']
                    cv2.circle(image,(int(cx),int(cy)),2,(0,0,255),1)


                #crop image based on key points
                startx=max(0,((face["position"]["center"]["x"]-0.6*face['position']['width'])/100)*result['img_width'])
                starty = max(((face["position"]["center"]["y"]-1.25*face['position']['height'])/100)*result['img_height'],0)
                endx =((face["position"]["center"]["x"]+0.6*face['position']['width'])/100)*result['img_width']
                endy = ((face["position"]["center"]["y"] + 0.8*face['position']['height'])/100)*result['img_height']


                cropped = image[starty:endy, startx:endx]
                cv2.imshow("cropped", cropped)
                printid=outfile_path + face["face_id"] +".jpeg"
                cv2.imwrite(printid, cropped)
                time.sleep(2)
                cv2.destroyAllWindows()
                
                time.sleep(1)
                #faces2.merge(pd.DataFrame(face["face_id"]))
                r3 = r2["result"][0]["landmark"]

                print(allFaces2)
                for key,value in r3.iteritems():
                    facePts = {}
                    facePts["face_id"] = face["face_id"]
                    facePts["position"] = key.encode("ascii","ignore")
                    for k,v in value.iteritems():
                        if k == u'x':
                            facePts["x"] = v
                        if k == u'y':
                            facePts["y"] = v
                    allfacePts.append(facePts)

            finalFaces = pd.DataFrame(allfacePts)
            cv2.destroyAllWindows()

        return [allFaces2, finalFaces, facesMeta]