from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson

"""
needed for Race to start:
    ability_str parsed
    npc_only
    name, parsed
    proficiency parsed
    traits parsed for abiltiy score increases, skills, feat, etc
    
    
    then, add in other data
    and compare/weight to avoid all the dragonborns for example
"""
DESIGNATED_NPC_RACES = ['changeling']


class Race:
    def __init__(self, name, size, speed, ability, proficiency, trait, spellAbility="", modifier=""):
        self.npc_only = 'npc' in name.lower() or name.lower() in DESIGNATED_NPC_RACES
        self.name = name
        self.size = size
        self.speed = speed
        self.ability_str = ability
        self.abilities = self.parse_abilities()
        self.proficiency = proficiency
        self.parse_proficiency()
        self.trait = trait
        self.spell_ability = spellAbility
        self.modifier = modifier

    def __str__(self):
        return self.name

    def apply(self, character_obj):
        pass

    def parse_abilities(self):
        abil = []
        if not self.ability_str:
            return []
        entries = self.ability_str.split(',')
        for entry in entries:
            entry = entry.strip()
            ability_type = entry[:3].upper()
            ability_mod = int(entry[3:].strip())
            # ability_obj['stats'][ability_type] += ability_mod
            abil.append((ability_type, ability_mod))
        return abil

    def parse_proficiency(self):
        self.proficiency = self.proficiency.split(',') if self.proficiency else ''


class Universe:
    def __init__(self):
        self.data_folder = join(dirname(abspath(__file__)), 'data')
        self.data = {}

    def load_data(self):
        a = self.load_core()
        a.update(self.load_eberron())
        a.update(self.load_npc_race_data())
        a = self.match_race_to_already_existing(a)
        self.data = a

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

    def load_core(self):
        with open(join(self.data_folder, 'Core.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Race(**x) for x in json_data['race']}

    def load_eberron(self):
        with open(join(self.data_folder, 'EberronAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Race(**x) for x in json_data['race']}

    def load_npc_race_data(self):
        with open(join(self.data_folder, 'NPCRacesAddOn.xml')) as fin:
            xmldata = fin.read()
        json_data = xmljson.parker.data(fromstring(xmldata))
        return {x['name']: Race(**x) for x in json_data['race']}


uni = Universe()
uni.load_data()

from dnd_char_gen.utils import choose
allow_npc = False


def choose_race():
    major_race = choose(list(uni.data), 1)[0]
    if len(uni.data[major_race]) == 1:
        return uni.data[major_race][0]
    else:
        subr = choose(uni.data[major_race], 1)[0]
        i = uni.data[major_race].index(subr)
        return uni.data[major_race][i]


picks = 1
pick = choose_race()
if allow_npc:
    print(pick)
else:
    while pick.npc_only:  # have to keep picking
        pick = choose_race()
        print(pick)
        picks += 1
    print(pick)
print(picks)