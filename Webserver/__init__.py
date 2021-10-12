import os
os.environ['FLASK_ENV'] = "production" #'development'

from flask import Flask

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

import nltk
nltk.download('punkt')

from Webserver import routes
