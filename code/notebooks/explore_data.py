'''
script to explore the data a little bit
'''
import utils


# load each line of the data
data = open('../data/cmudict.dict').readlines()

# convert to word/sequence pairs:
splitted = [i.replace('\n', '').split(' ') for i in data]
word_seq_pairs = {i[0]: i[1:] for i in splitted}

# get largest subsequence of two words
word1 = 'tickle'
word2 = 'follicle'
substring = utils.longest_common_substring(word_seq_pairs[word1], word_seq_pairs[word2])
print(substring)