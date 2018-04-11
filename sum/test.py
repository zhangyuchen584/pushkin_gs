# # import numpy as np
# # # a = np.array()
# #
# # x = np.array([[1,2],[3,4]])
# # # print (x)
# # # print (x[:,1])
# # data = np.array([[1,'absdf'],[4,3],[0,2]])
# # print (data)
# # print (data[:,1])
# # # data = data[data[:,0].argsort()]
# # # print (data)
# #
# # column = np.array([3,5,7])
# # row = np.array([1,2])
# # y = np.row_stack((x,row))
# # print (y)
# # y = np.column_stack((y,column))
# # print(y)
# #
# #
# # stat = np.zeros((5,3), dtype=np.int16)
# # print (stat)
# #
# from nltk.corpus import wordnet as wn
#
# # motorcar=wn.synset('car.n.01')
# # print (motorcar)
# # types_of_motorcar=motorcar.hyponyms()
# # print (types_of_motorcar)
# # types_of_motorcar[26]
# # # Synset('stanley_steamer.n.01')
# # # sorted(
# # #     [lemma.name()
# # #      for synset in types_of_motorcar
# # #      for lemma in synset.lemmas()])
#
# # print (wn.synsets('suv')[0])
#
# # print (wn.synset('sport_utility.n.01').lemma_names())
# #
# # for i in wn.synset('sport_utility.n.01').lemma_names():
# #     print (' '.join(i.split('_')))
#
#
# # synonyms = []
# # antonyms = []
# #
# # for syn in wn.synsets("good"):
# #     for l in syn.lemmas():
# #         synonyms.append(' '.join(l.name().split('_')))
# #
# #
# # print(set(synonyms))
#
# import numpy as np
# docs = np.array([[1,2,3,4,5],[3,4,5,6,7]])
# print (docs)
# print ('--')
# B =[1,2,3,4,5,6,7,28,30,28]
# a = [(28, 50), (30, 42), (30, 50), (28, 30), (42, 50), (28, 42), (43, 50), (28, 43), (30, 3), (10, 43), (10, 50), (10, 28), (42, 43), (15, 17), (4, 15),]
# # a= (28, 43), (30, 43), (10, 43), (10, 50), (10, 28), (42, 43), (15, 17), (4, 15),
# # a = (33, 36), (18, 46), (10, 30), (30, 47), (1, 35), (42, 47), (10, 42), (5, 27), (19, 27), (17, 31)]
# allSents = ()
# for item in a:
#     allSents = allSents+item
# print (allSents)
#
# senGroup = []
# for item in [sent for sent in allSents if sent not in senGroup]:
#     if item not in senGroup:
#         senGroup.append('mark')
#         senGroup.append(item)
#
#     for index in senGroup:
#         for i,j in a :
#             if i==index and j not in senGroup:
#                 senGroup.append(j)
#
#             elif j == index and i not in senGroup:
#                 senGroup.append(i)
#         # print (index)
#
#
# print(senGroup)
#
# group = {}
# num = 0
# list = []
# for i in senGroup:
#     # print (i)
#     if i != 'mark':
#         list.append(i)
#         # print(list)
#     else:
#         group[num] = list
#         num = num +1
#         list = []
#         # print (list)
# group[num] = list
#
# print (group)


#

#  class A(object):
#     def foo(self,x):
#         print ("executing foo(%s,%s)"%(self,x))
#
#     @classmethod
#     def class_foo(cls,x):
#         print ("executing class_foo(%s,%s)"%(cls,x))
#
#     @staticmethod
#     def static_foo(x):
#         print ("executing static_foo(%s)"%x)
#
# a=A()
# A.static_foo(1)
# a.static_foo('hi')


from pyrouge import Rouge155
from pprint import pprint
#
# ref_texts = {'A': "Poor nations pressurise developed countries into granting trade subsidies.",
#              'B': "Developed countries should be pressurized. Business exemptions to poor nations.",
#              'C': "World's poor decide to urge developed nations for business concessions."}
# summary_text = "Poor nations demand trade subsidies from developed nations."
#
#
# rouge = Rouge155()
# score = rouge.score_summary(summary_text, ref_texts)
# pprint(score)
from sklearn.base import BaseEstimator


