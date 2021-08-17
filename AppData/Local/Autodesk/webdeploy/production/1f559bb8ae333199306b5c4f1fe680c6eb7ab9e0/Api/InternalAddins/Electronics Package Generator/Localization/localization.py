import os
import json

class Localization:

    def __init__(self, locale):
        
        global localeMessages

        with open(os.path.dirname(__file__) + '/' + locale + '.json', encoding="utf8") as locale_json:
            localeMessages = json.load(locale_json)  
        
    @staticmethod
    def getLocaleString(key, default_value):
        try:
            return localeMessages[key]
        except KeyError:
            return default_value