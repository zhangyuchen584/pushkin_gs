# coding:utf-8
from pre_processing import readLoadData,dataPreprocessing
from pushkin_gs.definition import ROOT_DIR
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer

def tfidf(data,tfidf_threshold=0.4):
    corpus = []
    for i in data:
        sent = ' '.join(i)
        corpus.append(sent)

    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
      vectorizer.fit_transform(corpus))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵

    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    # print (word)
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    contentWords = []
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
      # print (u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
      for j in range(len(word)):
        if weight[i][j] > tfidf_threshold:
          # print(word[j], weight[i][j])
          contentWords.append(word[j])
    print (contentWords)
    return contentWords


def tfidf_allDoc(data,tfidf_threshold=0.4):
    """
    :corpus: sentence at specific topic(like under 'ord')
    :allDoc: 6k twitter from train,test and validation datasets
    """
    corpus = []
    for i in data:
        sent = ' '.join(i)
        corpus.append(sent)

    with open(ROOT_DIR+"/Corpus/sentiment/Twitter/train.txt", "r") as f1,\
      open(ROOT_DIR+"/Corpus/sentiment/Twitter/test.txt", "r") as f2, \
            open(ROOT_DIR+"/Corpus/sentiment/Twitter/dev.txt", "r") as f3:
      data = f1.read()+f2.read()+f3.read()

    ln = data.split("\n")
    allDoc = [x.split("\t")[-1] for x in ln]
    # print (allDoc)
    # print (corpus)
    allDocStemmer = []
    snowball_stemmer = SnowballStemmer("english")

    for sen in allDoc:
      # print (sen)
      stemmer_words = [snowball_stemmer.stem(word) for word in sen.split(" ")]
      allDocStemmer.append(' '.join(stemmer_words))
    # print (allDocStemmer)


    vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
    tfidf = transformer.fit_transform(
      vectorizer.fit_transform(allDocStemmer))  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    # print (vectorizer.fit_transform(allDoc))
    # print (tfidf)
    vectorizer.fit_transform(corpus)
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语

    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    contentWords = []
    for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
      # print (u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
      for j in range(len(word)):
        if weight[i][j] > tfidf_threshold:
          # print(word[j], weight[i][j])
          contentWords.append(word[j])
    print (contentWords)
    return contentWords


if __name__ == "__main__":
    with open("text.txt","r") as f1:
        data = f1.read()

    readdata = readLoadData.read(data)
    lowerData = dataPreprocessing.toLower(readdata)
    dataNoiceReduction = dataPreprocessing.NoiceReduction(lowerData)
    dataWithoutAbb = dataPreprocessing.combineAbbreviation(dataNoiceReduction)
    processedData = dataPreprocessing.removeStopWord(dataWithoutAbb)
    a = tfidf_allDoc(processedData,0.7)









