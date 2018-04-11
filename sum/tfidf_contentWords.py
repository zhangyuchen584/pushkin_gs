# -*- coding: utf-8 -*-
__author__ = "Yuchen"
__aim__ = 'calculate TFIDF value for each topic in all documents(6k tweets) and return content words'

import argparse
import sys
import math
from textblob import TextBlob as tb
import json
sys.path.append(r"../..")
from pushkin_gs.definition import ROOT
from pushkin_gs.sum.Processing import process


class loadData(object):
    def __init__(self,database,targetData,contentWordNumber):
        self.database = database
        self.targetData = targetData
        self.contentWordNumber = contentWordNumber

    def readData(self):
        """
        database:X.txt file, which contain (target1 polarity1\tsent1 \ntarget2 polarity2\tsent2 \n)
        targetData:
        :return: 'DB' {'topic1':"sent1 sent2",
                     'topic2':"sent3 sent4"}
        :return: 'topicTweets' : {topic:sents}
                                :topic:come from your '--topic' file name, so the input format should be bmt_0.txt
                                :sents:all of the sentences from '--topic' file: (str)'sent1 sent2 sent...'
        """
        DB = {}
        for ifile in self.database:
            with open(ROOT.DATA_ROOT+'/'+ifile, "r") as fi:
                for isent in fi:
                    targPol = " ".join(" ".join(isent.split('\t')[0:-1]).split()).lower().strip('\r\n')

                    try:
                        DB[targPol] = DB[targPol] + ' ' + isent.split('\t',)[-1].lower()
                    except:
                        DB[targPol] = isent.split('\t',)[-1].lower()


        targetTweets = {}
        with open(ROOT.DATA_ROOT+'/target/'+self.targetData, "r") as file:
            topic = ' '.join(self.targetData.split(".")[0].lower().split("_"))  #bmt_positive
            for tweet in file:
                try:
                    sents = sents+' '+tweet.lower()
                except:
                    sents = tweet.lower()
        targetTweets[topic] = sents

        print ("func: readData",'\n'+"DB: ",DB , '\n' +"targetTweets: ", targetTweets,'\n'+'--'*100)
        return DB,targetTweets


    def processing(self,doc):
        """
        :param args: (type:dict(previous DB,targetTweets)) datasets which need to be processed
        :return: dic: {
                       0 : {target: sent1. sent2.}
                       1 : {target: sent1. sent2.}
                       ...
                       }
        """

        dic = {}
        for key in doc:
            sents = ''
            for line in doc[key].split("\n"):
                line = process(line)
                sents = sents+line
            dic[key] = sents

        print ("func: process",'\n'+"return dic: ", dic,'\n'+'--'*100)

        return dic


    def tfidf(self,allData,targetData):
        """
        :param allData: DB and target data
                        {
                        0:{target1:sents, target2:sents}, #alldata from DB
                        1:{target1:sents},                #target data
                        }
        :param contentWordNumber: threshold, how many content words you need
        :return:
        """
        print("func: tfidf")
        target = targetData.keys()

        dictMerged = dict(targetData, **allData)
        bloblist = []
        for sent in dictMerged:
            bloblist.append(tb(dictMerged[sent]))


        def tf(word, blob):
            return blob.words.count(word) / len(blob.words)

        def n_containing(word, bloblist):
            return sum(1 for blob in bloblist if word in blob.words)

        def idf(word, bloblist):
            return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

        def tfidf(word, blob, bloblist):
            return tf(word, blob) * idf(word, bloblist)

        # print("Top words in document: {}".format(target))
        scores = {word: tfidf(word, bloblist[0], bloblist) for word in bloblist[0].words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        contentWordList = []

        for word, score in sorted_words[:int(self.contentWordNumber)]:
            # print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
            # remove single letter
            if len(word)>1:
                contentWordList.append(word)
        print ('top',self.contentWordNumber,'content words for',target,'\n',contentWordList,'\n',100*'**')

        return contentWordList



def main():
    """
        python tfidf.py --allData train.txt test.txt dev.txt --topic bmt_2.txt --contentWordNumber 14
        :predefine:
        :--allData: X.txt file, which contain (target1 polarity1\tsent1\ntarget2 polarity2\tsent2\n )
        :--topic: bmt_0.txt, which contain (sent1 sent2 ... sentn)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--allData', default='', action='store', nargs='+',
                        help="add train test validation dataset together")
    parser.add_argument('--topic', default='', help="target topic")
    parser.add_argument('--contentWordNumber', default='', help="threshold for content Word Number")
    parser.add_argument('--returnNSents', default='', help="top N sentences")

    args = parser.parse_args()
    data = loadData(args.allData, args.topic, args.contentWordNumber)
    allDataDic, targetTweets = data.readData()
    """
    ##modify at def_processing, re-run below line##
    outputDB = data.processing(allDataDic)
    with open(ROOT.DATA_ROOT+'/'+'allDataDic.txt', 'w') as file:
        file.write(json.dumps(outputDB))
    """

    targData = data.processing(targetTweets)
    outputDB = json.load(open(ROOT.DATA_ROOT + '/allDataDic.txt'))
    contentWords = data.tfidf(outputDB, targData)
    return targetTweets,targData, contentWords


if __name__ == '__main__':
    """
    python tfidf.py --allData train.txt test.txt dev.txt --topic bmt_2.txt --contentWordNumber 14
    :predefine:
    :--allData: X.txt file, which contain (target1 polarity1\tsent1\ntarget2 polarity2\tsent2\n )
    :--topic: bmt_0.txt, which contain (sent1 sent2 ... sentn)
    """
    main()