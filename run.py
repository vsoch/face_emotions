#####################################################################
# Use Microsoft Emotions API to categorize emotions, upload tags to
# Airtable database. The user can provide an image on command line

from numpy.random import choice
import ImageFile
import requests
import urllib
import numpy
import json
import cv2
import sys
import os


## VARIABLES #########################################################################


# Minimum width and height to use
min_width = 300
min_height = 300

# FaceDetect haar cascade file for opencv
cascade_file = "FaceDetect/haarcascade_frontalface_default.xml"

# Create the haar cascade
face_cascade = cv2.CascadeClassifier(cascade_file)


## FUNCTIONS #########################################################################

# Function to get size of images
# http://stackoverflow.com/questions/7460218/get-image-size-without-downloading-it-in-python
def getsizes(url):
    # get file size *and* image size (None if not known)
    file = urllib.urlopen(url)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None


# METHOD #1: OpenCV, NumPy, and urllib
# http://www.pyimagesearch.com/2015/03/02/convert-url-to-image-with-python-and-opencv/
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

# Does the emotion api key file exist?
# Emotion - Preview	30,000 transactions per month, 20 per minute.

if not os.path.exists(".secret"):

    print """Please write Microsoft Emotion API key into a file called .secret in this directory!
          See: https://www.microsoft.com/cognitive-services/en-us/emotion-api
          """

    sys.exit()

# Read in emotion API key
api_key = open(".secret").readlines()[0].strip("\n")

# Define image source
images = json.load(open("loc_images.json","rb"))

# Find an image!
found_image = False
while found_image == False:
    image_pk = choice(images.keys())
    image = images[image_pk]
    image_title = image['title']
    image_url = "http:%s" %image['image']['full'] 
    size,dims = getsizes(image_url)
    # Is it big enough?
    if dims[0] <= min_width or dims[1] <= min_height:
        print "Image %s has size %s, skipping!" %(image_title,dims)
    else:
        # Do we detect a face?
        imgdata = url_to_image(image_url)
        gray = cv2.cvtColor(imgdata, cv2.COLOR_BGR2GRAY)
        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray,
                                              scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(30, 30),
                                              flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(faces) > 0:
            found_image = True
            print "Found big enough image with %s faces: %s, with size %s." %(len(faces),image_title,dims)

# Microsoft Emotion API URL to request data
emo_url = 'https://api.projectoxford.ai/emotion/v1.0/recognize'
headers = {'Content-Type':'application/json','Ocp-Apim-Subscription-Key':api_key}
body = {'url':image_url}
response = requests.post(emo_url, headers=headers, data=json.dumps(body))

if response.status_code == 200:
    face_emotions = response.json()[0]
    face_emotions["image"] = image

# And here we will do for more images, save data, do diabolical things... :)
