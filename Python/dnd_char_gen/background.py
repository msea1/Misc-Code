from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson

"""
needed for start:
    
"""


class Background:
    def __init__(self, name, proficiency, trait):
        self.name = name
        self.proficiency = proficiency
        self.traits = trait

    def __str__(self):
        return self.name

    def parse_proficiency(self):
        self.proficiency = self.proficiency.replace('.', ',')
        self.proficiency = self.proficiency.split(', ') if self.proficiency else ''
        self.saving_throws = self.proficiency[:2]
        self.proficiency = self.proficiency[2:]
        self.proficiency = [(x, PROF_MAP[x]) for x in self.proficiency]

    def grade(self, input):
        return 0


class Universe:
    def __init__(self):
        self.data_folder = join(dirname(abspath(__file__)), 'data')
        self.data = {}

    def load_data(self):
        a = self.load_core()
        a.update(self.load_eberron())
        self.data = a
        self.combine_backgrounds()

    def load_core(self):
        with open(join(self.data_folder, 'Core.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Background(**x) for x in json_data['background']}

    def load_eberron(self):
        with open(join(self.data_folder, 'EberronAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Background(**x) for x in json_data['background']}

    def combine_backgrounds(self):
        temp = {'House Agent': []}
        for k, v in self.data.items():
            if 'House' not in k:
                temp[k] = [v]
            else:
                temp['House Agent'].append(v)
        self.data = temp

PROF_MAP = {
    'Animal Handling': "WIS",
    'Athletics': "STR",
    'Intimidation': "CHA",
    'Nature': "INT",
    'Perception': "WIS",
    'Survival': "WIS",
    'Acrobatics': "DEX",
    'Arcana': "INT",
    'Deception': "CHA",
    'History': "INT",
    'Insight': "WIS",
    'Investigation': "INT",
    'Medicine': "WIS",
    'Performance': "CHA",
    'Persuasion': "CHA",
    'Religion': "INT",
    'Sleight of Hand': "DEX",
    'Stealth': "DEX",
}

uni = Universe()
uni.load_data()

from dnd_char_gen.utils import choose, roll


def choose_random_bg():
    background = choose(list(uni.data), 1)[0]
    bg_list = uni.data[background]
    if len(bg_list) == 1:
        return bg_list[0]
    else:
        sub_i = roll(len(bg_list))
        return bg_list[sub_i-1]


def compile_all_grades(abilities):
    return [x.grade(None) for x in uni.data]


picks = 1
choice = choose_random_bg()
print(choice)
print(f'Good at {choice.proficiency}')
