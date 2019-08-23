from enum import IntEnum


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


def create_base_abilities():
    return {
        'STR': 8,
        'DEX': 8,
        'CON': 8,
        'INT': 8,
        'WIS': 8,
        'CHA': 8
    }


PROF_MAP = {
    'Deception': 'CHA',
    'Intimidation': 'CHA',
    'Performance': 'CHA',
    'Persuasion': 'CHA',
    'Acrobatics': 'DEX',
    'Sleight of Hand': 'DEX',
    'Stealth': 'DEX',
    'Arcana': 'INT',
    'History': 'INT',
    'Investigation': 'INT',
    'Nature': 'INT',
    'Religion': 'INT',
    'Athletics': 'STR',
    'Animal Handling': 'WIS',
    'Insight': 'WIS',
    'Medicine': 'WIS',
    'Perception': 'WIS',
    'Survival': 'WIS'
}
