# # -*- coding: utf-8 -*-
# __author__ = "Yuchen"
# __aim__ = 'rank top sentences in one topic'
# __testCase__ = "../test/test_sentenceRanking.py"
#
# class similarity(object):
#     def __init__(self):
#
#     def bag_of_words(self):
#


from rouge import Rouge as R
from prettytable import PrettyTable

class Rouge(object):
    def __init__(self, evaluated_sentences, reference_sentences):
        rouge = R()
        eval_sents = None
        ref_sents = None
        if type(evaluated_sentences) is list:
            eval_sents = ' '.join(evaluated_sentences)
        else:
            eval_sents = evaluated_sentences
        if type(reference_sentences) is list:
            ref_sents = ' '.join(reference_sentences)
        else:
            ref_sents = reference_sentences
        self._score = rouge.get_scores(eval_sents, ref_sents)[0]

    def get_rouge(self):
        return self._score

    def get_rouge_1(self):
        return self._score["rouge-1"]

    def get_rouge_2(self):
        return self._score["rouge-2"]

    def get_rouge_l(self):
        return self._score["rouge-l"]

    @staticmethod
    def cal_avg_rouge(rouges):
        """
        :param rouges: list
            List of dict.
        :return: dict
        """
        avg_rouge = rouges[0]
        n = len(rouges)
        if n > 1:
            for rouge in rouges[1:]:
                for k in rouge:
                    avg_rouge[k]["f"] += rouge[k]["f"]
                    avg_rouge[k]["p"] += rouge[k]["p"]
                    avg_rouge[k]["r"] += rouge[k]["r"]
            for v in avg_rouge.values():
                v["f"] /= n
                v["p"] /= n
                v["r"] /= n

        return avg_rouge

    @staticmethod
    def print(labels, rouges):
        if type(labels) is not list:
            labels = [labels]
        if type(rouges) is not list:
            rouges = [rouges]
        for k in rouges[0]:
            print(k)
            t = PrettyTable(['Summarizer', 'F1-score', 'Precision', 'Recall'])
            for i, v in enumerate(labels):
                t.add_row([v] + list(rouges[i][k].values()))
            print(t)



def main():
    sent1 = '@nightslikedeze congrats respect man . btw when y\'all doing the bmt cheer thingy ,  tommy and i can completely visualize you doing it'
    sent2 = 'pop looooo heheso proud of you and aww so cute to see you do the bmt roar hahhaha @ the float at'
    sent3 = 'cheers to adulthood my bmt buddiesthank you for the unforgettable night and i hope you all enjoyed'
    sent4 = 'soon will be marching with my section mate that make my bmt going so well and always having fun'
    sent5 = 'happy pop my bae it doesnt feel like 9 weeks at all ( ? ! ) but im glad to have been part of your bmt'
    enstance = Rouge(sent1,sent5)
    score = enstance.get_rouge_1()
    print (score)


if __name__ == '__main__':
    # main()

    bookout_1 = []
    bookout_2 = []
    f_score = 0
    k = 0
    with open ('C:/Users/Yuchen/Downloads/annotation/enlistment_p_linh.txt', 'r') as fi:
        for line in fi:
            # print (line)
            if line != None:
                bookout_1.append(line.strip('\r\n'))
        print (bookout_1)
    with open ('C:/Users/Yuchen/Downloads/annotation/enlistment_p_Toey.txt', 'r') as fi:
        for line in fi:
            # print (line)
            if line != None:
                bookout_2.append(line.strip('\r\n'))
        print (bookout_2)
    for i in bookout_1:
        for j in bookout_2:
            k = k +1
            print (i)
            print (j)
            enstance = Rouge(i, j)
            score = enstance.get_rouge_1()
            f_score = f_score + score['f']
            print(score['f'])
            print ('------')
    print(f_score / k)
    # print (f_score)


