from Webserver import app
from flask import render_template
from flask import Flask, Markup
from flask import send_file, make_response, abort, jsonify, request, send_from_directory
import re
import os

#@app.route('/index')
#@app.route('/')
#def index():
#    return render_template('index.html', title='DevEnv')

# Custom static data
@app.route('/assets/<path:folder>/<path:filename>')
def custom_static(folder,filename):
    dir = "../Webserver/static/angular/assets/"+folder+"/"
    return send_from_directory(dir, filename)

#  Custom static data (Bauer)
@app.route('/bauercreate/images/<path:folder>/<path:filename>')
def custom_staticBauer(folder,filename):
    dir = "../NLP/bauercreate_nextmedia_devhw/images/"+folder+"/"
    return send_from_directory(dir, filename)

@app.route('/', defaults={'path': ''})
@app.route('/about')
def index(**kwargs):
    return make_response(open('Webserver/static/angular/index.html').read())


#  Custom static acess to images for LDA model
@app.route('/lda_model/<path:model>/<path:filename>')
def lda_model_image(model,filename):
    dir = f'../NLP/{model}/'
    return send_from_directory(dir, filename)

@app.route('/lda_model/<path:model>')
def lda_model(model):
    dir = f'../NLP/{model}/'
    return send_from_directory(dir, "lda.html")

@app.route('/response.json')
def jsonFile():
    return jsonify({"Cake": "Butter"})
    #return send_from_directory(os.path.abspath(os.path.dirname('countries.json')), 'countries.json')

@app.route('/<path:path>')
def pageNotFound(**kwargs):
    #print(kwargs)
    #print(request.args)
    return make_response(open('Webserver/static/angular/index.html').read())

@app.route('/template')
def test():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    test = Markup("<b>This is a test</b>")
    return render_template('test_index.html', title='Home', user=user, posts=posts, test={"cake": test})



from Webserver import rest