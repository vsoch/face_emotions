from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api
from sklearn.cluster import KMeans
from numpy.random import choice
from datetime import datetime
import requests
import numpy
import pandas
import json
import re


# SERVER CONFIGURATION ##############################################
class EmotionServer(Flask):

    def __init__(self, *args, **kwargs):
        super(EmotionServer, self).__init__(*args, **kwargs)

        # load data on start of application
        self.emotions = pandas.read_csv('data/emotion_df.tsv',sep="\t",index_col=0)
        self.subjects = json.load(open('data/subjects.json','rb'))
        self.meta = pandas.read_csv('data/image_df.tsv',sep="\t",index_col=0)
        self.dates = json.load(open('data/dates.json','rb'))
        
        # Use Kmeans to cluster, cosine distance to generate graph/plot
        self.centers = [[1,0,0,0,0,0,0,0], # anger
                        [0,1,0,0,0,0,0,0], # contempt
                        [0,0,1,0,0,0,0,0], # disgust
                        [0,0,0,1,0,0,0,0], # fear
                        [0,0,0,0,1,0,0,0], # happiness
                        [0,0,0,0,0,1,0,0], # neutral
                        [0,0,0,0,0,0,1,0], # sadness
                        [0,0,0,0,0,0,0,1]] # surprise

        self.labels = ["anger","contempt","disgust","fear","happiness",
                       "neutral","sadness","surprise"]
        self.colors = ["#E60F0D","#E6550D","#E6910D","#1D7B13","#3182BD",
                       "#777","#1D1772","#8F0E72"]

        # Add core emotions to data frame 
        for i in range(len(self.centers)):   
            self.emotions.loc[self.labels[i]] = self.centers[i]

        self.cluster = KMeans(n_clusters=len(self.centers),init=numpy.array(self.centers))
        self.cluster.fit(self.emotions)
        self.assignments = self.cluster.labels_
        self.mapping = pandas.read_csv('data/mds_mapping.tsv',sep="\t") # columns [x,y]

# Start application
app = EmotionServer(__name__)
api = Api(app)

# API VIEWS ##########################################################################################

class apiIndex(Resource):
    """apiIndex
    Main view for REST API to display all available emotion data
    """
    def get(self):
        emotion_json = app.emotions.to_dict(orient="records")
        return emotion_json

class apiQueryDates(Resource):
    """apiQueryDates
    return a list of ids for emotion photos between a range of dates
    """
    def get(self, start_year, end_year):
        date_range = range(start_year,end_year)
        subset = [app.dates[str(x)] for x in date_range if str(x) in app.dates]
        subset = numpy.unique([item for sublist in subset for item in sublist]).tolist()
        return {"ids": subset}
              
# Add all resources
api.add_resource(apiIndex,'/api/emotions')
api.add_resource(apiQueryDates,'/api/dates/<int:start_year>/<int:end_year>')

# Views ##############################################################################################

@app.route("/")
def index():
    '''Generate kmeans clustering for all data'''

    # Use the known labels to get assignment groups
    mapping = app.mapping.copy()
 
    # The last 7 are our emotions
    lookup = [{"id":mapping.uid[x],"color":app.colors[app.assignments[x]]} for x in mapping.index[len(mapping.index)-len(app.centers):]]

    # Get min and max dates
    date_keys = app.dates.keys()
    date_keys.sort()
    min_date = "%s-01-01" %date_keys[0]
    max_date = "%s-12-25" %date_keys[-1]

    mapping['colors'] = [app.colors[x] for x in app.assignments.tolist()]

    return render_template("index.html",coords=mapping.to_json(orient="records"),
                                        lookup=lookup,
                                        dates=app.dates,
                                        min_date=min_date,
                                        max_date=max_date)    
if __name__ == "__main__":
    app.debug = True
    app.run()
