import numpy as np
import utils
import random
import scipy.stats as stats
from scipy.sparse import lil_matrix
import matplotlib.pyplot as plt
import utils
import progressbar
from sklearn.neighrbos import NearestNeighbors


class NearestRhymeNeighbors(NearestNeighbors):
	'''Nearest Neighbors sklearn class inherited for easier querying nearest neighbors by word

	Attributes
	----------

	Methods
	-------

	'''

	def __init__(self):
		pass