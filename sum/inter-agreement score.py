# -*- coding: utf-8 -*-
__author__ = "Yuchen"
__aim__ = 'rank top sentences in one topic'
__testCase__ = "../test/test_sentenceRanking.py"

import argparse
import numpy as np
# from Processing import process,synonyms
import Processing
from sentSimilarity import Rouge
import operator
from tfidf_contentWords import loadData
## for annotation sentences, there have many similar sentences； I hate monday/ I hate monday either. Although diff people select diff sentences, but the meaning is exactly same.
# So the question is how to measure the the similar sentence at annotation stage

def load_data(i_corpus):
    """
    input data format: txt. sentence --(rank:1)
                            sentence --(rank:0)..
    :return:
    """

    docs = np.zeros((1 , len(i_corpus)+1), dtype=np.int16)

    # for ifl in i_corpus:
    #     print (ifl)
    for ifl in enumerate(i_corpus):
        print (ifl)
        if ifl[0] == 0:
            with open(ifl[1]) as fi:
                for ln in enumerate(fi):

                    row = np.array([ln[0],ln[1].split(" --(")[0],ln[1].split(" --(")[1].split(")")[0]])
                    docs = np.row_stack((docs,row))
        else:
            with open(ifl[1]) as fi:
                list = [0]
                for ln in enumerate(fi):
                    # print (ln[1])
                    list.append(ln[1].split(" --(")[1].split(")")[0])
                column = np.array(list)
                docs = np.column_stack((docs, column))
    return docs



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--allData', default='', action='store', nargs='+',
                        help="add train test validation dataset together")

    args = parser.parse_args()
    data = load_data(args.allData)

    ##processing
    list = [0]
    for sent in data[:,1][1:]:
        list.append(Processing.process(sent))
    column = np.array(list)
    data = np.column_stack((data, column))


    #find synonyms
    synonyms_column = [0]
    for sent in data[:, -1][1:]:
        synonyms_sent = []
        for word in sent.split():
            weight = 1/len(sent.split())
            # print (weight)
            word_list = Processing.synonyms(word)

            synonyms_sent = synonyms_sent + word_list
        uniqSynon = set(synonyms_sent)
        synonyms_column.append(uniqSynon)

    data = np.column_stack((data, synonyms_column))



    #calculate similarity

    dic = {}
    simiSentences = []
    for i in range(1,len(data)):
        for j in range(i+1,len(data)):

            enstance = Rouge(' '.join(data[:,-1][i]), ' '.join(data[:,-1][j]))
            score = enstance.get_rouge_1()
            dic[i-1, j-1] = score['f']
    sorted_x = sorted(dic.items(), key=operator.itemgetter(1),reverse=True)
    # print (sorted_x)
    for sents,simiScore in sorted_x:
        if simiScore > 0.6:
            simiSentences.append(sents)

    # print (simiSentences)


    ## sentence groups
    allSents = ()
    for item in simiSentences:
        allSents = allSents + item
    # print(allSents)

    senGroup = []
    for item in [sent for sent in allSents if sent not in senGroup]:
        if item not in senGroup:
            senGroup.append('mark')
            senGroup.append(item)

        for index in senGroup:
            for i, j in simiSentences:
                if i == index and j not in senGroup:
                    senGroup.append(j)

                elif j == index and i not in senGroup:
                    senGroup.append(i)
    # print (senGroup)

    ## each sentence groups
    group = {}
    num = 0
    list = []
    for i in senGroup:
        # print (i)
        if i != 'mark':
            list.append(i)
            # print(list)
        else:
            group[num] = list
            num = num + 1
            list = []
            # print (list)
    group[num] = list
    print(group)



    #delete first row
    data = np.delete(data, 0, 0)


    ##annotate similar sentence
    for row in data:
        # pass
        print (row[:,2:-2])




if __name__ == '__main__':
    """
    --allData enlistment_pos1.txt enlistment_pos2.txt
    """
    main()

