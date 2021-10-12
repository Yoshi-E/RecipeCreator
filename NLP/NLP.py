import nltk
import re
from gensim.models.callbacks import CallbackAny2Vec
from gensim import models, corpora
import pickle
import pyLDAvis
#from pyLDAvis import gensim

import spacy
"""
python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
"""
spacy_nlp = spacy.load('de_core_news_sm') #en_core_web_sm #
#from spacy.lang.de import German

def cst_token_test(token):
    token = token.strip().lower()
    if token.isnumeric():
        return False
    if re.search(r'\d', token):
        return False
    if len(token)<=1:
        return False
    return True
    

def cst_tokenize(text):
    words = nltk.tokenize.word_tokenize(text, language="german")
    blacklist = """
        g el zutat zutaten für ca person personen m ( ) stück Größe : . , 
        Portion Packung Stück Bund Stiel Dose Rewe % D Cl C. B. Welt 
        glas l Dr. Oetker kg z.b. z.b Ml Abtr.gew Minute Foto Zubereitung Hamburg Monat
    """.lower().split()

    words=[word.lower() for word in words if word.lower() not in blacklist and cst_token_test(word)]
    return words
    
def cst_tokenize_stem(text):
    words = nltk.tokenize.word_tokenize(text, language="german")
    blacklist = """
        g el zutat zutaten für ca person personen m ( ) stück Größe : . , 
        Portion Packung Stück Bund Stiel Dose Rewe % D Cl C. B. Welt 
        glas l Dr. Oetker kg z.b. z.b Ml Abtr.gew Minute Foto Zubereitung Hamburg Monat
    """.lower().split()

    words=[stem(word).lower() for word in words if word.lower() not in blacklist and cst_token_test(word)]
    return words

def stem(a):
    print(a)
    for t in spacy_nlp.tokenizer(a):
        print(t,t.lemma_)
        return t.lemma_

def stem_en(a):
    p = nltk.PorterStemmer()
    return str(p.stem(a))

class EpochSaver(CallbackAny2Vec):
    '''Callback to save model after each epoch.'''

    def __init__(self, path_prefix):
        self.path_prefix = path_prefix
        self.epoch = 0
        self.logger = None

    def on_epoch_end(self, model):
        if self.epoch % 10 == 0:
            #output_path = get_tmpfile('{}_epoch{}.model'.format(self.path_prefix, self.epoch))
            output_path = '{}_epoch{}.model'.format(self.path_prefix, self.epoch)
            model.save(output_path)
            print("-"*100)
            print("SAVING MODEL:", output_path)
        self.epoch += 1

def generateHTMLView(DIR, MODEL):
#DIR = "lda_100i50p_Z/"
#MODEL = "lda_100i50p.model"
    with open(DIR+"_data.pkl", "rb") as a_file:
        sentences_lemmatized = pickle.load(a_file)
    dictionary = corpora.Dictionary.load(DIR+'_gensim.dict')

    corpus =[dictionary.doc2bow(text) for text in sentences_lemmatized]

    doc_id = 0
    doc, doc_raw = corpus[doc_id], sentences_lemmatized[doc_id]
    print(doc_raw)

    lda = models.LdaModel.load(DIR+MODEL)



    vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_html(vis, DIR+'lda.html')