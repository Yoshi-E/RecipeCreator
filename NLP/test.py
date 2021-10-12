import MySQLdb
import MySQLdb.cursors
from glob import glob
from xml.etree import cElementTree as ElementTree
import time
import pickle
import os
import io

from NLP import *

db = MySQLdb.connect(host="gamesound.eu",
                user="bauer",     
                passwd="rEN1cDaAQSJGrfbcCxzN",
                db="bauermedia",
                port=3307,
                cursorclass=MySQLdb.cursors.DictCursor)

cur = db.cursor()

def sql(sql):
    try:
        cur.execute(sql)
        db.commit()
        return cur.fetchall()
    except Exception as ex:
        print(sql, ex)
        db.rollback()
        raise Exception("Error: {}".format(sql))

#results = sql("SELECT * FROM bauermedia.images;")
#print(results)

RECIPE_PATH = "bauercreate_nextmedia_devhw/recipes/"

# Time: ~15min
def loadDataFromOriginal():
    start = time.time()

    #check if action was already completed
    if os.path.isfile("preparations.pickle") and os.path.isfile("ingredients.pickle"):
        ingredients = open("ingredients.pickle", 'rb')
        preparations = open("preparations.pickle", 'rb')
        return pickle.load(ingredients), pickle.load(preparations) 
    
    ingredients = []
    preparations = []
    fails = 0
    for file in glob(RECIPE_PATH+"*/*.xml"):
        tree = ElementTree.parse(file)
        root = tree.getroot()

        body = root.find('document').find('body')
        try:
            data = ElementTree.tostring(body.find('ZUTATEN'), method="text", encoding="utf-8")
            ingredients.append(data.decode("utf-8"))
        except AttributeError:
            fails += 1
            #pass #No ingridients found   
        
        try:
            data = ElementTree.tostring(body.find('ZUBEREITUNG'), method="text", encoding="utf-8")
            preparations.append(data.decode("utf-8"))
        except AttributeError:
            fails += 1
            #pass #No ingridients found
         

    with open("ingredients.pickle", "wb") as f:
        pickle.dump(ingredients, f)    
    with open("preparations.pickle", "wb") as f:
        pickle.dump(preparations, f)
    end = time.time()
    print("[loadDataFromOriginal] Loaded {} and {} elements in {} seconds. Failed to read: {}".format(len(ingredients), len(preparations), round(end - start, 2), fails))
    return ingredients, preparations

import nltk
from nltk.tokenize import RegexpTokenizer
nltk.download('punkt')


ingredients, preparations = loadDataFromOriginal()
print(ingredients[0])

def test1():
    stemmer = nltk.stem.cistem.Cistem()

    for word in ingredients[0].split(" "):
        #word = "Speicherbehältern"
        print(stemmer.stem(word))
        continue
        for r in stemmer.segment(word):
            print(r)

# cauclate difference between two texts 
def cosinus(a,b):
    return sum([a[k]*b[k] for k in a if k in b]) / (math.sqrt(sum([a[k]**2 for k in a])) * math.sqrt(sum([b[k]**2 for k in b])))


start = time.time()
import spacy
spacy.load('de_core_news_sm') #en_core_web_sm #
from spacy.lang.de import German
from HanTa import HanoverTagger as ht
from pprint import pprint

# Time ~10min
def generateLemmatization():
    sentences = ingredients[0]
    nouns = [] 
    sentences_tok = [cst_tokenize(sent) for sent in ingredients]
    #sentences_tok = [nltk.tokenize.word_tokenize(sentences)]
    #print(sentences_tok)
    for sent in sentences_tok:
        tags = tagger.tag_sent(sent) 
        nouns_from_sent = [lemma for (word,lemma,pos) in tags if pos == "NN" or pos == "NE"]
        nouns.extend(nouns_from_sent)

    fdist = nltk.FreqDist(nouns)    

    with io.open("ingredients_set.txt", "w+", encoding="utf-8") as f:
        for element in fdist.most_common(10000):
            line = str(element) + "\n"
            f.write(line)

    pprint(fdist.most_common(10))
    end = time.time()
    print("Time:",round(end - start, 2))

    fdist.plot(50,cumulative=False)

def testTagger():
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')

    parser = German()

    # based on
    # https://textmining.wp.hs-hannover.de/Klassifikation.html
    # https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21

    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(ingredients[0])
    #nltk.tokenize.word_tokenize(ingredients[0],language='german')
    print(tokens)
    #tags = tagger.tag_sent(tokenized_sent)

from gensim import matutils, models, corpora


if os.path.exists("data.pkl"):
    with open("data.pkl", "rb") as a_file:
        sentences_lemmatized = pickle.load(a_file)
else:
    sentences_tok = [cst_tokenize(sent) for sent in ingredients]
    sentences_lemmatized = []
    tagger = ht.HanoverTagger('morphmodel_ger.pgz')
    nouns = [] 
    for sent in sentences_tok:
        tags = tagger.tag_sent(sent) 
        nouns_from_sent = [lemma for (word,lemma,pos) in tags if pos == "NN" or pos == "NE"]
        nouns.extend(nouns_from_sent)
        sentences_lemmatized.append(nouns_from_sent)

    with open("data.pkl", "wb") as a_file:
        pickle.dump(sentences_lemmatized, a_file)

import logging
import math
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if not os.path.exists('gensim.dict'):
    dictionary = corpora.Dictionary(sentences_lemmatized)
    dictionary.save('gensim.dict')
else:
    dictionary = corpora.Dictionary.load('gensim.dict')

print("-"*50)
print(dictionary)
print(sentences_lemmatized[0])


start = time.time()
corpus =[dictionary.doc2bow(text) for text in sentences_lemmatized]
lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=100, passes=100, update_every=1) #, distributed=True, chunksize=math.floor((len(sentences_lemmatized)-1)/5), 

# set PYRO_SERIALIZERS_ACCEPTED=pickle
# set PYRO_SERIALIZER=pickle

#python -m Pyro4.naming -n 0.0.0.0
#python -m gensim.models.lda_worker
#python -m gensim.models.lda_dispatcher

lda.save("lda.model")
print(lda.print_topics())

end = time.time()
print("Time:",round(end - start, 2))
# avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
# print('Average topic coherence: %.4f.' % avg_topic_coherence)



## look at https://openrefine.org/ for data cleaning
