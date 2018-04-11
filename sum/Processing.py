# -*- coding: utf-8 -*-
__author__ = "Yuchen"
import sys
import re
from nltk.stem import SnowballStemmer
import unidecode
from string import punctuation
from nltk.corpus import wordnet as wn
sys.path.append(r"../..")
from pushkin_gs.definition import ROOT
from pushkin_gs.support import stopwordsNoNegWords


def process(line):
    """

    :param data: data you should do processing
           data format: str(sentence)
    :return:
    """
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)

    # define abbraviation
    with open(ROOT.ROOT_DIR + "/support/slangDic.txt", "r") as f1:
        slangDic = f1.read()

    slang = {}
    slangKey = []

    for index in slangDic.split("\n"):
        try:
            slang[index.split(":")[0]] = index.split(":")[1]
            slangKey.append(index.split(":")[0])
        except:
            pass

    ##stemmer words##
    snowball_stemmer = SnowballStemmer("english")


    line = line.replace("\t", " ").lower()
    # doc[key] = doc[key].replace("\n","PA$$w@r0")
    ##remove url##
    line = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', line)
    ##remove @people remove #hashtag##
    line = re.sub(r'[@#][ ]?([A-Za-z0-9_-]+)', '', line)
    ##remove punctuations##
    # line = ' '.join(word for word in line.split() if word not in punctuation)+' . '
    line = ' '.join(''.join(word for word in line if word not in punctuation).split())

    ##modify accent(Málaga->Malaga)##
    line = unidecode.unidecode(line)
    ##remove emoticons##
    line = emoji_pattern.sub(r'', line)

    ##remove abbreviation##
    abbre = [x for x in slangKey if x in line.split(" ")]

    line = line.split(" ")

    if abbre:
        for item in abbre:
            line = [x if (x not in abbre) else slang[item] for x in line]
    line = ' '.join(line)

    ##remove stopWords and stemmer word##
    try:
        line = ' '.join([word for word in line.split() if word not in stopwordsNoNegWords.stop_words])
        line = ' '.join([snowball_stemmer.stem(word) for word in line.split()])+'.'
    except:
        pass

    return line


def synonyms(word):
    """

    :param words: str(word)
    :return: synonyms list['word1','word2','word3'...]
    """
    synonyms = []
    for syn in wn.synsets(word):
        for l in syn.lemmas():
            synonyms.append(' '.join(l.name().split('_')))

    # print(set(synonyms))
    return synonyms



if __name__ == '__main__':

    data = 'you  didn\'t  gonna ()..)thinking "improvement" http://www.df.df i home @lichao .'
    # return
    # didnt go think improv home
    print (process(data))
