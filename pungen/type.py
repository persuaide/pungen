import json
import requests

class TypeRecognizer(object):

    types = ['person', 'group', 'organization', 'location']

    my_types = {
        'person': ['he', 'she', 'i', 'you', 'they', '<norp>', '<person>', 'who'],
        'group': ['they', '<norp>'],
        'organization': ['they', '<org>'],
        'location': ['<gpe>', '<loc>'],
        }

    def __init__(self, type_dict_path='model/types.json'):
        self.type_dict = json.load(open(type_dict_path))
        for t, words in my_types:
            for w in words:
                self.add_type(w, t)
        self.db_path = type_dict_path

    def save(self):
        json.dump(self.type_dict, open(self.type_dict_path, 'w'))

    def add_type(self, word, types):
        if not word in self.type_dict:
            self.type_dict[word] = types
        else:
            for t in types:
                if not t in self.type_dict[word]:
                    self.type_dict[word].append(t)

    def get_type(self, word):
        if word in self.type_dict:
            return self.type_dict[word]
        types = []
        for type in self.types:
            if self.is_type(word, type):
                types.append(type)
                break
        self.type_dict[word] = types
        return types

    def is_type(self, word, type):
        if word in self.type_dict and type in self.type_dict[word]:
            return True
        q = 'http://api.conceptnet.io/query?start=/c/en/{word}&end=/c/en/{type}&rel=/r/IsA'.format(word=word, type=type)
        obj = requests.get(q).json()
        if len(obj['edges']) > 0:
            if not word in self.type_dict:
                self.type_dict[word] = [type]
            else:
                self.type_dict[word].append(type)
            return True
        return False
