#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
sys.path.append(r"../..")
##This is your Project Root##
from pushkin_gs.definition import ROOT_DIR
# ROOT_DIR = os.path.abspath('..') #This is the father folder
# ROOT_DIR = os.path.abspath('.') #This is your current Work Root
import re
from nltk import word_tokenize
import unidecode
from string import punctuation
import numpy as np
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from nltk.stem import SnowballStemmer

class readLoadData():
    def read(readdata):
        ln = readdata.split("\n")
        return ln


class dataPreprocessing():

    def toLower(data):  ##not sure it is useful or not？##
        """
        :return: twitter sentences to lowercase
        """
        for index in range(len(data)):
            data[index] = data[index].lower()

        return data

    def NoiceReduction(data):
        """
        :description: 1.remove url,media etc/ 2.remove words with accents or emoticons/
                      3.remove non-printable ascII characters /4.Finally, the cleaned text is tokenized
        :return:
        """
        ##define emoji emoticons##
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        Data = []
        for sentence in data:

            ##remove url##
            sentence = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', sentence)
            ##remove punctuations##
            sentence = ' '.join(word for word in sentence.split(" ") if word not in punctuation)
            ##modify accent(Málaga->Malaga)##
            sentence = unidecode.unidecode(sentence)
            ##remove emoticons##
            sentence = emoji_pattern.sub(r'', sentence)
            ##remove @people remove #hashtag##
            sentence = re.sub(r'[@#][ ]?([A-Za-z0-9_-]+)','',sentence)

            ##tokenization using nltk##
            # sentence = word_tokenize(sentence)
            ##there have an issue if use tokenization: words like 'gonna' will be split to 'gon','na', then next step remove abbreviation will make some noize data##
            sentence = sentence.split(" ")
            Data.append(sentence)

        return Data


    def combineAbbreviation(data):
        with open(ROOT_DIR + "/support/slangDic.txt", "r") as f1:
            slangDic = f1.read()

        # print (slangDic.split("\n"))
        slang = {}
        slangKey = []
        for index in slangDic.split("\n"):
            try:
                slang[index.split(":")[0]] = index.split(":")[1]
                slangKey.append(index.split(":")[0])
            except:
                pass
        # print (slangKey)

        dataWithOutAbb = []
        for sent in data:
            abb = [x for x in slangKey if x in sent]
            if abb:
                for item in abb:
                    sent = [x if (x != item) else slang[item] for x in sent]
                    sent = ' '.join(sent).split(" ")
                dataWithOutAbb.append(sent)
            else:
                dataWithOutAbb.append(sent)
        # print (dataWithOutAbb)
        return dataWithOutAbb




    def combinePhrase(data):
        """
        #Natural Language Corpus Data: Beautiful Data
        #http://norvig.com/ngrams/
        combine word phrase, like 'surface_water', but we need to find Synsets from wordNet, so cannot combine at this stage
        """
        pass
    def removeStopWord(data):
        ##remove stop word also stemmer word##

        dataWithOutStops = []
        snowball_stemmer = SnowballStemmer("english")
        for sent in data:

            filtered_words = [word for word in sent if word not in stopwords.words('english')]
            stemmer_words = [snowball_stemmer.stem(word) for word in filtered_words]
            dataWithOutStops.append(stemmer_words)
        print(dataWithOutStops)
        return dataWithOutStops



    def wordNet(data):
        """
        find Synsets
        many problems: Polysemy word will change sentence meaning, really time consuming
        """
        pass
        # print("1", wn.synsets('going'))  ##find similar words
        # print("2", wn.synset('miss.n.01').lemma_names())





if __name__ == "__main__":

    with open("text.txt","r") as f1:
        data = f1.read()

    readdata = readLoadData.read(data)
    lowerData = dataPreprocessing.toLower(readdata)
    dataNoiceReduction = dataPreprocessing.NoiceReduction(lowerData)
    dataWithoutAbb = dataPreprocessing.combineAbbreviation(dataNoiceReduction)
    processedData = dataPreprocessing.removeStopWord(dataWithoutAbb)
    # print (processedData)

"""
    print ("3",wn.synsets('car'))
    motorcar = wn.synset('car.n.01')
    types_of_motorcar = motorcar.hyponyms()
    print ("4",types_of_motorcar)
    print (sorted([lemma.name()
                   for synset in types_of_motorcar
                   for lemma in synset.lemmas()]))


    input = [[('A', 1), ('B', 2)], ('C', 3), ('D', 4)]
    from functools import reduce
    reduce(lambda x, y: x + y, input)
    print (list(itertools.chain(*input)))
"""




# if __name__ == "__main__":
#     #open all rawData & combine together
#
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--corpus',  default='',action='store', nargs='+',help='sentiment file')
#
#
#     with open(ROOT_DIR+"/data/Subtasks_BD/twitter-2015testBD.txt", "r") as f1, \
#             open(ROOT_DIR+"/data/Subtasks_BD/twitter-2015train-BD.txt", "r") as f2:
#         rawData1,rawData2,rawData3,rawData4,rawData5,rawData6 = f1.read(),f2.read()
#

