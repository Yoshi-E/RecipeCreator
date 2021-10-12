from gensim import matutils, models, corpora
import sys
import numpy as np
import json
from functools import singledispatch
import pickle
import os
NLP_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../../NLP/"))+"/" #"F:/Git/NLP/NLP/"
sys.path.append(NLP_PATH)
import NLP

from HanTa import HanoverTagger as ht


class TopicManager():
    def __init__(self):
        self.DIR = "lda_100i30p40t_Z/"  #"lda_model2_I/lda.model"
        self.MODEL = "lda_100i30p40t.model"
        self.lda_model = models.LdaModel.load(NLP_PATH+self.DIR+self.MODEL)
        self.tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        self.gensim_dict = corpora.Dictionary.load(NLP_PATH+self.DIR+'_gensim.dict')
        
        if os.path.exists(NLP_PATH+self.DIR+'recipe_topics.pickle'):
            with open(NLP_PATH+self.DIR+'recipe_topics.pickle', "rb") as a_file:
                self.recipe_topics = pickle.load(a_file)

    def _getBow(self, text):
        sentences_tok = NLP.cst_tokenize(text)

        tags = self.tagger.tag_sent(sentences_tok) 
        nouns = [lemma for (word,lemma,pos) in tags if pos == "NN" or pos == "NE"]
        return self.gensim_dict.doc2bow(nouns)


    def getTopic(self, text):
        bow =  self._getBow(text)
        topics = self.lda_model.get_document_topics(bow, minimum_probability=0.20)
        topics.sort(key=lambda tup: tup[1], reverse=True)
        
        _topics = []
        for topic, prob in topics:
            _topics.append((topic, prob, self.lda_model.show_topic(topic)))

        return _topics

    def getTopicRecipes(self, topicID: int, limit=10):
        recipes = [] 
        for recipe, prob in self.recipe_topics[topicID][:limit]:
            recipes.append(recipe)
        return recipes

    @singledispatch
    def to_serializable(val):
        """Used by default."""
        return str(val)


    @to_serializable.register(np.float32)
    def ts_float32(val):
        """Used if *val* is an instance of numpy.float32."""
        return np.float64(val)


if __name__ == "__main__":
    tm = TopicManager()

    text ="""
Zutaten für ca. 10 Stücke:
175 g Mehl
125 g gemahlene Haferflocken (Hafermehl)
Salz
300 g kalte Butter
1 Eigelb (Größe M)
5 Eier (Größe M)
2 TL Golden Syrup
100 g + 2 EL kernige Haferflocken
Fett für die Form
"""
    print(len(tm.recipe_topics[0]))
    #print(tm.getTopic(text))