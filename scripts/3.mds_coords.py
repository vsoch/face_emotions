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

# try 2d and 3d MDS
dims = [2,3]
column_names = ['x','y','z']
for dim in dims:
    mds = manifold.MDS(n_components=dim, dissimilarity="precomputed")
    results = mds.fit(similarities)
    mapping  = pandas.DataFrame(results.embedding_)
    mapping.columns = column_names[0:dim]
    mapping.index = emotions.index
    mapping.to_csv('../data/mds_mapping_%sd.tsv' %(dim),sep="\t")

# TSNE might be better, we just want good groupings, not necessarily to preserve distances
tsne = manifold.TSNE(n_components=2, random_state=0)
result = pandas.DataFrame(tsne.fit_transform(emotions))
result['uid'] = emotions.index
result.columns = ['x','y','uid']
result.to_csv('../data/mds_mapping.tsv',sep="\t")
