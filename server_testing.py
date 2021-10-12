from Webserver import app

if __name__ == '__main__':
    app.run(debug=False, port=8011, host="localhost")


    #TODO: Translation https://huggingface.co/t5-large