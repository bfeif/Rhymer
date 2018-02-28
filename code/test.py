from NearestRhymeNeighbors import NearestRhymeNeighbors
import numpy as np
import random

# samples = np.array([[0,0,2], [0,0,0], [0,0,1], [1,1,1]])
# # neigh = NearestNeighbors(2, .4)
# neigh = NearestRhymeNeighbors(2, .4)
# neigh.fit(samples)
# dist, ind = neigh.kneighbors(np.array([0,0,.1]).reshape(1,-1))
# print(samples[ind])



# load data
data = open('../data/cmudict.dict').readlines()
# splitted = [i.replace('\n', '').split(' ') for i in data]
splitted = random.sample([i.replace('\n', '').split(' ') for i in data], 20)
word_seq_pairs = {i[0]: (index, i[1:]) for index, i in enumerate(splitted)}

# create nearest neighbors object
nn = NearestRhymeNeighbors(n_neighbors=2, radius=.2, metric='precomputed')
nn.fit(word_seq_pairs, rhyme_similarity_threshold=.4)