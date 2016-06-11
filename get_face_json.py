from functions import url_to_image, getsizes, has_face
import requests
import time
import cv2

## STEP 1: Search for images using face terms ##########################################

search_terms = ["face","portrait","man","woman"]

current_page = 1
last_page = 2
images = dict()
for search_term in search_terms:
    print "Parsing term %s..." %(search_term)
    library_congress_url = "http://loc.gov/pictures/search/?q=%s&fo=json" %(search_term)
    response = requests.get(library_congress_url)
    if response.status_code == 200:
        response = response.json()
        if "pages" in response:
            last_page = response['pages']['total']    
        for page in range(current_page,last_page+1):
            print "Page %s of %s" %(page,last_page)
            time.sleep(0.5)
            url = "http://www.loc.gov/pictures/search/?q=%s&sp=%s&fo=json" %(search_term,page)
            response = requests.get(url)
            if response.status_code == 200:
                response = response.json()
                if "results" in response:
                    results = response['results']
                    images = parse_results(results,images)
        
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


# Save the json to file
save_json(images,"loc.json")


## STEP 2: Subset to images that likey have faces ######################################

# FaceDetect haar cascade file for opencv
cascade_file = "FaceDetect/haarcascade_frontalface_default.xml"

# Create the haar cascade
face_cascade = cv2.CascadeClassifier(cascade_file)

min_width=300
min_height=300

# Subset to large images with faces
faces = dict()
for image_key,image in images.iteritems():

    image_url = "http:%s" %image['image']['full'] 
    size,dims = getsizes(image_url)
    # Is it big enough?
    if dims[0] <= min_width or dims[1] <= min_height:
        print "Image %s has size %s, skipping!" %(image['title'],dims)
    else:
        if has_face(face_cascade,image_url):
            print "Found face! %s" %(image['title']) 
            faces[image_key] = image


save_json(faces,"loc_faces.json")
