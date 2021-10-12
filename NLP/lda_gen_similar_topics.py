from gensim import matutils, models, corpora
import pickle
import sys
from glob import glob
from xml.etree import cElementTree as ElementTree
import os
import pickle
# get path to Webserver
lib = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../Webserver/static/py/RecipeManager/"))
sys.path.append(lib)
sys.path.append(os.path.join(lib, "database"))
from topics import TopicManager
#from recipe import Recipe # r = Recipe("F9325101")

RECIPE_PATH = "bauercreate_nextmedia_devhw/recipes/"
DIR = "lda_100i30p40t_Z/"

with open(DIR+"_data.pkl", "rb") as a_file:
    sentences_lemmatized = pickle.load(a_file)

# with open("ingredients.pickle", "rb") as a_file:
#     documents = pickle.load(a_file)

dictionary = corpora.Dictionary.load(DIR+'_gensim.dict')

corpus =[dictionary.doc2bow(text) for text in sentences_lemmatized]
lda = models.LdaModel.load(DIR+"lda_100i30p40t.model")
tm = TopicManager()

topicDict = {}

for file in glob(RECIPE_PATH+"*/*.xml"):
    tree = ElementTree.parse(file)
    root = tree.getroot()
    dcid = os.path.basename(file).replace(".xml", "")
    body = root.find('document').find('body')
    try: # ZUTATEN or ZUBEREITUNG
        data = ElementTree.tostring(body.find('ZUTATEN'), method="text", encoding="utf-8")
        bow = tm._getBow(data.decode("utf-8"))
        #print(bow)
        topics = lda.get_document_topics(bow)
        for topic in topics:
            topicDict.setdefault(topic[0], []) 
            topicDict[topic[0]].append((dcid, topic[1]))
    except AttributeError:
        pass #No ingridients found   

for key, item in topicDict.items():
    item.sort(key=lambda tup: tup[1], reverse=True)

with open(DIR+"recipe_topics.pickle", "wb") as f:
    pickle.dump(topicDict, f)