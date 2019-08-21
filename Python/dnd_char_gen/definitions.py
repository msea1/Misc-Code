from enum import IntEnum


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


class Skills():
    def __init__(self):
        pass
        # not sure if class makes sense on all these
        # yes for once in the character, but not for priming
