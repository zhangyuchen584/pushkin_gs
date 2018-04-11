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
from get_target_stat import load_stat


##print all class with its counts##
if __name__ == '__main__':
    """
    (F)python get_prune_topic.py --mode train --stat stat_train.csv --threshold 30
    (T)python get_prune_topic.py --stat stat_train.csv --threshold 15
    --stat youtube_output.csv --threshold 30
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--stat',  default = '', action='store', help='statistic data file to topic-poparity occurrences')
    parser.add_argument('--threshold',  default = 10, type=int, help='threshold to prune category')
    print(sys.argv)
    try:
        args = parser.parse_args(sys.argv[1:])
        load_stat(args.stat, args.threshold)
    except:
        parser.print_help()

