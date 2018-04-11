#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import json
import argparse
import re
import numpy as np
import csv
import sys

def get_target_stat(i_corpus, i_topic, osave,mode,threshold):
    """
    calculate each data-set, how many tweets for each class <topic, polarity>
    :the raw datasets: train_target.txt(Polarity,Senten), train_tag.txt(Target,Polarity,Senten)\
                      test_target.txt,dev_target.txt
    :param i_corpus: which data set you want to analysis
    :param i_topic: 'twitter_topic_words.txt' which contain all the topics for twitter
    :param osave: save method
    :param mode: train/test
    :param threshold: prune the dataset, return top N topic
    :return: count number matrix
    """
    topics = dict()

    ##load all topics data##
    with open(i_topic) as fileTopic:
        cid = 0
        for topi in fileTopic:
            wd = topi.strip('\r\n').split(':')[0].strip(' ')
            if wd in topics:
                # print('duplicate topics')
                pass
            else:
                topics[wd] = cid
                cid += 1
    sent_with_topic_count = 0
    sen_tag = []
    for ifl in i_corpus:
        with open(ifl) as fi:
            for s in fi:
                s = s.strip('\r\n').lower().split()
                if mode.lower() == 'train':
                    #find topic
                    ifound = []
                    for tp, tid in topics.items():

                        ifound = re.findall('#{0,1}'+tp+'\\b', ' '.join(s[1:]))
                        if len(ifound):
                            ##find all sentences within those topics##
                            sent_with_topic_count += 1
                            sen_tag.append((tid, int(s[0])))
                            break
                    if len(ifound) == 0:
                        sen_tag.append((-1, int(s[0])))
                else:
                    for pos, wd in enumerate(s):
                        if wd in ['0','1','2']:
                            break
                    tp = ' '.join(s[:pos])
                    ts = s[pos]
                    if tp in topics:
                        sen_tag.append((topics[tp], int(ts)))
                        sent_with_topic_count += 1
                    else:
                        print('%s not in topics' % tp)
                        sen_tag.append((-1, int(ts)))
    print (sen_tag)
    print (type(sen_tag))
    sen_tag = np.array(sen_tag)
    print (sen_tag)
    stat = np.zeros((len(topics),3), dtype=np.int16)
    for tp, tid in topics.items():
        for p in [0,1,2]:
            i1 = np.logical_and(sen_tag[:,0] == tid,sen_tag[:,1] == p)
            try:
                if np.sum(i1):
                    stat[tid,p] = np.sum(i1)
            except:
                print('%d %d'%(tid,p))
    #print(stat)
    polarity = {0:'neg',1:'neutral',2:'pos'}
    h_count = 0
    with open(osave, 'wt') as fo:
        csvwt = csv.writer(fo, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        pry = [polarity[p] for p in [0,1,2]]
        csvwt.writerow(['topic']+pry)
        for tp, tid in topics.items():
            rw = [tp]
            for p in [0,1,2]:
                rw += [stat[tid,p]]
                if stat[tid,p]>=threshold:
                    h_count += 1
            csvwt.writerow(rw)

    print('%d %f sentences has target'%(sent_with_topic_count,float(sent_with_topic_count)/sen_tag.shape[0]))
    print('%d category (topic-polarity pair) found in more than %d sentences'% (h_count, threshold))

#select tweet for specific topic & polarity
def list_tweet_category(i_corpus, topc, polarity, mode,osave):
    select_tweet = []
    for ifl in i_corpus:
        with open(ifl) as fi:
            for ln in fi:
                ln = ln.strip('\r\n')
                s = ln.lower().split()
                if mode.lower() == 'train':
                    #find topic
                    ifound = re.findall('#{0,1}'+topc+'\\b', ' '.join(s[1:]))
                    print ('ifound',ifound)
                    if len(ifound) and s[0] == polarity:
                        select_tweet.append(ln)
                else:
                    for pos, wd in enumerate(s):
                        if wd in ['0','1','2']:
                            break
                    tp = ' '.join(s[:pos])
                    ts = s[pos]
                    if tp == topc and ts == polarity:
                        ln = ln.replace(' , ', ' ; ')

                        select_tweet.append(ln+'\n')
    # print('\n'.join(select_tweet))
    print (select_tweet)
    with open(osave, 'w') as fo:
        fo.writelines(select_tweet)

def load_stat(ifile, threshold):
    top_topics = dict({'neg':[],'pos':[],'neutral':[]})
    with open(ifile) as fo:
        csvwt = csv.DictReader(fo, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for r in csvwt:
            ps = []
            if int(r['neg']) > threshold:
                top_topics['neg'] += [r['topic']]
            if int(r['neutral']) > threshold:
                top_topics['neutral'] += [r['topic']]
            if int(r['pos']) > threshold:
                top_topics['pos'] += [r['topic']]
    for sp, tp in top_topics.items():
        print('\nTop sentiment:\t%s,\t%d' % (sp, len(tp)))
        print('\t** %s' % ' * '.join(tp))


#automatic find target based on target list and exact match
def tag_target(i_corpus, i_topic, osave):
    topics = dict()
    with open(i_topic) as fi:
        cid = 0
        for s in fi:
            wd = s.strip('\r\n').split(':')[0].strip(' ')
            if wd in topics:
                # print('duplicate topics')
                pass
            else:
                topics[wd] = cid
                cid += 1
    print (topics)
    sen_tag = []
    for ifl in i_corpus:
        previous = 1
        after = 1
        with open(ifl) as fi:
            for ln in fi:

                ln = ln.strip('\r\n')
                s = ln.lower().split()
                previous = previous + 1

                ifound = []
                for tp, tid in topics.items():
                    # print (tp)
                    ifound = re.findall('#{0,1}'+tp+'\\b', ' '.join(s[1:]))
                    # ifound = re.findall('#{0,1}'+tp+'\\b',s[1:])
                    # print ('1111s')


                    if len(ifound):
                        # print ('-'.join(tp.split())+'\t'+ln)
                        sen_tag.append(' '.join(tp.split())+'\t'+ln+'\n')
                        after = after+1
                        break
        print ("\n\n",ifl)
        print ("previous: ",previous,",after getting target：",after)

    with open(osave, 'w') as fo:
        fo.writelines(sen_tag)

if __name__ == '__main__':
    """
    python get_target_stat.py --corpus sentiment/Twitter/train_target.txt  --topic sentiment/twitter_topic_words.txt --mode train --save stat_train.csv --threshold 30
    python get_target_stat.py --corpus sentiment/Twitter/train_tag.txt sentiment/Twitter/dev_target.txt sentiment/Twitter/test_target.txt  --topic sentiment/twitter_topic_words.txt --mode test --save stat_train_dev_test.txt    
    --corpus sentiment/YouTube/train_targ.txt sentiment/YouTube/test_targ.txt  sentiment/YouTube/dev_targ.txt  --topic sentiment/youtube_topic_words.txt --mode test --save youtube_output.csv
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus',  default='',action='store', nargs='+',help='sentiment file')
    parser.add_argument('--topic',  default = '', action='store', help='topic file to list all topics')
    parser.add_argument('--mode',  default = 'train', action='store', help='type of sentiment file. dev & test has target label, and train has no target label and need topic list to do exact match to find')
    parser.add_argument('--threshold',  default = 10, type=int, help='threshold to prune category')
    parser.add_argument('--save',  default = '', action='store', help='save stat to file')
    print(sys.argv)
    try:
        args = parser.parse_args(sys.argv[1:])
        get_target_stat(args.corpus, args.topic,args.save, args.mode,args.threshold)

    except:
        parser.print_help()