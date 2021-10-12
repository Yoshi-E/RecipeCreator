import os
from glob import glob


NLP_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../../../NLP/"))+"/" #"F:/Git/NLP/NLP/"

def getLDAModels():
    models = {}
    for model in glob(NLP_PATH+"*/*.html"):
        model = model.replace("\\", "/").replace(NLP_PATH, "")
        dir = os.path.dirname(model)
        models.setdefault(dir, [])
        models[dir].append(model)
        for image in glob(NLP_PATH+dir+"/*.png"):
            models[dir].append(image.replace("\\", "/").replace(NLP_PATH, ""))

    return models
    
