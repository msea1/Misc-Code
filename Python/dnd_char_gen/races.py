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
