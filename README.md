
<p align="center">
 <img src="./RecipeWebAppFrontend/src/assets/icons/logo.svg" align="middle" width = "600"/>
<p align="center">

------------------------------------------------------------------------------------------
<p align="left">
    <a href=""><img src="https://img.shields.io/badge/python-3.6+-aff.svg"></a>
    <a href=""><img src="https://img.shields.io/badge/os-linux%2C%20win%2C%20mac-pink.svg"></a>
</p>

# RecipeWebApp
 A webbased app build to process and edit cooking recipies.
 Cooking recipes are something almost everybody knows, and will encounter on a regular basis in the mundane life.
However finding, managing and creating recipes is often a difficult and tedious task. Many, will simply use their notes app on their phone, or MS Word on their computer to write down the instructions and ingredients.

This project aims to explore technical methods, namly natural language processing, to process and aid in the creation and classification of cooking recipes.

# Live Demo (Fully Available until 30.10.2021, limited afterwards)

<h1><a href="https://recipe.bergter.com/">DEMO</a></h1>
<h1><a href="https://recipe.bergter.com/api/doc">Swagger Docs</a></h1>
<a href="https://eric.bergter.com/files/RecipeCreator.zip">Download Project with model files & Database (300mb, 3GB uncompressed)</a> Licenced Files (BLS, or the Recipies are not included)



------------------------------------------------------------------------------------------

# Technology used
- Frontend: Angular (CLI) / Typescript / JS
- Backend: Python 3.6
- Webserver: Flask, Flast-RestX (Documentation)
- NLP Libaries: gensim, pyLDAvis, nltk, spacy, tensorflow
- Other central utils: sqlite, mysql, re

# Features

- Text processing:
    - detection of ingredients
    - detection of units
    - detection and calculation of item quanity
    - parsing of brackets and parentheses
    - utilizes Stemming, Lemmatizer, Tokenizer
- Ingredient processing:
    - Identification
    - Finding best match
    - Match confidence
- User interface:
    - Basic functionality
    - Works in real time
    - REST API
    


# Requirements
- Python3 (Tested on 3.6 and 3.9)
- Linux / Win / OSX (Tested on Win10)

# Install
1. The Git Repo lacks the Database login and Models. The Full project can be downloaded above.
Alternativly just clone the repo.

2. Setup a virtual environment for python
```
python -m venv .venv
```
4. Activate the virtal environment

5. Install the python modules and requirements

```
python -m pip install -r requirements.txt

python -m spacy download en_core_web_sm

python -m spacy download de_core_news_sm
```

# Issues with libaries
Some Libaries had some issues, if you want to build your own models, you will most likeley need to do similar tweaks.

- For the LDA visualization you need to apply to following fix to the pyLDAvis package:
  
    In the file: pyLDAvis/_display.py:
    - replacing open() for urls with urllib.request (or manually paste the css code)