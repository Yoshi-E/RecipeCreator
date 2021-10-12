from Webserver import app
from waitress import serve

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8011, threads=6)
    #app.run(debug=False, port=8011, host="localhost")


    #TODO: Translation https://huggingface.co/t5-large