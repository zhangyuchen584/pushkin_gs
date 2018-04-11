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
from get_target_stat import list_tweet_category

##give topic,sentiment to it, then return sentence##
if __name__ == '__main__':
    """
    python get_topic_tweet.py --topic ippt --corpus sentiment/Twitter/dev_target.txt --mode test --senti 2 --save zhang.csv
    --topic ns --corpus sentiment/YouTube/useful/dev_targ.txt  sentiment/YouTube/useful/train_targ.txt sentiment/YouTube/useful/test_targ.txt --mode test --senti 2 --save sentiment/YouTube/useful/ns_2.csv
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus',  default='',action='store', nargs='+',help='sentiment file')
    parser.add_argument('--topic',  default = '', action='store', help='particular topic selected for display')
    parser.add_argument('--senti',  default = '', action='store', help='sentiment')
    parser.add_argument('--mode',  default = 'train', action='store', help='type of sentiment file. dev & test has target label, and train has no target label and need topic list to do exact match to find')
    parser.add_argument('--save', default='', action='store', help='save stat to file')
    print(sys.argv)
    try:
        args = parser.parse_args(sys.argv[1:])
        list_tweet_category(args.corpus, args.topic, args.senti, args.mode, args.save)
    except:
        parser.print_help()

