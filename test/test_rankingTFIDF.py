import sys
sys.path.append(r"../..")
from pushkin_gs.sum import rankingTFIDF
from pushkin_gs.sum import tfidf_contentWords


def main():

    contentWords = ['and', 'document','one',"first"]
    data = [
    'This is the first document document document document document',
    'This is the second second document document document document document',
    'And the third one one one one one',
    'Is this the first',
    ]
    test = rankingTFIDF.TFIDF(data,contentWords,1,data)
    test.SentRankTFIDF()

if __name__ == '__main__':
    main()

