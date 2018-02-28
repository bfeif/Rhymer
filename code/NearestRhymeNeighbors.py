import numpy as np
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
				 metric='minkowski',
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


	def fit(self, X):
		X = X
		return self._fit(X)

	def somefunction(self):
		return 1