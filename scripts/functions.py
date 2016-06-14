import ImageFile
import urllib
import numpy
import json
import cv2

## FUNCTIONS #########################################################################

def has_face(face_cascade,image_url):
    imgdata = url_to_image(image_url)
    gray = cv2.cvtColor(imgdata, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(faces) > 0:
        return True
    return False


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


def parse_results(results,images):
    for result in results:
        if result['pk'] not in images:
            images[result['pk']] = result
    return images


def save_json(json_obj,output_file):
    filey = open(output_file,'wb')
    filey.write(json.dumps(json_obj, sort_keys=True,indent=4, separators=(',', ': ')))
    filey.close()
    return output_file

