from json import encoder
from Webserver import app
from Webserver.static.py.RecipeManager.database import DatabaseIngredients
from Webserver.static.py.RecipeManager import database
from Webserver.static.py.RecipeManager.database import db
from Webserver.static.py.RecipeManager.recipe import Recipe
from Webserver.static.py.RecipeManager.prediction import IngredientGenerator
from Webserver.static.py import NLPManager
from flask import jsonify, abort, make_response, request, Response
from flask_restx import Namespace, Resource, fields, reqparse

namespace = Namespace('editor', 'editor')

import unicodedata
import json

dh = database.DatabaseIngredients()
tm = database.TopicManager()
ig = IngredientGenerator()

@namespace.route('/suggestWord/<word>')
class suggestWord(Resource):
    def get(self, word):
        """
        Suggest an ingredient with the highest levenshtein similarity 
        """
        if word == "":
            abort(404)
        return jsonify({"response": dh.suggest_word(word)})
    
@namespace.route('/searchIngredient/<word>')
class searchIngredient(Resource):
    def get(self, word):
        """
        Predicts the most likely simlar / matching ingredient
        """
        if word == "":
            abort(404)
        return jsonify(dh.ingredient_search(word))
    
@namespace.route('/searchRecipe/<word>')
class searchRecipe(Resource):
    def get(self, word):
        """
        Searches in the database for recipes matching the query
        """
        if word == "":
            abort(404)
        return jsonify(dh.recipe_search(word))


model_BLS_data = namespace.model('model_BLS_data', {
    "BLS_key": fields.String(description="BLS id key"),
    "name_de": fields.String(description="The ingredient name in german"),
    "name_en": fields.String(description="The ingredient name in english"),
})

model_processLine = namespace.model('model_processLine', {
    "confidence": fields.Float(min=0, max=1, description="Confidence of the detection"),
    "ingredient": fields.String(description="The ingredient that is assumed to match the given line"),
    "data": fields.String(description="BLS data for the detected ingredient"),
    "original": fields.String(description="The original input"),
    "unitD": fields.String(description="The type of unit that was detected for the given line"),
    "value": fields.Integer(description="The normalized quantity value that was derived from valueD"),
    "valueD": fields.Integer(description="The quantity value that was detected in the given line")
})

model_response1 = namespace.model('model_response1', {
    "response": fields.Nested(model_processLine) #, description="Geschäftspartnerangaben für Belege", title="BusinessPartner"
})

@namespace.route('/processLine')
class processLine(Resource):
    @namespace.doc(params={'line': 'A single of a recipe'})
    @namespace.marshal_with(model_response1)
    def get(self):
        """
        Processes a single text line of a recipe
        """
        if "line" not in request.args:
            abort(404)
        return jsonify({"response": dh.process_line(request.args["line"])})


@namespace.route('/processIngredientInput')
class processIngredientInput(Resource):
    @namespace.doc(params={'recipe_text': 'Recipe text to be processed'})
    def get(self):
        """
        Processes an entire text block for a recipe 
        """
        if "recipe_text" not in request.args:
            abort(404)
        text = request.args["recipe_text"]
        data = dh.process_input(text)
        return jsonify(data)
    
@namespace.route('/recipe')
class recipe(Resource):
    @namespace.doc(params={'id': 'Return the recipe matching the id'})
    def get(self):
        """
        Get the recipe for a give nid
        """
        if "id" not in request.args:
            abort(404)
        id = request.args["id"]
        
        try:
            r = Recipe(id)
            return r.getDocument()
        except IndexError:
            abort(404)

@namespace.route('/recipeImage')
class recipeImage(Resource):
    @namespace.doc(params={'id': 'Return the recipe images matching the recipe id'})
    def get(self):
        """
        Get the images to a recipe
        """
        if "id" not in request.args:
            abort(404)
        id = request.args["id"]
        
        try:
            return jsonify(Recipe.getImagesFromID(id))
        except IndexError:
            abort(404)

@namespace.route('/topicRaw')
class topicRaw(Resource):
    @namespace.doc(params={'id': 'Returns a raw LDA topic spec', 'text': 'Returns a raw LDA topic spec matching the input text'})
    def get(self):
        """
        Get the raw LDA topic data for a given topic id or for a string
        """
        if "id" in request.args:
            id = request.args["id"]
            r = Recipe(id)
            text = r.getBody()["ZUTATEN"]
            return Response(json.dumps(tm.getTopic(text), default=database.TopicManager.to_serializable), mimetype='application/json')
        elif "text" in request.args:
            text = request.args["text"]
            return Response(json.dumps(tm.getTopic(text), default=database.TopicManager.to_serializable), mimetype='application/json')
        abort(404)

@namespace.route('/topicRecipes')
class topicRecipes(Resource):
    @namespace.doc(params={'id': 'Returns a list of recipes that match the given topic id'})
    def get(self):
        """
        Returns a list of recipes that match the given topic id
        """
        if "id" in request.args:
            id = int(request.args["id"])
            _list = []
            for recipe in tm.getTopicRecipes(id):
                r = Recipe(recipe)
                title = r.getBody()["TITEL"]
                _list.append((recipe, title))
            return jsonify(_list) #, default=database.TopicManager.to_serializable
        abort(404)
        

#model_prediction = namespace.model('model_prediction', {fields.String()})

@namespace.route('/prediction')
class makeIngredientSuggestion(Resource):
    @namespace.doc(params={'text': 'recipes text used to make a prediction based on the detected LDA topic'})
    @namespace.doc(responses={200: """['Ingredient1', 'Ingredient2', 'Ingredient3']"""})
    #@namespace.marshal_with(model_prediction, as_list=True)
    def get(self):
        """
        Makes a prediction based on the detected LDA topic
        """
        if "text" in request.args:
            text = str(request.args["text"])
            return jsonify(ig.predict(text))
        abort(404)

namespace2 = Namespace('lda', 'lda')

model_lda_models = namespace2.model('model_lda_models', {
    "lda_key": fields.List(fields.String())})


@namespace2.route('/models')
class getLDAModels(Resource):
    #@namespace2.marshal_with(model_lda_models, as_list=True)
    def get(self):
        """
        Returns a list of all trained LDA models
        """
        return jsonify(NLPManager.getLDAModels())
