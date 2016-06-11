#####################################################################
# Use Microsoft Emotions API to categorize emotions, upload tags to
# Airtable database. The user can provide an image on command line

import requests
import numpy
import json
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

if not os.path.exists(".secret"):

    print """Please write Microsoft Emotion API key into a file called .secret in this directory!
          See: https://www.microsoft.com/cognitive-services/en-us/emotion-api
          """

    sys.exit()

# Read in emotion API key
api_key = open(".secret").readlines()[0].strip("\n")

# Define image source, these have been filtered for faces and size
images = json.load(open("loc_faces.json","rb"))

# If the user doesn't want to save to database
if json_save == True:
    emotions = dict()

for image in images:

    image_title = image['title']
    image_url = "http:%s" %image['image']['full'] 

    # Microsoft Emotion API URL to request data
    emo_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
    headers = {'Content-Type':'application/json','Ocp-Apim-Subscription-Key':api_key}
    body = {'url':image_url}
    response = requests.post(emo_url, headers=headers, data=json.dumps(body))

    if response.status_code == 200:
        face_emotions = response.json()[0]
        face_emotions["image"] = image

        if json_save == True:
            emotions[image['pk']] = face_emotions 
            # And here we will have option to save to relational graphical db!
    
