from flask import Flask, render_template, request, jsonify
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
        self.mapping = pandas.read_csv('data/mds_mapping_euclidean.tsv',sep="\t") # columns [x,y]
        self.mapping.columns = ['uid','x','y']

# Start application
app = EmotionServer(__name__)

# Views ##############################################################################################

@app.route("/")
def index():
    '''Generate kmeans clustering for all data'''

    # Use the known labels to get assignment groups
    mapping = app.mapping.copy()
 
    # The last 7 are our emotions
    lookup = [{"id":mapping.uid[x],"color":app.colors[app.assignments[x]]} for x in mapping.index[len(mapping.index)-len(app.centers):]]
    mapping['colors'] = [app.colors[x] for x in app.assignments.tolist()]
    return render_template("index.html",coords=mapping.to_json(orient="records"),
                                        lookup=lookup)

@app.route("/login",methods=["POST","GET"])
def login():
    '''login is the first view seen after login'''
    
    if request.method == "POST":
        account = int(request.form["account_id"])
        result = base_login(account)
        if result["success"] == True:
            return render_template("home.html",log=result["log"],
                                               message=result["message"],
                                               account_id=result["id"])  
        else:
            return render_template("index.html",message=result["message"])
    else:
        message = "You must log in first before viewing account home."
    return render_template("index.html",message=message)
    
if __name__ == "__main__":
    app.debug = True
    app.run()
