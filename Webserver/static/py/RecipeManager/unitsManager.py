class Unit():
    #based on: 
    #https://www.chefkoch.de/magazin/artikel/500,0/Chefkoch/Ratgeber-Gewichte-und-Masseinheiten.html
    
    
    #mass in gramms
    dict_mass = {
        "mg": {"name": "Milligramm",    "short": "mg", "ratio": 0.001},
        "g": {"name": "Gramm",          "short": "g",  "ratio": 1},
        "pfd": {"name": "Pfund",        "short": "pfd","ratio": 500 },
        "kg": {"name": "Kilogramm",     "short": "kg", "ratio": 1000  },
        "Pr": {"name": "Prise",         "short": "Pr", "ratio": 0.04 },
        "Msp": {"name": "Messerspitze", "short": "Msp", "ratio": 0.25 },
        "TL": {"name": "Teelöffel",     "short": "TL", "ratio": 5 },
        "EL": {"name": "Esslöffel",     "short": "EL", "ratio": 15 },
        "Tas": {"name": "Tasse",        "short": "Tas", "ratio": 120 },
        "Bd": {"name": "Bund",          "short": "Bd", "ratio": 50 },
        "Sc": {"name": "Scheibe",       "short": "Sc", "ratio": 30 }
    }          
    
    #in ml
    dict_liquid = {
        "L": {"name": "Liter",          "short": "L", "ratio": 1000},
        "ml": {"name": "Milliliter",    "short": "ml", "ratio": 1},
        "cl": {"name": "Zentiliter",    "short": "ml", "ratio": 10},
        "dl": {"name": "Deziliter",     "short": "dl", "ratio": 100},
        "EL": {"name": "Esslöffel",     "short": "EL", "ratio": 10},
        "TL": {"name": "Teelöffel",     "short": "TL", "ratio": 5},
        "Tasse": {"name": "Tasse",      "short": "Tasse", "ratio": 125},
        "Schnapsglas": {"name": "Schnapsglas", "short": "Schnapsglas", "ratio": 20}
    }     
    units = set(list(dict_mass.keys()) + list(dict_liquid.keys())) 
    
    #per 100g of good in g
    raw_goods_prepared = {
        #fruit
        "Kiwi": 87,
        "Mandarine": 65,
        "Mango": 69,
        "Pfirsich": 92,
        "Pflaume": 94,
        "Orange": 72,
        "Wassermelone": 44,
        "Weintraube": 96,
        "Apfel": 85,
        "Banane": 67,
        "Birne": 90,
        "Erdbeere": 97,
        "Grapefruit": 66,
        "Honigmelone": 80,
        "Johannisbeere": 98,
        "Kirsche": 89,
        #vegetables
        "Aubergine": 83,
        "Stangensellerie": 63,
        "Blumenkohl": 62,
        "Grüne Bohnen": 94,
        "Brokkoli": 61,
        "Champignons": 98,
        "Chinakohl": 79,
        "Chicoree": 89,
        "Fenchel": 93,
        "Kartoffel": 80,
        "Wirsingkohl": 72,
        "Zwiebel": 92,
        "Kohlrabi": 66,
        "Möhren": 81,
        "Paprikaschoten": 77,
        "Porree": 58,
        "Lauch": 58,
        "Radieschen": 63,
        "Rosenkohl": 78,
        "Salatgurke": 74,
        "Spargel": 74,
        "Spinat": 85,
        "Tomate": 96,
        "Zucchini": 87
    }
    
    #name: [tee_spoon, spoon] in g
    level_spoon = {
        "Backpulver": [3, 10],
        "Bratensoße": [3, 8],
        "Brühe": [3, 8],
        "Butter": [4, 10],
        "Creme fraiche": [5, 15],
        "Fruchtzucker": [4, 12],
        "Graupen": [10, 18],
        "Grieß": [4, 12],
        "Gewürze": [2, 7],
        "Haferflocken": [3, 8],
        "Honig": [10, 20],
        "Kaffeepulver": [2, 6],
        "Kaffeesahne": [5, 15],
        "Kakaopulver": [2, 5],
        "Käse": [3, 8],
        "Marmelade": [6, 16],
        "Konfitüre": [6, 16],
        "Kräuter": [2, 4],
        "Mandeln": [3, 8],
        "Margarine": [4, 10],
        "Mayonnaise": [4, 12],
        "Mehl": [3, 10],
        "Milch": [5, 15],
        "Öl": [3, 10],
        "Puddingpulver": [3, 10],
        "Puderzucker": [3, 10],
        "sauer Sahne": [5, 13],
        "süß Sahne": [5, 13],
        "Salz": [5, 15],
        "Senf": [5, 9],
        "Semmelmehl": [4, 12],
        "Speisestärke": [3, 9],
        "Tomatenmark": [5, 15],
        "Zucker": [5, 15]
    }
    
    #in g
    standard_sizes = {
        "Scheibe Brot": 40 ,
        "Toastbrot": 30,
        "Scheibe Weißbrot": 30,
        "Scheibe Knäckebrot": 9,
        "Brötchen": 45,
        "Zwieback": 8,
        "Scheibe Käse": 30,
        "dünne Scheibe Käse": 20,
        "dicke Scheibe Käse": 40,
        "Schinken": 35,
        "dünne Schinken": 25,
        "gekochter Schinken": 45,
        "Cornedbeef": 27,
        "Roastbeef": 30,
        "Salami": 5,
        "Quark": 30,
        "kleiner Apfel": 115,
        "mittelgroßer Apfel": 135,
        "Apfel": 135,
        "großer Apfel": 200,
        "Birne": 150,
        "kleine Birne": 100,
        "große Birne": 200,
        "Orange": 170,
        "Grapefruit": 350,
        "Pampelmuse": 350,
        "Pfirsich": 110,
        "kleiner Pfirsich": 75,
        "mittelgroßer Pfirsich": 100,
        "großer Pfirsich": 150,
        "Tomate": 50,
        "Gemüsetomate": 220,
        "Salatgurke": 400,
        "Zwiebel": 50,
        "Würfelzucker": 4,
        "Bund Radieschen": 50
    }
    
    #in g für tassen
    standard_sizes_cup = {
        "Zucker": 180,
        "Mehl": 105 ,
        "Semmelmehl": 130 ,
        "Grieß": 150
    }
    
    def __init__(self, value, unit):
        self.value = value
        
        #convert full name b_unit int shot form
        for key,val in Unit.dict_mass.items():
            if(val["name"] == unit or val["name"] == unit[:-1]):
                unit = val["short"]       
        for key,val in Unit.dict_liquid.items():
            if(val["name"] == unit or val["name"] == unit[:-1]):
                unit = val["short"]
        
        if unit in Unit.units:
            self.unit = unit
        else: 
            raise Exception("Invalid unit '{}'".format(unit))
            
    def __repr__(self):
        return "Unit({} {})".format(self.value, self.unit) 
        
    def __str__(self):
        return "{} {}".format(self.value, self.unit)
    
    def __copy__(self):
        return Unit(self.value, self.unit)    
        
    def copy(self):
        return Unit(self.value, self.unit)
        
    def convert(self, b_unit):
        if self.value == 0: 
            return 0
        
        if not b_unit in Unit.units:
            raise Exception("Invalid unit '{}'".format(b_unit))

        result = {"old_value": self.value, "old_unit": self.unit, "new_value": None, "new_unit": b_unit}
        
        #if type is mass, 
        if(b_unit in Unit.dict_mass.keys()):
            #convert to gramm first:
            if(self.unit == "g"):
                gramm = self.value
            else:
                if(self.unit in Unit.dict_mass.keys()):
                    gramm = Unit.dict_mass[self.unit]["ratio"] * self.value
                elif(self.unit in Unit.dict_liquid.keys()):
                    gramm = Unit.dict_liquid[self.unit]["ratio"] * self.value #TODO: Warning Liquid density not taken into account
                
            self.value = gramm / Unit.dict_mass[b_unit]["ratio"]
            self.unit = b_unit
            result["new_value"] = self.value
        else:
            #is liquid
            pass
        return result
    

    re_value = r"(((?P<valueA>[0-9]+)(?P<symbol>\/|-|–|–)(?P<valueB>[0-9]+))|(?P<value>[0-9]+))" #matches 1-2 or 1/4
    
    def unit_regex():
        #TODO: 1,2 kg --> comma numbers
        #TODO:  normalization decomposition?
        
        #build units list:
        units = []
        units += [e.replace(" ", "\s") for e in Unit.units]
        units += [v["name"].replace(" ", "\s") for k,v in Unit.dict_mass.items()]
        units += [v["name"].replace(" ", "\s") for k,v in Unit.dict_liquid.items()]
        #units += [e.replace(" ", "\s") for e in Unit.standard_sizes.keys()]
        #units += [e.replace(" ", "\s") for e in Unit.raw_goods_prepared.keys()]

        
        re_unit = r"(?P<unit>{})".format("n*|".join(units)+"n*")
        re_ingrients = r"(?P<ingredient>.*)"

        for key,val in Unit.dict_mass.items():
            units.append(val["name"].replace(" ", "\s"))        
        for key,val in Unit.dict_liquid.items():
            units.append(val["name"].replace(" ", "\s"))
            
        return Unit.re_value+"\s*"+re_unit+"\s+"+re_ingrients
        
        #r"([0-9]*)\s*([a-zA-Z]{1,4})\s+(.*)" #100 g Zucker
        
    def num_regex():
        return Unit.re_value
        
        
        
        #Killoklaorien
        #KJ 
        #Fett
        #Eiweiss
        #Kohlenhyrdate
        #
"""
Common pattern:

100 g Zucker
1 Ei
knapp 1 TL Kakaopulver
Mehl für die Arbeitsfläche
ca. 1/4 l laktosefreie Milch
1 Würfel (42 g) Hefe
500 g Mehl (Type 1050)
1 TL Salz
1 gestrichener TL Backpulver
1 1/2 EL Rosinen
1-2 EL Limettensaft
250 g + 3 EL Zucker

#Val Unit Ingiredient
^([0-9]*)\s+(.*?)\s+(.*)
"""