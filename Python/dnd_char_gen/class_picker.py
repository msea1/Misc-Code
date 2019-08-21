from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson

from dnd_char_gen.ability_roll import roll_ability

"""
needed for class to start:
    define a grading rubric for class given ablility spread
    match a class to a given ability spread
    combine class and ability
    add artificer? https://www.dndbeyond.com/classes/artificer
"""


class Class:
    def __init__(self, name, hd, proficiency, spellAbility, numSkills, autolevel, armor, weapons, tools, wealth):
        self.name = name
        self.hit_die = hd
        self.proficiency = proficiency
        self.saving_throws = None
        self.parse_proficiency()
        self.spell_ability = spellAbility
        self.skills = numSkills
        self.auto_level = autolevel
        self.stats = (armor, weapons, tools, wealth)

    def __str__(self):
        return self.name

    def parse_proficiency(self):
        self.proficiency = self.proficiency.replace('.', ',')
        self.proficiency = self.proficiency.split(', ') if self.proficiency else ''
        self.saving_throws = self.proficiency[:2]
        self.proficiency = self.proficiency[2:]
        self.proficiency = [(x, PROF_MAP[x]) for x in self.proficiency]

    def grade_class_for_ability_spread(self, ability_obj):
        """
        :param ability_obj:  ABILITIES = {
            'STR': 8,
            'DEX': 8,
            'CON': 8,
            'INT': 8,
            'WIS': 8,
            'CHA': 8
        }
        :return: grade of 0-100

        Considerations:
            Saving throws
            Spell casting
            Attacks
            Defense
            Proficiencies available in areas w/high abilities (buf)
            Proficiencies available in areas w/low abilities (mitigate)

        Example of very good match!
Sorcerer
Pick 2 among [('Arcana', 'INT'), ('Deception', 'CHA'), ('Insight', 'WIS'), ('Intimidation', 'CHA'), ('Persuasion', 'CHA'), ('Religion', 'INT')]
Saves: ['Constitution', 'Charisma'] and Spells: Charisma
{'STR': 12, 'DEX': 14, 'CON': 12, 'INT': 9, 'WIS': 10, 'CHA': 15}
        """
        return 0


class Universe:
    def __init__(self):
        self.data_folder = join(dirname(abspath(__file__)), 'data')
        self.data = {}

    def load_data(self):
        a = self.load_core()
        self.data = a
        # profs = []
        # for i in a:
        #     for j in a[i].proficiency:
        #         if j not in profs:
        #             profs.append(j)
        # sorted(profs)
        # print(profs)

    def load_core(self):
        with open(join(self.data_folder, 'Core.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Class(**x) for x in json_data['class']}


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


def choose_random_class():
    return uni.data[choose(list(uni.data), 1)[0]]


def compile_all_class_grades(abilities):
    return [x.grade_class_for_ability_spread(abilities) for x in uni.data]


def weighted_choose_classes(choices, weights):
    pass


picks = 1
choice = choose_random_class()
abilities = roll_ability()
match = choice.grade_class_for_ability_spread(abilities)
print(choice)
print(f'Pick {choice.skills} among {choice.proficiency}')
print(f'Saves: {choice.saving_throws} and Spells: {choice.spell_ability}')
print(abilities)
print(f'Grade: {match}')
