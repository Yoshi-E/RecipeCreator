from gensim import matutils, models, corpora
import pickle
from NLP import *
import pyLDAvis
from pyLDAvis import gensim

DIR = "lda_100i50p_Z/"
MODEL = "lda_100i50p.model"
with open(DIR+"_data.pkl", "rb") as a_file:
    sentences_lemmatized = pickle.load(a_file)
dictionary = corpora.Dictionary.load(DIR+'_gensim.dict')

corpus =[dictionary.doc2bow(text) for text in sentences_lemmatized]

doc_id = 0
doc, doc_raw = corpus[doc_id], sentences_lemmatized[doc_id]
print(doc_raw)

lda = models.LdaModel.load(DIR+MODEL)

#topics = lda.get_document_topics(doc)
#print(topics)
for topic, rep in lda.show_topics(num_topics=100, formatted=False):
    words = []
    for word in rep:
        if(word[1] > 0.05):
            words.append(word[0])
    print(topic, " ,".join(words))

# https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/#14computemodelperplexityandcoherencescore
# Visualize model:
# fixing pyLDAvis:
# pyLDAvis\_display.py
# replacing open() for urls with urllib.request (or manually pasting the css code)
vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
pyLDAvis.save_html(vis, DIR+'lda.html')
#pyLDAvis.show(vis)