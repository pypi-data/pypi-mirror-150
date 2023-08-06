import requests
import decouple
import json


class RasaEventBroker():
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = decouple.config("API_URL")

    def insert_entities_text(self, text, entities):
        for entity in entities:
            entity["text"] = text[entity["start"]:entity["end"]]
        return entities

    def check_duplicate_entities(self, entities):
        entities_start = list()
        new_entities = list()
        entities = sorted(entities, key=lambda entity: entity['start'])
        for entity in entities:
            if entity["start"] not in entities_start:
                entities_start.append(entity["start"])
                new_entities.append(entity)
        return new_entities

    def publish(self, event):
        url = f"{self.api_url}/track"
        params = {
            "apiKey": self.api_key,
            "platform": "rasa"
        }
        if event['event'] == 'user':
            text = event['text']
            new_text = text
            event['parse_data']['entities'] = self.insert_entities_text(text, event["parse_data"]["entities"])
            entities = self.check_duplicate_entities(event['parse_data']['entities'])
            event['handled'] = event['parse_data']['intent']['name'] != 'nlu_fallback'
            for entity in entities:
                dict_entity = {'entity': entity['entity'], 'value': entity['value']}
                new_text = new_text.replace(entity["text"], f"[{entity['text']}]{json.dumps(dict_entity)}", 1)
            event['text'] = new_text
        if event['event'] in ['session_started', 'user', 'bot']:
            requests.post(url, params=params, json=event)

    @classmethod
    def from_endpoint_config(cls, broker_config):
        if broker_config is None:
            return None
        return cls(**broker_config.kwargs)
