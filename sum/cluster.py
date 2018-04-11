"""
ask for advise online:
https://codereview.stackexchange.com/questions/151908/sentences-clustering-affinity-propagation-cosine-similarity-python-sciki
"""
import argparse
import sys
import numpy as np
import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity
sys.path.append(r"../..")
from pushkin_gs.support.calculate_eachTopicSents import topicSents
from pushkin_gs.sum.Processing import process


parser = argparse.ArgumentParser()
parser.add_argument('--dataFolder', default='', help="Tw", action='store', nargs='+')
parser.add_argument('--threshold', default='', help="Tw", action='store', nargs='+')
args = parser.parse_args()
data = topicSents(args.dataFolder, args.threshold)



punctuation_map = dict((ord(char), None) for char in string.punctuation)
stemmer = nltk.stem.snowball.SpanishStemmer()

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize)


# print (tfidf.toarray())

def get_clusters(sentences):
    tf_idf_matrix = vectorizer.fit_transform(sentences)

    #dot product
    similarity_matrix = (tf_idf_matrix * tf_idf_matrix.T).A
    # print (similarity_matrix)

    # similarity_matrix[similarity_matrix<0.03] = 0

    for i in similarity_matrix:
        pass
        # print ([w for w in i if w > 0.05])

    affinity_propagation = AffinityPropagation(affinity="precomputed", damping=0.98999,preference = 0,convergence_iter=5000)
    affinity_propagation.fit(similarity_matrix)
    labels = affinity_propagation.labels_
    cluster_centers = affinity_propagation.cluster_centers_indices_
    tagged_sentences = zip(sentences, labels)
    clusters = {}

    for sentence, cluster_id in tagged_sentences:
        clusters.setdefault(sentences[cluster_centers[cluster_id]], []).append(sentence)

    return clusters


# target = ['bmt_2','bookout_2','tekong_0','platoon_2','ord_2','ippt_0','ord_0','enlistment_2']
target = ['ns_2']


for itarg in target:
    print ('-'*100)
    print ('\n\n',itarg)
    matrix = np.arange(len(data[itarg].split('\n'))).reshape(len(data[itarg].split('\n')), 1)
    rawSents = []
    sents = []
    for index in range(len(data[itarg].split('\n'))):
        sents.append(process(data[itarg].split('\n')[index]))
        rawSents.append(data[itarg].split('\n')[index])
    matrix = np.c_[matrix,rawSents,sents]
    matrix = np.delete(matrix,-1,axis=0)
    # print (matrix[:,2])


    delSent = []

    for i in range(len(matrix[:,2])):
        for j in range(i+1,len(matrix[:,2])):
            senti = matrix[i, 2].split()
            sentj = matrix[j, 2].split()
            intersection = [val for val in senti if val in sentj]
            wordMatchSame = len(intersection)/min(len(senti),len(sentj))
            if wordMatchSame > 0.9:
                ## print (i,j,len(senti),len(sentj))
                if len(senti)<len(sentj):
                    delSent.append(i)
                    break
                else:
                    delSent.append(j)
    # print (list(set(delSent)))
    matrix = np.delete(matrix, list(set(delSent)), axis=0)


    # clusters = get_clusters(matrix[:,2])
    # print()
    # print (itarg)
    # for cluster in clusters:
    #     print(cluster, ':')
    #     for element in clusters[cluster]:
    #         print('  - ', element)

    clusters = get_clusters(matrix[:,2])

    for cluster in clusters:
        for i in range(len(matrix[:,2])):
            # print (matrix[i,2])
            if matrix[i,2] == cluster:
                print()
                # print (matrix[i,1]) #print cluster center
                rank = []
                for element in clusters[cluster]:
                    for j in range(len(matrix[:, 2])):
                        if matrix[j, 2] == element:
                            # print ('  - ',matrix[j, 1])
                            rank.append(matrix[j,1])
                rank.sort(key=lambda s: len(s))
                for senrank in rank:
                    # print ('  - ',senrank)
                    print (senrank)

