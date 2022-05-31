from utils import CadocsIntents
import requests

# the Intent Manager is used to detect the Intent behind an user's message
class IntentManager:
    def detect_intent(self, text):
        #
        # intent detection from our nlp model
        # it will return a text that will be transformed into the correspondent enum
        # it could also return the list of entities found in the text (repo link, date, etc)
        #

        x = requests.get('http://localhost:5000/predict?message=' + text)
        results = x.json()
        nlu_intent = results.get('intent').get('intent').get('name')
        nlu_intent_confidence = results.get('intent').get('intent').get('confidence')
        entities_list = results.get('entities')
        if len(entities_list) > 0:
            entities = [x for x in results.get('entities')[0] if x]
        else:
            entities = []
        print(nlu_intent, nlu_intent_confidence, entities)
        
        if nlu_intent == "report":
            return CadocsIntents.Report, [""]
        elif nlu_intent == "info":
            return CadocsIntents.Info, [""]
        elif nlu_intent == "get_smells":
            return CadocsIntents.GetSmells, entities
        elif nlu_intent == "get_smells_date":
            return CadocsIntents.GetSmellsDate, entities

