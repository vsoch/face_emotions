# Prepare MDS coordinates from emotions similarity matrix for plotting emotions

from sklearn.metrics import pairwise_distances
from sklearn import manifold

emotions = pandas.read_csv('../data/emotion_df.tsv',sep="\t",index_col=0)

# Add pure emotions as coordinates
centers = [[1,0,0,0,0,0,0,0], # anger
           [0,1,0,0,0,0,0,0], # contempt
           [0,0,1,0,0,0,0,0], # disgust
           [0,0,0,1,0,0,0,0], # fear
           [0,0,0,0,1,0,0,0], # happiness
           [0,0,0,0,0,1,0,0], # neutral
           [0,0,0,0,0,0,1,0], # sadness
           [0,0,0,0,0,0,0,1]] # surprise

emotion_labels = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
for i in range(len(centers)):   
    emotions.loc[emotion_labels[i]] = centers[i]

similarities = pandas.DataFrame(pairwise_distances(emotions,metric='euclidean')) # ranges 0 to 1
similarities.index = emotions.index
similarities.columns = emotions.index

mds = manifold.MDS(n_components=3, dissimilarity="precomputed")
results = mds.fit(similarities)
mapping  = pandas.DataFrame(results.embedding_)
mapping.columns = ['x','y','z']
mapping.index = emotions.index
mapping.to_csv('../data/mds_mapping_3d.tsv',sep="\t")
