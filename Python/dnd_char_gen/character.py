from enum import IntEnum
from dnd_char_gen.utils import roll, parse_traits, choose


class Character:
    def __init__(self, cli_args):
        self.name = ""
        self.abilities = cli_args.abilities
        # self.points = cli_args.points
        self.is_npc = kwargs.get('is_npc', False)
        self.race = cli_args.race
        self.dnd_class = kwargs.get('dnd_class', None)
        self.background = kwargs.get('background', None)
        self.alignment = kwargs.get('alignment_value', None)
        self.traits = []  # T.I.B.F.
        self.bonus_actions = []
        self.reactions = []

    def __str__(self):
        pass

    def create(self, data):
        #  Abilities - Race - Class - Background - Backstory
        if not self.abilities:
            self.abilities = self.pick_abilities()
        if not self.race:
            self.race = self.pick_race(data)

    def pick_abilities(self):
        pass

    def pick_race(self, data):
        # TODO: race weighting
        all_races = list(data['races'])
        while True:
            potential_choice = choose(all_races)
            if self.is_npc or not data['races'][potential_choice].playable:
                chosen_race = data['races'][potential_choice]
                chosen_race.apply(self)
                return chosen_race



class Race:
    def __init__(self, name, size, speed, ability, proficiency, trait):
        self.npc_only = 'npc' in name.lower()
        self.name = name
        self.size = size
        self.speed = speed
        self.ability_str = ability
        self.proficiency = proficiency
        self.trait = parse_traits(trait)

    def __str__(self):
        pass

    def apply(self, character_obj):
        pass

    def parse_abilities(self, ability_obj):
        entries = self.ability_str.split(',')
        for entry in entries:
            ability_type = entry[:3].upper()
            ability_mod = int(entry[3:].strip())
            ability_obj['stats'][ability_type] += ability_mod

class Class:
    def __init__(self, name, hd, proficiency, spellAbility):
        pass

    def __str__(self):
        pass


class Background:
    def __init__(self, name, proficiency, trait):
        self.name = name
        self.proficiency = proficiency
        self.trait = parse_traits(trait)

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
