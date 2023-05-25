import pandas as pd
import re
import snowballstemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import Word2Vec

#sayısal değerlerin kaldırılması
def remove_numeric(value):
    bfr = [item for item in value if not item.isdigit()]
    bfr = "".join(bfr)
    return bfr


#emojilerin kaldırılması
def remove_emoji(value) : 
    bfr = re.compile("[\U00010000-\U0010ffff]" , flags = re.UNICODE)
    bfr = bfr.sub(r'', value)
    return bfr


#tek karakterlerin kaldırılması
def remove_single_chracter(value) : 
    return re.sub(r'(?:^| )\w(?:$| )' , '' , value)


#noktalama işaretlerinin kaldırılması
def remove_punctuation(value): 
    return re.sub(r'[^\w\s]', '' , value)


#linklerin kaldırılması
def remove_link(value):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','' , value)


#hastaglerin kaldırılması
def remove_hashtag(value):
    return re.sub(r'#[^\s]+','',value)


#kullanıcı adı kaldırma
def remove_username(value):
    return re.sub(r'@[^\s]+','',value)

#kök indirgeme ve stop word
def stem_word(value):
    stemmer = snowballstemmer.stemmer("turkish")
    value = value.lower()
    value = stemmer.stemWords(value.split())
    stop_words = ["acaba", "altmış", "altı", "ama", "ancak", "daha", "da", "de", "dedi",
    "diye", "doğru", "doksan", "dokuz", "dolayı", "dört", "için", "gibi",
    "hâlâ", "hangi", "hem", "hep", "her", "hiç", "iki", "ile", "ise", "kadar",
    "ki", "kim", "küçük", "mı", "mu", "mıydı", "muymuş", "nasıl", "ne",
    "neden", "nedenle", "nin", "on", "onlar", "otuz", "oysa", "şey", "şu","bir",
    "sıfır", "tarafından", "üç", "üzere", "var", "veya", "ve", "ya", "yani",
    "yirmi", "yok", "zaten", "çok"]
    value = [item for item in value if not item in stop_words]
    value = ' '.join(value)
    return value


def pre_processing(value):
    return [remove_numeric(remove_emoji
                           (remove_single_chracter
                            (remove_punctuation
                             (remove_link
                              (remove_hashtag
                               (remove_username
                                (stem_word(word)))))))) for word in value.split()]


#boşlukları kaldırma
def remove_space(value):
    return [item for item in value if item.strip()]


# bag of words model

def bag_of_words(value):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()

# tf-idf model
def tfidf(value):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()

#word2vec model
def word2vec(value):
    model = Word2Vec.load("data/word2vec.model")
    bfr_list = []
    bfr_len = len(value)

    for k in value:
        bfr = model.wv.key_to_index[k]
        bfr = model.wv[bfr]
        bfr_list.append(bfr)
    
    bfr_list = sum(bfr_list)
    bfr_list = bfr_list/bfr_len
    return bfr_list.tolist()