import numpy as np
import pandas as pd
import utils
import random
import scipy.stats as stats
from scipy.sparse import lil_matrix
import matplotlib.pyplot as plt
import utils
import progressbar
from sklearn.neighbors import NearestNeighbors


class NearestRhymeNeighbors(NearestNeighbors):
	'''Nearest Neighbors sklearn class inherited for easier querying nearest neighbors by word

	Attributes
	----------

	Methods
	-------

	'''

	def __init__(self,
				 n_neighbors=5, 
				 radius=1.0,
				 algorithm='auto',
				 leaf_size=30,
				 metric='precomputed',
				 p=2,
				 metric_params=None,
				 n_jobs=1,
				 **kwargs):
		super(NearestRhymeNeighbors, self).__init__(n_neighbors=n_neighbors, 
													radius=radius,
													algorithm=algorithm,
													leaf_size=leaf_size,
													metric=metric,
													p=p,
													metric_params=metric_params,
													n_jobs=n_jobs
													)
		self.word_sim_matrix = None


	def fit(self, phone_dictionary, rhyme_similarity_threshold=.5):
		'''Fits the nearest neighbors

		First uses the passed in word-phone dictionary to create and set a similarity matrix/dataframe,
		then fits on the word similarity matrix.

		Parameters
		----------
		phone_dictionary : dict
			Keys are words (strings), values are phone sequences (tuples).

		Returns
		-------
		self

		'''
		# get and set the word similarity dataframe
		self.word_sim_matrix = self.set_word_sim_matrix(phone_dictionary, rhyme_similarity_threshold=rhyme_similarity_threshold)
		
		# fit on the values of the dataframe
		X = self.word_sim_matrix.values
		# print(self.word_sim_matrix)
		# print(X)
		return self._fit(X)


	def set_word_sim_matrix(self, phone_dictionary, rhyme_similarity_threshold=.5):
		'''Make and return a word similarity matrix

		'''
		dist = lil_matrix((len(phone_dictionary), len(phone_dictionary)), dtype=np.bool)
		bar = progressbar.ProgressBar()
		# print(phone_dictionary.items())
		k_v1 = phone_dictionary.items()
		k_v2 = phone_dictionary.items()
		for k1, v1 in bar(k_v1):
			for k2, v2 in k_v2:
				d = utils.get_rhyme_similarity(v1[1], v2[1])>rhyme_similarity_threshold
				# print('---')
				# print(d)
				dist[v1[0], v2[0]] = d
		# print(dist)
		# print(dist.toarray())
		df = pd.SparseDataFrame(data=dist.toarray(), index=[k_v[0] for k_v in k_v1], columns=[k_v[0] for k_v in k_v2])
		# df = pd.SparseDataFrame(dist)
		print(df)
		return df


	def kneighbors(self, word_X=None, n_neighbors=None, return_distance=True):
		'''Gets the k nearest neighbors for a query word

		Parameters
		----------
		word_X : str, np.array
			The input word. If np.array, then input should be the word's vector representation. If string, vector 
			representation will be retrieved for the word.
		n_neighbors : int
			Number of neighbors to get (default is the value
			passed to the constructor).
		return_distance : boolean, optional. Defaults to True.
			If False, distances will not be returned
		
		Returns
		-------
		dist : array
			Array representing the lengths to points, only present if
			return_distance=True
		ind : array
			Indices of the nearest points in the population matrix.
		'''
		if type(word_X)==str:
			X = self.get_word_array(word_X)
		else:
			X = word_X
		return super(NearestRhymeNeighbors, self).kneighbors(X=X, n_neighbors=n_neighbors, return_distance=return_distance)


	def get_word_array(self, word):
		return word