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
from get_target_stat import tag_target

##刚开始的train文件格式不对，更改格式的
if __name__ == '__main__':
    """
    python get_target_stat.py --corpus sentiment/YouTube/train_target.txt  --topic sentiment/youtube_topic_words.txt --save sentiment/YouTube/train_targ.txt
    --corpus sentiment/YouTube/test.txt  --topic sentiment/youtube_topic_words.txt --save sentiment/YouTube/useful/test_targ.txt
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus',  default='',action='store', nargs='+',help='sentiment file')
    parser.add_argument('--topic',  default = '', action='store', help='topic file to list all topics')
    parser.add_argument('--save',  default = '', action='store', help='save stat to file')
    print(sys.argv)
    try:
        args = parser.parse_args(sys.argv[1:])
        tag_target(args.corpus, args.topic,args.save)
    except:
        parser.print_help()