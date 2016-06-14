# Subset data to things we need, obtain additional info about things

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

# We will keep track of dates and subjects
date_list = []
subject_list = []

# Function to parse dates from subjects list
def get_dates(subjects):
    dates = [x.split('--')[-1].replace(".",'').split(',')[0] for x in subjects if re.search("[0-9]{4}-[0-9]{4}",x.split('--')[-1])]
    dates = numpy.unique(dates).tolist()
    # We only want to match date ranges in format [XXXX-XXXX]
    dates = [re.findall("[0-9]{4}-[0-9]{4}",x)[0] for x in dates if len(re.findall("[0-9]{4}-[0-9]{4}",x)) > 0]
    return dates

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
        [date_list.append(d) for d in dates if d not in date_list]
        # This will get highest level of subjects
        subjects = [x.split('--')[0].lower() for x in subjects]
    else:
        subjects = []
     
    # turn medium_brief into features (subject tag)
    # format seems to be type: material : size
    medium_tags = [tag.strip().replace(".","") for tag in image['image']['medium'].split(":")]
    subjects = numpy.unique(subjects + medium_tags).tolist()
    [subject_list.append(s) for s in subjects if s not in subject_list]

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

del image_df
del emotion_df

# Now generate subject and dates data frames
subject_df = pandas.DataFrame(columns=subject_list)
dates_df = pandas.DataFrame(columns=date_list)

count = 1
for image_uid,image in emotions.iteritems():
    print "Parsing %s of %s" %(count,len(emotions))

    # Subjects
    subjects = image['image']['subjects']
    
    # Parse dates from subjects, add to list
    if subjects != None:
        dates = get_dates(subjects)
        dates_df.loc[image_uid,dates] = 1
        # This will get highest level of subjects
        subjects = [x.split('--')[0].lower() for x in subjects]
    else:
        subjects = []
     
    # turn medium_brief into features (subject tag)
    # format seems to be type: material : size
    medium_tags = [tag.strip().replace(".","") for tag in image['image']['medium'].split(":")]
    subjects = numpy.unique(subjects + medium_tags).tolist()
    subject_df.loc[image_uid,subjects] = subjects
    
    count+=1    

subject_df.to_csv('../data/subjects_df.tsv',sep="\t",encoding='utf-8')
dates_df.to_csv('../data/dates_df.tsv',sep='\t')
