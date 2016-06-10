
from repofish import save_json
import requests
import time

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
save_json(images,"loc_images.json")
