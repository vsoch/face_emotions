# Subset data to things we need, obtain additional info about things

from functions import save_json
import pandas
import json
import re

# Read in emotions json data, get airtable credentials
emotions = json.load(open("data/loc_emotions.json","rb"))
print "Found %s picture with emotion scores!" %(len(emotions))

# Whittle down to fields that we need for application
emotion_columns = ['anger','contempt','disgust','fear',
                   'happiness','neutral','sadness','surprise']
columns = ['title','creator','published_date','url_thumbnail','url_full','url_square',
           'url_info','collections','medium','created']

# We will have a data frame of image meta data, emotions, subject tags, and dates
image_df = pandas.DataFrame(columns=columns)
emotion_df = pandas.DataFrame(columns=emotion_columns)

# Dates and subject should be dictionary
dates_dict = dict()
subjects_dict = dict()

###################################################################################
# FUNCTIONS #######################################################################
###################################################################################

# Function to parse dates from subjects list
def get_dates(subjects):
    dates = [x.split('--')[-1].replace(".",'').split(',')[0] for x in subjects if re.search("[0-9]{4}-[0-9]{4}",x.split('--')[-1])]
    dates = numpy.unique(dates).tolist()
    # We only want to match date ranges in format [XXXX-XXXX]
    dates = [re.findall("[0-9]{4}-[0-9]{4}",x)[0] for x in dates if len(re.findall("[0-9]{4}-[0-9]{4}",x)) > 0]
    return dates

# Function to add uid to each of list of keys in dictionary
def add_to_dict(dictionary,keys,value):
    for key in keys:
        if key not in dictionary:
            dictionary[key] = [value]
        else:
            dictionary[key].append(value)
    return dictionary


###################################################################################
# PARSING #########################################################################
###################################################################################

count = 1
for image_uid,image in emotions.iteritems():

    print "Parsing %s of %s" %(count,len(emotions))

    # Emotions
    emotion_df.loc[image_uid,image['scores'].keys()] = image['scores'].values() 

    # Subjects
    subjects = image['image']['subjects']
    
    # Parse dates from subjects, add to list
    if subjects != None:
        dates = get_dates(subjects)
        dates_dict = add_to_dict(dates_dict,dates,image_uid)

        # This will get highest level of subjects
        subjects = [x.split('--')[0].lower() for x in subjects]
    else:
        subjects = []
     
    # turn medium_brief into features (subject tag)
    # format seems to be type: material : size
    medium_tags = [tag.strip().replace(".","") for tag in image['image']['medium'].split(":")]
    subjects = numpy.unique(subjects + medium_tags).tolist()
    subjects_dict = add_to_dict(subjects_dict,subjects,image_uid)

    # Finally, image meta data
    image_df.loc[image_uid,columns] = [image['image']['title'],
                                       image['image']['creator'],
                                       image['image']['created_published_date'],
                                       "https:%s" %(image['image']['image']['thumb']),
                                       "https:%s" %(image['image']['image']['full']),
                                       "https:%s" %(image['image']['image']['square']),
                                       "https:%s" %image['image']['links']['item'],
                                       ",".join(image['image']['collection']),
                                       image['image']['medium_brief'],
                                       image['image']['created']]
   
    
    count+=1    

# Save the data frames and then free up memory
image_df.to_csv('../data/image_df.tsv',sep="\t",encoding='utf-8')
emotion_df.to_csv('../data/emotion_df.tsv',sep="\t")
save_json(subjects_dict,'../data/subjects.json')
save_json(dates_dict,'../data/dates.json')
