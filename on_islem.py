import pandas as pd
import re
import snowballstemmer

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
    "neden", "nedenle", "nin", "on", "onlar", "otuz", "oysa", "şey", "şu",
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


