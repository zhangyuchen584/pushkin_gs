import sys
sys.path.append(r"../..")
from pushkin_gs.definition import ROOT
import argparse

origDataRoot = ROOT.DATA_ROOT+'/corpus/'
# with open(ROOT.DATA_ROOT+'/corpus', "r") as fi:
# files = os.listdir(ROOT.DATA_ROOT+'/corpus')
# # print ('files',files)
# def calculate_eachTopicSents(folder):
#     for ifl in folder:
#         dir = ROOT.DATA_ROOT + '/corpus/'+ifl
#         pattern = re.compile(r'.txt')
#         print (pattern)
#         files = os.listdir(dir)
#         print (files)
#         for i in files:
#             print (i)
#             match = pattern.match(i)
#             print (match)
#
#
#
#
#     # files = os.listdir(ROOT.DATA_ROOT + '/corpus/'+)
#
# if __name__ == '__main__':
#     """
#
#     """
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--dataFolder', default='', help="Tw",action='store', nargs='+')
#
#
#     args = parser.parse_args()
#     data = calculate_eachTopicSents(args.dataFolder)
#
#     # print (data)
#     # pass

import os


alldata = {}

def topicSents(folders,threshold):
    count = 1
    for ifold in folders:
        dir = origDataRoot+ifold

        files = os.listdir(dir)  # 得到文件夹下的所有文件名称
        for file in files:

            if file.find('swp') == -1:
                if file.find('txt') != -1:
                    print(file)
                    with open (origDataRoot+'/'+ifold+'/'+file,'r') as fi:
                        icount = 1
                        for line in fi:
                            # print (line)
                            count = count + 1
                            icount = icount +1
                            # print(re.split('1|2|0', line, 1))
                            # print (line.split('\t')[0]+'_'+line.split('\t')[1])
                            try:
                                alldata[line.split('\t')[0]+'_'+line.split('\t')[1]] = alldata[line.split('\t')[0]+'_'+line.split('\t')[1]] + line.split('\t')[2]
                            except:
                                alldata[line.split('\t')[0] + '_' + line.split('\t')[1]] = line.split('\t')[2]
                    print (icount)
    print ("total number of sentence: ",count)
    # print(alldata)
    for ith in threshold:
        neg = 0
        pos = 0
        print ("\n\n\nnumber of sents > ", ith)
        for i in alldata:
            if i[-1] == str(1):
                continue

            if len(alldata[i].split('\n')) > int(ith):
                if i[-1] == str(0):
                    neg = neg+1
                if i[-1] == str(2):
                    pos = pos+1
                print ("target: ",i, ",  number: ",len(alldata[i].split('\n')))
        print ("\npolarity_0:", neg,"polarity_1:", pos)

    return alldata




if __name__ == "__main__":
    """
    python calculate_eachTopicSents.py --dataFolder Twitter YouTube --threshold 40
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataFolder', default='', help="Tw",action='store', nargs='+')
    parser.add_argument('--threshold', default='', help="Tw", action='store', nargs='+')
    args = parser.parse_args()
    data = topicSents(args.dataFolder,args.threshold)



    import re


