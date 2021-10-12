
import difflib
#import pymysql
from Webserver.static.py.Config import Config
from Webserver.static.py.Log import log
from Webserver.static.py.RecipeManager.unitsManager import Unit
from . import Database
import unicodedata
import re
from functools import lru_cache
#from RecipeManager.database.unitsManager import Unit

class DatabaseIngredients(Database):
    def __init__(self):
        cfg = Config("Webserver\static\config\database.json",
                     "Webserver\static\config\database.json_default")
        super().__init__(cfg)

        self.setup_dict()

    def setup_dict(self):
        data = self.exe_sql("SELECT `name_de` FROM bls.bls;")
        print("Found", len(data), "ingredients")
        self.ingredients = []
        self.dict = set()
        self.dict_lower = set()
        for e in data:
            name = e["name_de"]
            self.ingredients.append(name)
            
            for i in name.replace("(", "").replace(")", "").replace(",", "").split(" "):
                if(not i.isdigit()):
                    self.dict.add(i)
                    self.dict_lower.add(i.lower())
        
        #remove unwanted from set:
        unwanted = ["", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
                    "für", "einen", "einer", "und", "mit", "a", "einfach"]
        for e in unwanted:
            if(e in self.dict):
                self.dict.remove(e)
            if(e.lower() in self.dict_lower):
                self.dict_lower.remove(e.lower())
        
        #Get column map
        self.column_map = {"name_de": "Zutat"}
        map = self.exe_sql("SELECT * FROM bls.bls_column;")
        for e in map:
            self.column_map[str(e["column"])] = e["name"]


    @lru_cache(maxsize=128)
    def suggest_word(self, word, n=10, cutoff=0.6):
        return difflib.get_close_matches(word.lower(), self.dict_lower, n=n, cutoff=cutoff)

    @lru_cache(maxsize=128)
    def ingredient_search(self, text, broadSearch=False):
        fields = ["name_de", "0", "6", "29", "54", "138"]
        #Closest match --> Starting with --> somewhere in text.
        limit = 20
        result = {"fields": fields, "data": [], "column_map": self.column_map}
        # ingredients = difflib.get_close_matches(text, self.ingredients, n=limit, cutoff=0.6)
        # if(len(ingredients)>0):
            # return {"data": ingredients}
        
        if(len(text.strip()) <= 2):
            return result
        
        sql = "SELECT {} FROM bls.bls WHERE name_de LIKE ".format("`"+"`,`".join(fields)+"`")
        sql += "'{0}' ORDER BY -bls.levenshtein(name_de, '{0}') DESC LIMIT {1};".format("{0}", limit)
        #print(sql)
        if(broadSearch):
            ingredients = self.exe_sql(sql.format(text+"%"))
            if(len(ingredients)>0):
                result["data"] = ingredients
                return result
        
        ingredients = self.exe_sql(sql.format("%"+text+"%"))
        if(len(ingredients)>0):
            result["data"] = ingredients
        
        return result

    def process_input(self, text):
        lines = text.splitlines()
        words = []
        data = []
        for line in lines:
            if(line.strip() == ""):
                continue
            data.append(self.process_line(line.strip()))
            words += line.split(" ")

        s = set()
        for word in words:
            suggestions = self.suggest_word(word, cutoff=0.95)
            if len(suggestions)>0:
                s.add(unicodedata.normalize("NFKC", word))
        return {"data": data, "column_map": self.column_map}

    @lru_cache(maxsize=128)
    def process_line(self, line):
        line = lineObj(unicodedata.normalize("NFKC", line).strip())
        line.processed = re.compile(r"\s*\([^)]*\)").sub("", str(line)) #.rstrip()
        
        
        #Step 1: Get the amound and unit from the text line
        #print(Unit.unit_regex())
        m = re.search(Unit.unit_regex(), str(line))
        self.regex_mapping(line, m)
        unitD = None
        valueD = None

        if(line.value and line.unit):
            line_unit = Unit(line.value, line.unit)
            unitD = line_unit.unit
            valueD = line_unit.value

            line_unit.convert("g")
            
            line.value = line_unit.value
            line.unit = line_unit.unit
        
        #If no unit and value was found, only look for value:
        if(not line.value):
            m = re.search(Unit.num_regex(), str(line))
            self.regex_mapping(line, m)
            unitD = line.unit

        #Step 2: Get look up the ingredient in the database
        data = self.db_lookup(line)
        if(data):
            line.bls_data = data[0] #Closest match

        #Step 3: Build result:
        confidence = 0
        value=unit=ingredient = None
        
        if(line.value):
            value = line.value
        else:
            value = 1
            
        if(line.unit):
            unit = line.unit

        if line.bls_data:
            if(not line.unit):
                unit = "DEFAULT_AVRG"
                
            if("name_de" in line.bls_data):
                ingredient = line.bls_data["name_de"]
            else:  
                ingredient = None
            if(line.ingredient):
                confidence = difflib.SequenceMatcher(None, line.ingredient, line.bls_data["name_de"]).ratio()
            else:
                confidence = difflib.SequenceMatcher(None, line.processed, line.bls_data["name_de"]).ratio()
            #Calculate default value for items with no unit:
            if(line.bls_data and unit=="DEFAULT_AVRG"):
                unit = "g"
                value = line.bls_data["138"] * value #Mittlere Portionsgröße g/Port

        #Step 4: Display the and build results
        name = "{} {} {}".format(value, unit, ingredient)


        result = {  "original": line.line,
                    "value": value,
                    "unit": unit,
                    "valueD": valueD,
                    "unitD": unitD,
                    "ingredient": ingredient,
                    "confidence": confidence,
                    "data": line.bls_data
                }
        print(line.line.ljust(45), "{} {} {}".format(line.value, line.unit, line.ingredient).ljust(45), name, confidence)
        return result

    def regex_mapping(self, line, regex):
        if not regex:
            return
        m = regex.groupdict()
        if("value" in m and m["value"]):
            line.value = int(regex.group("value"))   
        if("valueA" in m and m["valueA"]):
            if(m["symbol"] == "/"):
                line.value = int(m["valueA"]) / int(m["valueB"])    
            elif(m["symbol"] in ["–", "-", "–"]):
                line.value = (int(m["valueA"]) + int(m["valueB"])) / 2
            else:
                raise Exception("unknown symbol '' for line '{}'".format(m["symbol"], line))
        if("unit" in m):
            line.unit = regex.group("unit")        
        if("ingredient" in m):
            line.ingredient = regex.group("ingredient")

            #Acess the database to look up the item
    def db_lookup(self, line):
        #TODO
        #Compare "matchrate" of words, and search for possibly better results 
        #e.g. Mark von 1/2 Vanilleschote -->  Mark vs Vanilleschote
        #1 Spalte (ca. 600 g) Muskatkürbis --> not working
        #1 TL Speisestärke --> not working
        #Mapping: Milch --> Kuhmilch, Blaubeeren --> Heidelbeeren, Möhren --> Karotten
        # Weizenmehl --> weizenmehl
        if(line.ingredient):
            #1. Search for the full string
            fields = ["*"]
            sql = "SELECT {} FROM bls.bls WHERE name_de LIKE ".format("`"+"`,`".join(fields)+"`")
            sql += "'{0}' ORDER BY -bls.levenshtein(name_de, '{0}') DESC LIMIT {1};".format("{0}", 1) #limit to 1 for now
            data = self.exe_sql(sql.format(line.ingredient+"%"))
            #print(sql.format(line.ingredient+"%"))
            if(len(data)>0):
                bls_id = data[0]["name_de"]
                return data
            else:
                #Search for each subword
                for e in line.ingredient.split(" "):
                    data = self.exe_sql(sql.format(e+"%"))
                    if(len(data)>0):
                        bls_id = data[0]["name_de"]
                        return data   
                        
                for e in line.ingredient.split(" "):
                    data = self.exe_sql(sql.format("%"+e+"%"))
                    if(len(data)>0):
                        bls_id = data[0]["name_de"]
                        return data    
                        
        fields = ["*"]
        distance = 4
        sql = "SELECT {} FROM bls.bls WHERE name_de LIKE ".format("`"+"`,`".join(fields)+"`")
        sql += "'{0}' ORDER BY -bls.levenshtein(name_de, '{0}') DESC LIMIT {1};".format("{0}", 1) #limit to 1 for now
        for e in line.processed.split(" "):
            if(not e.isnumeric()):
                data = self.exe_sql(sql.format(e+"%"))
                if(len(data)>0):
                    bls_id = data[0]["name_de"]
                    return data    
                    
        sql = 'SELECT {} FROM bls.bls WHERE SOUNDEX(name_de) LIKE '
        sql = sql.format("`"+"`,`".join(fields)+"`")
        sql += 'SOUNDEX("{0}") AND bls.levenshtein(name_de, "{0}")<=4 ORDER BY -bls.levenshtein(name_de, "{0}") DESC LIMIT {1};'.format("{0}", 1) #limit to 1 for now
        for e in line.processed.split(" "):
            if(not e.isnumeric()):
                data = self.exe_sql(sql.format(e))
                if(len(data)>0):
                    bls_id = data[0]["name_de"]
                    return data     
        return None

    def recipe_search(self, search):
        sql = f"""SELECT * 
                FROM bauermedia.recipes 
                WHERE 
                  (recipes.recipe_id = '{search}' OR
					recipes.dc_id LIKE '{search}'	)
                OR title LIKE '%{search}%'
				OR dc_id IN (
					SELECT dc_id FROM bauermedia.recipes WHERE recipe_id IN (
                        SELECT recipe_id FROM bauermedia.recipes_tags WHERE tag_id 
							IN (SELECT tag_id FROM bauermedia.tags WHERE name LIKE '{search}')))
                LIMIT 25
            """
        data = self.exe_sql(sql)
        return data

class lineObj():
    def __init__(self, line: str):
        #Original Text line
        self.line = line
        #All Brackets: (content)
        self.brackets = re.findall(r"\s*\(([^)]*)\)", line)
        #List of stuff remove from the line
        self.clutter = None
        #Line without Brackets
        self.processed = None #re.compile(r"\s*\([^)]*\)").sub("", line)
        
        #.rstrip()
        self.value = None
        self.unit = None
        self.ingredient = None
        self.bls_data = None
    
    def __repr__(self): 
        return "lineObj({})".format(self.line)
        
    def __str__(self): 
        return str(self.line)
        
    def __add__(self, item): 
        return self.line + item 
        
    def __contains__(self, item):
        return item in self.line