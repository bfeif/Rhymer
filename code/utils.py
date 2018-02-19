'''
some utilities before this becomes a class
'''

def is_rhyme(word1, word2):
	'''
	Function that checks if two words rhyme or not
	For use
	'''
	return True


def parse_line(line):
	'''
	Reads line from dict file and returns a data record from it of as a dictionary of the form {word, sequence}
	'''
	return {}


def longest_common_substring(s1, s2):
	m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
	longest, x_longest = 0, 0
	for x in range(1, 1 + len(s1)):
		for y in range(1, 1 + len(s2)):
			if s1[x - 1] == s2[y - 1]:
				m[x][y] = m[x - 1][y - 1] + 1
				if m[x][y] > longest:
					longest = m[x][y]
					x_longest = x
			else:
				m[x][y] = 0
	return s1[x_longest - longest: x_longest]


def get_rhyme_similarity(word1, word2, dist_metric='default'):
	'''
	gets longest matching subsequence, and uses its length to get a rhyme similarity for the two words

	Parameters
	----------
	word1 (list)
		sequence of phones
	word2 (list)
		sequence of phones
	dist_metric (string)

	Returns
	-------
	int
		value is in [0,1]. 1 means very similar, 0 means very dissimilar 
	'''
	sub = longest_common_substring(word1, word2)
	rhyme_similarity = 9999
	if dist_metric=='default':
		rhyme_similarity = 2 * len(sub) / (len(word1) + len(word2))
	return rhyme_similarity