
from nltk.corpus import stopwords
# print (set(stopwords.words('english')))

stop_words = { 'ain', 'in', 'them', 'did', 'shan', 're', 'by', 'have', 'those', 'itself', 'ours', 'more',  'mustn', 'until', "you'd", 'over',
               'if', 'be', 'whom',  'was', 'is', 'why', 'about', 'yourselves', 'down', 'above', 'doesn', 'being', 'how',  'won', 'he', 'your',
               'who', 'that', 'the', 've', 'because',  'll', 'm',  'now', 'just', 'o',  'does', 'then',  'are', 'under', 'him', 'during',
               'below', 'theirs', "you've",  'had', 's', 'his', 'further', 'they', 'while', 'such', 'there', 'me', 'on', 'both', 'it', 'off',
               'most', 'too', 'these', 'ma', 'its', "mightn't", 'y', 'into', 'to',  'we', 'myself', 'doing', 'this', 'a', 'nor', 'where',
               "it's", 'or', 'of', 'for', 'when', "you're", 'and', 'very', 'up', 'all', 'as', 'ourselves', 'before', 'through', 'which',
               'any', 'what', 'do', 'same', 'themselves', 'from', 'yourself', 'only', 'haven', "that'll", 'don', 'between', 'yours', 'once',
               'i', 'herself', 'at', 'her', 'can', 'shouldn', 'has', "you'll", 'my', 'will', 'd', "she's",  'been', 'after', 'an',
               'mightn', 'wasn', 'with', 'other', 'she', 'you', 'their', 'again', 'am', 'here', 'some', 'than', 'should', 'own',  'himself',
               'having',  'each', 'hers',  'were','few', 'our', 'so'}
