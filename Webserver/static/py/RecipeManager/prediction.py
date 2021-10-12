
"""
General concept:

Input:
    List of Ingredients

Output: 
    New Ingredient for the list

e.g.:
    Input:
        [Mehl, Zucker]
    Output:
        "Milch"

"""
import nltk
import re
from gensim.models.callbacks import CallbackAny2Vec
from gensim import models, corpora
import pickle
import pyLDAvis
#from pyLDAvis import gensim
import sys
import os
from HanTa import HanoverTagger as ht
NLP_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../NLP/"))+"/"
sys.path.append(NLP_PATH)
import NLP
from Webserver.static.py.RecipeManager.database import DatabaseIngredients
import difflib

class IngredientGenerator():
    def __init__(self):
        self.DIR = "lda_100i30p40t_Z/"  #"lda_model2_I/lda.model"
        self.MODEL = "lda_100i30p40t.model"
        self.lda_model = models.LdaModel.load(NLP_PATH+self.DIR+self.MODEL)
        self.tagger = ht.HanoverTagger('morphmodel_ger.pgz')
        self.gensim_dict = corpora.Dictionary.load(NLP_PATH+self.DIR+'_gensim.dict')
        self.DI = DatabaseIngredients()

        if os.path.exists(NLP_PATH+self.DIR+'recipe_topics.pickle'):
            with open(NLP_PATH+self.DIR+'recipe_topics.pickle', "rb") as a_file:
                self.recipe_topics = pickle.load(a_file)

    def _getBow(self, text):
        sentences_tok = NLP.cst_tokenize(text)

        tags = self.tagger.tag_sent(sentences_tok) 
        nouns = [lemma for (word,lemma,pos) in tags if pos == "NN" or pos == "NE"]
        return self.gensim_dict.doc2bow(nouns)


    def getTopic(self, text, prob=0.20):
        bow =  self._getBow(text)
        topics = self.lda_model.get_document_topics(bow, minimum_probability=prob)
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

    # TODO
    # Connect to internal DB
    # test if ingredient is in list of known ingredients
    def isIngredient(self, ingredient):
        return True


    def suggest(self, ingredients=None):
        if not ingredients:
            ingredients = []

        for topic in self.getTopic(ingredients):
            print("-"*50)
            for word in topic[2]:
                print(word)

        return None   
        
    def predict(self, ingredients=None):
        if not ingredients:
            ingredients = []

        predicted = []
        ingredients_tk = NLP.cst_tokenize(ingredients)
        for topic in self.getTopic(ingredients, prob=0.05):
            for word in topic[2]:
                wordtk = NLP.cst_tokenize(word[0])
                if word[0] not in ingredients and \
                wordtk and wordtk[0] not in ingredients_tk:
                    r = self.DI.ingredient_search(word[0])
                    if len(r["data"]) > 0:
                        ratio = difflib.SequenceMatcher(None, word[0], r["data"][0]["name_de"]).ratio()
                        print(word[0], r["data"][0]["name_de"], ratio)
                        if ratio > 0.6:
                            predicted.append(word[0])
                    else:
                        print(word[0], "-")

        return predicted

if __name__ == "__main__":
    ig = IngredientGenerator()
    print(ig.predict("Tomate Brot Salz"))

    """
    Examples:
        Limo: http://bergter.com:8011/api/editor/prediction?text=Pfefferminze%0Agr%C3%BCner%20Tee%0AZucker%0AZitronen%0AMineralwasser%0AEisw%C3%BCrfel
        Kuchen: http://bergter.com:8011/api/editor/prediction?text=Mehl%0ABackpulver%20%0AButter%20%0AEi%0ASalz%0ARosinen%0A%C3%84pfel%0AZimt%0APuderzucker%0AZitronensaft%0AFett%20f%C3%BCr%20die%20Form

    """
