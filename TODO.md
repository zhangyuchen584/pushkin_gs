# read 6 data into numpy (✔️)
--?单独处理retweets
# lowcases (?)(✔️)

# remove
    ##url(✔️),media(?) etc
    ##accent(✔️？), emoticons(✔️？)
    ##Finally, the cleaned text is tokenized.(✔️)
    ##不处理spelling false, hash tag
#converter acronyms and abbreviations
    ##crawler slang dictionary
        ##已经爬完了，写出csv来.
#delete stop words


##Tweet Cleaning Submodule
Additionally, it removes all non-printable ascII characters(✔️).
Finally, the cleaned text is tokenized.



ling correction and hashtag segmentation are expensive to perform especially in a mobile device.


##Tweet Ranker Submodule:
1. tf-idf / centroid of the topic / cosine similarity between the tweet
2. word rank score Swr (t) / list of words within each topic, sorted by their word frequencies / word frequency score Sw f (t ) / 
3. hashtag score (Sht ) and popularity score (Spop )

##Topic Labels Generator Submodule
graph-based TextRank
1.To generate topic labels for each topic, it  rst com- putes the frequencies of the bigrams<?>




小写 (T)
降噪： URL，@人名 #话题 (T)
去掉stop words (T)

0. 缩写 -> 意义的词 (T)
0.1. 去掉stop words (T)
1. 用wordnet做同义词的替换，对content words （wordnet ->word similarity）
2. 使用tfidf找到content words (T)
尝试下LDA topic modeling #进阶考虑可以试试lda（也是基于统计）提取特征。


basic method: tfidf + MMR
##3..尝试下  用sklearn  affinity progpagation
标记数据的前端

document frequency using 6k docs (text rank)？意义是什么？ TEXTRANK at whole dataset

# gs # 可以用n-gram来 detect phrase

# MMR
# sentence similarity
# ROUGE

QQQQ：现在的tfidf 句子分数是 contentwords直接相加，但是contentwords有自己的tfidf权重， 要不要乘？？
QQQQ: class TFIDF 需要一个nyarray去存 index, ini_sent, processed_sent, ranking_score, 加上惩罚因子的ranking score