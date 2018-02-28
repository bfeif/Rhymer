import numpy as np
from sklearn.neighbors import NearestNeighbors

samples = np.array([[0,0,2], [0,0,0], [0,0,1], [1,1,1]])
neigh = NearestNeighbors(2, .4)
neigh.fit(samples)
dist, ind = neigh.kneighbors(np.array([0,0,.1]).reshape(1,-1))

print(samples[ind])
