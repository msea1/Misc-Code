from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson

from dnd_char_gen.character import Race


class Universe:
    def __init__(self):
        self.data_folder = join(dirname(dirname(abspath(__file__))), 'data')
        self.data = {}

    def load_data(self):
        self.load_core()
        self.load_eberron()
        self.load_npc_race_data()

    def load_core(self):
        with open(join(self.data_folder, 'Core.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        bgs = {x['name']: x for x in json_data['background']}
        dnd_classes = {x['name']: x for x in json_data['class']}
        # feats = {x['name']: x for x in json_data['feat']}
        # items = {x['name']: x for x in json_data['item']}
        monsters = {x['name']: x for x in json_data['monster']}
        races = {x['name']: Race(**x) for x in json_data['race']}
        # spells = {x['name']: x for x in json_data['spell']}


    def load_eberron(self):
        with open(join(self.data_folder, 'EberronAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        bgs = {x['name']: x for x in json_data['background']}
        feats = {x['name']: x for x in json_data['feat']}
        items = {x['name']: x for x in json_data['item']}
        monsters = {x['name']: x for x in json_data['monster']}
        races = {x['name']: Race(**x) for x in json_data['race']}


    def load_npc_race_data(self):
        with open(join(self.data_folder, 'NPCRacesAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        races = {x['name']: Race(**x) for x in json_data['race']}
        return races
