#####################################################################
# Use Microsoft Emotions API to categorize emotions, upload tags to
# Airtable database. The user can provide an image on command line

import requests
import pandas
import numpy
import json
import time
import cv2
import sys
import os


## VARIABLES #########################################################################

database_file = ".database_credentials"
json_save = True
if os.path.exists(database_file):
    json_save = False

# Does the emotion api key file exist?
# Emotion - Preview	30,000 transactions per month, 20 per minute.
limit = 30000

if not os.path.exists(".secret"):

    print """Please write Microsoft Emotion API key into a file called .secret in this directory!
          See: https://www.microsoft.com/cognitive-services/en-us/emotion-api
          """

    sys.exit()

# Microsoft Emotion API URL to request data
api_key = open(".secret").readlines()[0].strip("\n")
emo_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
headers = {'Content-Type':'application/json','Ocp-Apim-Subscription-Key':api_key}

# Define image source, these have been filtered for faces and size
images = json.load(open("loc_faces.json","rb"))

emotions = dict()


count=0
for image_pk,image in images.iteritems():

    if count < limit and image_pk not in emotions:
        image_title = image['title']
        print "Parsing %s of %s: %s" %(count,limit,image_title)
        image_url = "http:%s" %image['image']['full'] 
        body = {'url':image_url}
        response = requests.post(emo_url, headers=headers, data=json.dumps(body))

        if response.status_code == 200 and response.text != '[]':
            face_emotions = response.json()[0]
            face_emotions["image"] = image
            emotions[image_pk] = face_emotions 

        count+=1
        time.sleep(3.0) # only 30 per minute