# def cosine_similarity(X, Y=None, dense_output=True):
#     """Compute cosine similarity between samples in X and Y.
#     Cosine similarity, or the cosine kernel, computes similarity as the
#     normalized dot product of X and Y:
#         K(X, Y) = <X, Y> / (||X||*||Y||)
#     On L2-normalized data, this function is equivalent to linear_kernel.
#     Read more in the :ref:`User Guide <cosine_similarity>`.
#     Parameters
#     ----------
#     X : ndarray or sparse array, shape: (n_samples_X, n_features)
#         Input data.
#     Y : ndarray or sparse array, shape: (n_samples_Y, n_features)
#         Input data. If ``None``, the output will be the pairwise
#         similarities between all samples in ``X``.
#     dense_output : boolean (optional), default True
#         Whether to return dense output even when the input is sparse. If
#         ``False``, the output is sparse if both input arrays are sparse.
#         .. versionadded:: 0.17
#            parameter ``dense_output`` for dense output.
#     Returns
#     -------
#     kernel matrix : array
#         An array with shape (n_samples_X, n_samples_Y).
#     """
#     # to avoid recursive import
#
#     X, Y = check_pairwise_arrays(X, Y)
#
#     X_normalized = normalize(X, copy=True)
#     if X is Y:
#         Y_normalized = X_normalized
#     else:
#         Y_normalized = normalize(Y, copy=True)
#
#     K = safe_sparse_dot(X_normalized, Y_normalized.T, dense_output=dense_output)
#
#     return K
import os
import re
import sys
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import operator
#--------------------==================#--------------------==================

# create stemmer
# f = open(r'/Users/newuser/Desktop/stopwords.txt')
# with open('/Users/newuser/Desktop/Text-Summarization-MMR-master/news_data.txt', "r", encoding='utf-8') as file:
# 	texts = file.readline()
# 	for i in file:
# 		print (i)



import sys
sys.path.append(r"../..")
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator
from pushkin_gs.sum.Processing import process


def calculateSimilarity(sentence, doc):
	if doc == []:
		return 0
	vocab = {}
	for word in sentence[:-1].split():
		vocab[word] = 0


	docInOneSentence = ''
	for t in doc:
		docInOneSentence += (t + ' ')
		for word in t[:-1].split():
			vocab[word] = 0
	cv = CountVectorizer(vocabulary=vocab.keys())
	docVector = cv.fit_transform([docInOneSentence])
	sentenceVector = cv.fit_transform([sentence])
	return cosine_similarity(docVector, sentenceVector)[0][0]

with open('/Users/newuser/Desktop/Text-Summarization-MMR-master/news_data.txt', "r", encoding='utf-8') as file:
	texts = file.readlines()

sentences = []
originalSentenceOf = {}

import time
start = time.time()

#clean data
clean = [process(i) for i in texts]
setClean = set(clean)

#calculate Similarity score each sentence with whole documents
scores = {}
for data in clean:
	temp_doc = setClean - set([data])
	score = calculateSimilarity(data,list(temp_doc))
	scores[data] = score
print (scores)

# calculate MMR

n = 20 * len(texts) / 100

alpha = 0.5
summarySet = []
while n > 0:
	mmr = {}
	# kurangkan dengan set summary
	for sentence in scores.keys():
		if not sentence in summarySet:
			mmr[sentence] = alpha * scores[sentence] - (1 - alpha) * calculateSimilarity(sentence, summarySet)
	# print (mmr)
	selected = max(mmr.items(), key=operator.itemgetter(1))[0]

	summarySet.append(selected)
	n -= 1

import numpy as np
from sklearn.preprocessing import normalize


name = ['l','h']
age = [12,34]
dic = {}
a = dict(zip(name,age))
print (a)