import MySQLdb
import MySQLdb.cursors
from glob import glob
from xml.etree import cElementTree as ElementTree
import time
import pickle
import os
import io
import shutil
import warnings
from NLP import *


RECIPE_PATH = "bauercreate_nextmedia_devhw/recipes/"
warnings.filterwarnings("ignore", category=DeprecationWarning)

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

# import nltk
# from nltk.tokenize import RegexpTokenizer
# nltk.download('punkt')

# import spacy
# spacy.load('de_core_news_sm') #en_core_web_sm #
# from spacy.lang.de import German
from HanTa import HanoverTagger as ht
from gensim import matutils, models, corpora
from gensim.models.callbacks import PerplexityMetric, ConvergenceMetric, CoherenceMetric
import logging
import sys 
import lda_analyse

if __name__ == "__main__":
    # Save models so they aren't lost
    if not os.path.exists("tmp/"):
        os.makedirs("tmp/")
    ingredients, preparations = loadDataFromOriginal()
    #print(ingredients[0])

    start = time.time()
    if os.path.exists("_data.pkl"):
        with open("_data.pkl", "rb") as a_file:
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

        with open("_data.pkl", "wb") as a_file:
            pickle.dump(sentences_lemmatized, a_file)

    root_logger= logging.getLogger()
    root_logger.setLevel(logging.DEBUG) # or whatever
    handler = logging.FileHandler('model_callbacks.log', 'w', 'utf-8') # or whatever
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s') # or whatever
    handler.setFormatter(formatter) # Pass handler as a parameter, not assign
    root_logger.addHandler(handler)
    root_logger.addHandler(logging.StreamHandler())

    if not os.path.exists('_gensim.dict'):
        dictionary = corpora.Dictionary(sentences_lemmatized)
        dictionary.save('_gensim.dict')
    else:
        dictionary = corpora.Dictionary.load('_gensim.dict')


    start = time.time()
    print("-"*50)
    print(dictionary)
    print(sentences_lemmatized[0])

    passes = 30
    iterations = [100]
    num_topics = 30
    postfix = "I"
    corpus =[dictionary.doc2bow(text) for text in sentences_lemmatized]
    perplexity_logger = PerplexityMetric(corpus=corpus, logger='shell')
    convergence_logger = ConvergenceMetric(logger='shell')
    coherence_cv_logger = CoherenceMetric(corpus=corpus, logger='shell', coherence = 'c_v', texts = sentences_lemmatized)
 

    for iteration in iterations:
        epoch_logger = EpochSaver(f"tmp/{iteration}") 
        # needs modifcation to \gensim\models\callbacks.py line 518:
        """ for i, metric in enumerate(self.metrics):
                if isinstance(metric, CallbackAny2Vec):
                    metric.on_epoch_end(copy.deepcopy(self.model))
                    continue
            ..."""
        root_logger.debug(f'Start of model: {iteration} iterations')
        lda = models.LdaModel(  corpus=corpus, 
                                id2word=dictionary, 
                                num_topics=num_topics, 
                                passes=passes, 
                                iterations=iteration,
                                #update_every=1,
                                eval_every=20,
                                random_state=100,
                                callbacks=[convergence_logger, perplexity_logger, coherence_cv_logger, epoch_logger]) 
                                #, distributed=True, chunksize=math.floor((len(sentences_lemmatized)-1)/5), 
        root_logger.debug(f'End of model: {iteration} iterations')
        
        DIR = f"lda_{iteration}i{passes}p{num_topics}t_{postfix}/"
        MODEL = f"lda_{iteration}i{passes}p{num_topics}t.model"
        # Save models so they aren't lost
        if not os.path.exists(DIR):
            os.makedirs(DIR)

        lda.save(DIR+MODEL)
        for file in ["model_callbacks.log", "_data.pkl", "_gensim.dict"]:
            shutil.copyfile(file, DIR+file)
        print("-"*100)
        print("Generating analytics")
        lda_analyse.analyseLog(iterations=iterations, DIR=DIR, MODEL=MODEL)
        print("-"*100)
        print("Generating HTML view")
        lda_analyse.generateHTMLView(DIR=DIR, MODEL=MODEL)
        


    # set PYRO_SERIALIZERS_ACCEPTED=pickle
    # set PYRO_SERIALIZER=pickle

    #python -m Pyro4.naming -n 0.0.0.0
    #python -m gensim.models.lda_worker
    #python -m gensim.models.lda_dispatcher

    #lda.save("lda.model")
    #print(lda.print_topics())

    end = time.time()
    print("Time:",round(end - start, 2))
    # avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    # print('Average topic coherence: %.4f.' % avg_topic_coherence)



    ## look at https://openrefine.org/ for data cleaning
