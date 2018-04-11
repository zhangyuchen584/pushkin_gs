# -*- coding: utf-8 -*-
__author__ = "Yuchen"
__aim__ = 'rank top sentences in one topic'
__testCase__ = "../test/test_rankingTFIDF.py"

from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
import sys
import argparse
import numpy as np
from termcolor import colored
from sklearn.metrics.pairwise import cosine_similarity
import operator
sys.path.append(r"../..")
from pushkin_gs.sum import tfidf_contentWords

class TFIDF(object):
    def __init__(self, train_data, contentWords, topN, targCorpus):
        """
        :param train_data: in 'tfidf_contentWords.py' file. after processing step, return a  'targData' dataset, use it to train sentence_tfidf_score
        :param contentWords: in 'tfidf_contentWords.py' file. get 'contentWords' for each topic
        :param topN: N sentence to summary the doc
        :param targCorpus: return top N sentence from init corpus
        """
        self.train_data = train_data
        self.contentWords = contentWords
        self.topN = topN
        self.targCorpus = targCorpus

    def SentRankTFIDF(self):
        """
        :return: tfidfArray: [[0.12, 0.99, 0.24]
                              [0.4, 0.3, 0.4, 0.33, ..]...]
        """

        """#tfidf
        #根据bag of words的原理计算corpus的词频矩阵，把每个句子(即矩阵的每一行)看做一个vector，计算每个vector(句子)在全部corpus中的tfidf值，每个句子的tfidf值是矩阵的每个行向量
        """
        print ("func: SentRankTFIDF")

        # convert corpus to term(word)_vectors
        vectorizer = CountVectorizer()
        # calculate appear times for each word
        term_freq_matrix = vectorizer.fit_transform(self.train_data)
        # get all terms(words) from corpus
        termList = vectorizer.get_feature_names()
        # 将词频矩阵term_freq_matrix统计成TF-IDF值
        # calculate tfidf value for each sentence using term_freq_matrix
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(term_freq_matrix)
        # tfidf[i][j] is sentence[i]'s tfidf value
        # 查看数据结构 tfidf[i][j]表示i类文本中的tf-idf权重
        tfidfArray = tfidf.toarray()
        # print (tfidf.toarray())


        """#claculate sentence score
        ##only summing tfidf values where the words belong to contentWords##
        根据上面求得的sentence tfidf矩阵(tfidfArray)，加和求每一行(每个句子)的tfidf value, 
        不是全部相加，只是把代表content words的值加起来
        Finally, 每个句子的tfidf分数除以整个文章tfidf总分数，即是该句子的ranking(sentRanking[i] = sentValueList[i]/docTfidfScore)
        """

        # content words in each sentence
        contWoEachSent = [[w for w in self.contentWords if w in sent.lower().split()]
                       for sent in self.train_data]
        # content words index(termList) in each sentence
        contWoIndex = [[[termList.index(w)] for w in self.contentWords if w in sent.lower().split()]
                       for sent in self.train_data]
        print (' content words in each sentence',contWoEachSent,'\n','content words index in each sent',contWoIndex)

        # calculate tfidf value for each sentence, return a score list for all sentence(sentValueList)
        sentValueList = []
        for i,index in enumerate(contWoIndex):
            sentValue = sum(tfidfArray[i,index])
            sentValueList.append(float(sentValue))
        print (' sentValueList',sentValueList)

        # sentence ranking #normalization
        sentRanking = [value/max(sentValueList) for value in sentValueList]

        sentRanking = np.array(sentRanking)
        # print ("sentRanking",sentRanking[np.argsort(-sentRanking)])

        topNSent = [self.targCorpus[rank] for rank in np.argsort(-sentRanking)[:-1]]
        topNProcess = [self.train_data[rank] for rank in np.argsort(-sentRanking)[:-1]]

        dicTop = np.c_[sentRanking[np.argsort(-sentRanking)[:-1]],topNProcess,topNSent]

        print (' sent with score',dicTop[:2])
        print ("....")
        print ('-'*200)
        self.dicTop = dicTop
        return dicTop

    # calculate Similarity score each sentence with whole documents
    def calculateSimilarity(self, sentence, doc):
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


    def MMR(self, dicTopSentence):
        print("func: MMR")

        ##惩罚因子
        ##score = a * i[2] + (1 - a) * similarity(i[sentence], (i - 1)[sentence])
        n = 20 * len(self.targCorpus) / 100
        alpha = 0.5
        summarySet = []
        temset = []
        while n > 0:
            mmr = {}
            for sentence in dicTopSentence:
                if not sentence[1] in temset:
                    # print (self.calculateSimilarity(sentence[1],summarySet))
                    mmr[sentence[1]] = alpha * float(sentence[0]) - (1 - alpha) * self.calculateSimilarity(sentence[1], temset)
            selected = max(mmr.items(), key=operator.itemgetter(1))[0]
            # print (selected)
            temset.append(selected)
            n -= 1

        for temsents in temset:
            summarySet.append(''.join([sent[2] for sent in self.dicTop if sent[1] == temsents]))


        print ('\nTotal Sentences', colored(len(self.train_data),'red'))
        print ('Top', colored(len(summarySet),'red') ,'sentences:')
        for sent in enumerate(summarySet):
            print (sent)
        print ("**"*100)
        return summarySet

def main():
    """
        python rankingTFIDF.py --topic bmt_2.txt --contentWordNumber 100
        :predefine:
        :--allData: X.txt file, which contain (target1 polarity1\tsent1\ntarget2 polarity2\tsent2\n )
        :--topic: bmt_0.txt, which contain (sent1 sent2 ... sentn)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', default='', help="target topic")
    parser.add_argument('--contentWordNumber', default='', help="threshold for content Word Number")
    parser.add_argument('--returnNSents', default='', help="top N sentences")
    args = parser.parse_args()
    targetTweets, targData, contentWords = tfidf_contentWords.main()

    for key in targData:
        trainData = targData[key].split(".")

    # init corpus: finally return top N sentence from init corpus
    for key in targetTweets:
        initCorpus = targetTweets[key].split('\n')

    instance = TFIDF(trainData, contentWords, args.returnNSents, initCorpus)
    topSent = instance.SentRankTFIDF()
    instance.MMR(topSent)



if __name__ == '__main__':
    """
    python rankingTFIDF.py --topic bmt_2.txt --contentWordNumber 100 (--returnNSents 2)
    """
    main()