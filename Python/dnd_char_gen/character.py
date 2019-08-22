from dnd_char_gen.ability_roll import roll_ability
from dnd_char_gen.definitions import Alignment, PROF_MAP
from dnd_char_gen.utils import choose, roll


class Character:
    def __init__(self, _cli_args):
        self.name = ""
        self.is_npc = False
        self.abilities = None
        self.race = None
        self.char_class = None
        self.saving_throws = None
        self.proficiencies = None
        self.background = None
        self.alignment = None
        # self.is_npc = kwargs.get('is_npc', False)
        # self.traits = []  # T.I.B.F.
        # self.bonus_actions = []
        # self.reactions = []

    def __str__(self):
        pass

    def create(self, data):
        if not self.abilities:
            self.abilities = self.pick_abilities()
            print(f'Abilities selected to be {self.abilities}')
        if not self.race:
            picks = 1
            pick = self.pick_race(data['race'])
            if self.is_npc:
                pass
            else:
                while pick.npc_only:  # have to keep picking
                    pick = self.pick_race(data['race'])
                    picks += 1
            self.race = pick
            print(f'Took {picks} picks to select {pick} as race')
        if not self.char_class:
            choice = self.pick_class(data['class'])
            self.saving_throws, self.proficiencies = self.parse_proficiency(choice.proficiency)
            print(f'Selected {choice} as class')
            print(f'    Pick {choice.num_skills} among {self.proficiencies}')
            print(f'    Saves: {" and ".join(self.saving_throws)} and Spell ability: {choice.spell_ability}')
        if not self.background:
            self.background = self.pick_background(data['background'])
            print(f'Background is {self.background}')
            print(f'    Good at {self.background.proficiency}')
        if not self.alignment:
            self.alignment = self.pick_alignment()
            print(f'Alignment is {self.alignment.name}')

    @staticmethod
    def parse_proficiency(prof_str):
        prof_str = prof_str.replace('.', ',')
        prof_list = prof_str.split(', ') if prof_str else None
        if not prof_list:
            return None, None
        saving_throws = prof_list[:2]
        proficiencies = [(x, PROF_MAP[x]) for x in prof_list[2:]]
        return saving_throws, proficiencies

    @staticmethod
    def pick_abilities():
        return roll_ability()

    @staticmethod
    def pick_race(race_data):
        major_race = choose(list(race_data), 1)[0]
        if len(race_data[major_race]) == 1:
            return race_data[major_race][0]
        else:
            subr = choose(race_data[major_race], 1)[0]
            i = race_data[major_race].index(subr)
            return race_data[major_race][i]

    @staticmethod
    def pick_class(class_data):
        random_class = class_data[choose(list(class_data), 1)[0]]
        # return sorted([x.grade_class_for_ability_spread(abilities) for x in class_data])
        return random_class

    @staticmethod
    def pick_background(bg_data):
        background = choose(list(bg_data), 1)[0]
        bg_list = bg_data[background]
        if len(bg_list) == 1:
            return bg_list[0]
        else:
            sub_i = roll(len(bg_list))
            return bg_list[sub_i - 1]

    @staticmethod
    def pick_alignment():
        choice = roll(9)
        return Alignment(choice)


class Feat:
    def __init__(self):
        pass  # future dev possibly to randomly assign a feat


class Item:
    def __init__(self):
        pass  # future dev possibly to randomly assign items


class Spell:
    def __init__(self):
        pass  # future dev possibly to randomly assign spells
