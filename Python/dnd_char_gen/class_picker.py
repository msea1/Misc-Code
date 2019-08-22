"""
needed for class to start:
    define a grading rubric for class given ablility spread
    match a class to a given ability spread
    combine class and ability
    add artificer? https://www.dndbeyond.com/classes/artificer
"""


class CharClass:
    def __init__(self, name, hd, proficiency, spellAbility, numSkills, autolevel, armor, weapons, tools, wealth):
        self.name = name
        self.hit_die = hd
        self.proficiency = proficiency
        self.spell_ability = spellAbility
        self.num_skills = numSkills
        self.auto_level = autolevel
        self.stats = (armor, weapons, tools, wealth)

    def __str__(self):
        return self.name

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
