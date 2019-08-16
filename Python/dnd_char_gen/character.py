from enum import IntEnum


class Character:
    def __init__(self, **kwargs):
        self.name = ""
        self.race = kwargs['race']
        self.dnd_clss = kwargs['race']
        self.background = kwargs['race']
        self.alignment = Alignment(kwargs['alignment_value'])

    def __str__(self):
        pass


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
    def __init__(self, **kwargs):
        self.npc = kwargs['npc']

    def __str__(self):
        pass


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
