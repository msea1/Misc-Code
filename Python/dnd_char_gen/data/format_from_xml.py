from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson
import json

from dnd_char_gen.background import Background
from dnd_char_gen.class_picker import CharClass
from dnd_char_gen.races import Race


class Universe:
    def __init__(self):
        self.data_folder = join(dirname(dirname(abspath(__file__))), 'data')
        self.data = {}
        self.sources = {}

    def load_data(self):
        self.sources['core'] = self.load_core()
        self.sources['eberron'] = self.load_eberron()
        self.sources['npc'] = self.load_npc_race_data()

    def combine_sources(self):
        self.data = self.sources['core']
        self.data['race'].update(self.sources['eberron']['race'])
        self.data['race'].update(self.sources['npc']['race'])
        self.data['background'].update(self.sources['eberron']['background'])

    def clean_up_data(self):
        self.data['race'] = self.match_race_to_already_existing(self.data['race'])
        self.data['background'] = self.combine_backgrounds(self.data['background'])

    @staticmethod
    def match_race_to_already_existing(all_races):
        attempt = {'Aasimar': [], 'Dragonborn': [], 'Dwarf': [], 'Elf': [], 'Genasi': [],
                   'Gnome': [], 'Halfling': [], 'Shifter': [], 'Warforged': []}  # todo, automate this
        to_process = []
        for r, v in all_races.items():
            if len(r.split()) == 1:
                attempt[r] = [v]
            else:
                to_process.append((r, v))
        for r, v in to_process:
            words = r.split()
            seen = False
            for w in words:
                if w in attempt:
                    attempt[w].append(v)
                    seen = True
                    break
            if not seen:
                attempt[r] = [v]
        return attempt

    @staticmethod
    def combine_backgrounds(backgrounds):
        temp = {'House Agent': []}
        for k, v in backgrounds.items():
            if 'House' not in k:
                temp[k] = [v]
            else:
                temp['House Agent'].append(v)
        return temp

    def output_data(self):
        with open(join(self.data_folder, 'source.json'), 'w') as fout:
            json.dump(self.data, fout)

    def load_core(self):
        with open(join(self.data_folder, 'Core.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        races = {x['name']: Race(**x) for x in json_data['race']}
        dnd_classes = {x['name']: CharClass(**x) for x in json_data['class']}
        bgs = {x['name']: Background(**x) for x in json_data['background']}
        # feats = {x['name']: x for x in json_data['feat']}
        # items = {x['name']: x for x in json_data['item']}
        # monsters = {x['name']: x for x in json_data['monster']}
        # spells = {x['name']: x for x in json_data['spell']}
        return {'race': races, 'class': dnd_classes, 'background': bgs}

    def load_eberron(self):
        with open(join(self.data_folder, 'EberronAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        races = {x['name']: Race(**x) for x in json_data['race']}
        bgs = {x['name']: Background(**x) for x in json_data['background']}
        return {'race': races, 'background': bgs}

    def load_npc_race_data(self):
        with open(join(self.data_folder, 'NPCRacesAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        races = {x['name']: Race(**x) for x in json_data['race']}
        return {'race': races}


if __name__ == '__main__':
    u = Universe()
    u.load_data()
    u.combine_sources()
    u.clean_up_data()
    u.output_data()
    print(u.data)
