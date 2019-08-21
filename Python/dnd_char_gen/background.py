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

    def load_core(self):
        with open(join(self.data_folder, 'Core.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Background(**x) for x in json_data['background']}

    def load_eberron(self):
        with open(join(self.data_folder, 'EberronAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: x for x in json_data['background']}


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

from dnd_char_gen.utils import choose


def choose_random_bg():
    return uni.data[choose(list(uni.data), 1)[0]]


def compile_all_grades(abilities):
    return [x.grade(None) for x in uni.data]


picks = 1
choice = choose_random_bg()
print(choice)
print(f'Good at {choice.proficiency}')
