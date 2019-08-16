from enum import IntEnum
from dnd_char_gen.utils import roll

class Character:
    def __init__(self, cli_args):
        self.name = ""
        self.abilities = Ability()
        self.is_npc = kwargs.get('is_npc', False)
        self.race = kwargs.get('race', None)
        self.dnd_class = kwargs.get('dnd_class', None)
        self.background = kwargs.get('background', None)
        self.alignment = kwargs.get('alignment_value', None)
        self.traits = []  # T.I.B.F.
        self.bonus_actions = []
        self.reactions = []

    def __str__(self):
        pass

    def create(self, data):
        #  Race - Abilities - Class - Background - Backstory
        if not self.race:
            self.race = data['races'][self.pick_race(self.is_npc, list(data['races']))]
        # self.alignment = Alignment(self.alignment)

    def pick_race(self, is_npc, list_of_races):
        # TODO: race weighting
        race = roll(len(list_of_races))
        while is_npc == False:
            race = roll(len(list_of_races))
            is_npc = self.race_allowed_for_player(list_of_races[race-1])
        return list_of_races[race-1]


class Ability():
    def __init__(self):
        self.stats = {
            'STR': 8,
            'DEX': 8,
            'CON': 8,
            'INT': 8,
            'WIS': 8,
            'CHA': 8
        }


class Alignment(IntEnum):
    LAWFUL_GOOD = 1
    LAWFUL_NEUTRAL = 2
    LAWFUL_EVIL = 3
    NEUTRAL_GOOD = 4
    NEUTRAL_NEUTRAL = 5
    NEUTRAL_EVIL = 6
    CHAOTIC_GOOD = 7
    CHAOTIC_NEUTRAL = 8
    CHAOTIC_EVIL = 9


class Race:
    def __init__(self, name, size, speed, ability, proficiency, traits):
        self.npc_only = 'npc' in name.lower()
        self.name = name
        self.size = size
        self.speed = speed
        self.ability_str = ability
        self.proficiency = proficiency
        self.traits = traits

    def __str__(self):
        pass

    def parse_abilities(self, ability_obj):
        entries = self.ability_str.split(',')
        for entry in entries:
            ability_type = entry[:3].upper()
            ability_mod = int(entry[3:].strip())
            ability_obj['stats'][ability_type] += ability_mod

    def parse_traits(self):
        return {x['name']: " ".join(x['text']) for x in self.traits}

class Class:
    def __init__(self, **kwargs):
        pass

    def __str__(self):
        pass


class Background:
    def __init__(self, **kwargs):
        pass

    def __str__(self):
        pass


class Feat:
    def __init__(self):
        pass  # future dev possibly to randomly assign a feat


class Item:
    def __init__(self):
        pass  # future dev possibly to randomly assign items


class Spell:
    def __init__(self):
        pass  # future dev possibly to randomly assign spells
