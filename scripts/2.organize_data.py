# Subset data to things we need, obtain additional info about things

import json
import re

# Read in emotions json data, get airtable credentials
emotions = json.load(open("data/loc_emotions.json","rb"))
print "Found %s picture with emotion scores!" %(len(emotions))

# Whittle down to fields that we need for application
emotion_columns = ['anger','contempt','disgust','fear',
                   'happiness','neutral','sadness','surprise']
columns = ['title','creator','created_date','url_thumbnail','url_full','url_square',
           'url_info','collections','medium','created']

# We will have a data frame of image meta data, emotions, subject tags, and dates
image_df = pandas.DataFrame(columns=columns)
subject_df = pandas.DataFrame()
dates_df = pandas.DataFrame()
emotion_df = pandas.DataFrame(columns=emotion_columns)

for image_uid,image in emotions.iteritems():
    
    # Emotions
    emotion_df.loc[image_uid,image['scores'].keys()] = image['scores'].values() 

    # Subjects
    subjects = image['image']['subjects']
    
    # Parse dates from subjects
    dates = [x.split('--')[-1].replace(".",'') for x in subjects if re.search("[0-9]{4}-[0-9]{4}",x.split('--')[-1])]
    dates = numpy.unique(dates).tolist()
    dates_df.loc[image_uid,dates] = 1

    # This will get highest level of subjects
    subjects = [x.split('--')[0].lower() for x in subjects]
     
    # turn medium_brief into features (subject tag)
    # STOPPED Here - figure out how to split this by looking at many,
    # then parse image meta data with columns
    image['image']['medium']

    subject_df.loc[image_uid,subjects] = 1

    # Finally, image meta data
    image_df.loc[image_uid,columns]    
   
    
    
    


