from dnd_char_gen.definitions import Proficiency


class Background:
    def __init__(self, name, proficiency, trait):  # named to coincide with the XML input
        self.name = name
        self.proficiency_str = proficiency or ''
        self.trait_list = trait

        self.proficiencies = Proficiency()
        self.traits = None

    def __str__(self):
        return f'{self.name}, good at {self.proficiency_str}'

    def parse(self):
        self.proficiencies.skills = self.parse_proficiency_string()
        self.traits = self.format_trait_list()
        self.parse_trait_dict()

    def parse_proficiency_string(self):
        if self.proficiency_str:
            return sorted([x.strip() for x in self.proficiency_str.split(',')])

    def format_trait_list(self):
        traits = {}
        for trait in self.trait_list:
            key = trait['name']
            value = trait['text']
            if isinstance(value, list):
                value = ("\n".join(i.strip() for i in value if i)).replace('\n\n', '\n').replace('\t', ' ')
            traits[key] = value
        return traits

    def parse_trait_dict(self):
        for k in self.traits.keys():
            if k == 'Starting Proficiencies':
                for line in self.traits['Starting Proficiencies'].split('\n'):
                    if ':' in line:
                        header, text = line.split(':')
                        if 'Skills' in header:
                            self.proficiency_str += f'. {line}'
                        elif 'Languages' in header:
                            self.proficiency_str += f'. {line}'
                        elif 'Tools' in header:
                            self.proficiency_str += f'. {line}'
            elif any(known in k for known in ('Ideal', 'Bond', 'Flaw', 'Description', 'Equipment')):
                pass
            else:
                pass
        """
        Skills {'Deception', 'Wisdom', 'Performance', 'Arcana', 'or Charisma skill of your choice', 'plus your choice of one from among Arcana', 'Stealth', 'Animal Handling', 'Persuasion', 'plus one from among Arcana', 'Acrobatics', 'History', 'Investigation', 'Nature', 'Insight and one Intelligence', 'Survival', 'Insight', 'Medicine', 'Perception', 'and Religion', 'or Survival', 'Choose two from Arcana', 'Athletics', 'as appropriate to your faction', 'as appropriate for your order', 'Religion', 'Sleight of Hand', 'Intimidation', 'and Stealth', 'Choose two from among Deception'}
        Tools {"cartographer's tools or navigator's tools", "alchemist's supplies and tinker's tools", 'land vehicles, water vehicles', 'Choose two from among one type of gaming set, one musical instrument, and thieves’ tools', 'vehicles (land) and one gaming set', 'one type of gaming set, land vehicles', "vehicles (sea/air) and navigator's tools", "thieves' tools", "one type of musical instrument or artisan's tools", 'disguise kit, forgery kit', "one type of gaming set, thieves' tools", 'vehicles (land) and herbalism kit', "thieves' tools, one type of musical instrument", "navigator's tools, water vehicles", 'one type of musical instrument', "brewer's supplies and cook's utensils", "disguise kit and one type of artisan's tools or gaming set", "alchemist's supplies and herbalism kit", 'disguise kit and one musical instrument', 'one type of gaming set or one musical instrument', 'disguise kits, forgery kits', "tinker's tools and thieves' tools", 'none', 'one type of gaming set, water vehicles', 'your choice of a gaming set or a musical instrument', "calligrapher's tools and forgery kit", "poisoner's kit and one musical instrument", 'disguise kits, one type of musical instrument', 'herbalism kits', 'one type of gaming set', 'any one musical instrument or gaming set of your choice, likely something native to your homeland', 'special (see origin below)', "one type of artisan's tools", "thieves' tools and one gaming set", 'forgery kit', 'land vehicles', 'one gaming set and vehicles (land)', "one type of artistic artisan's tools and one musical instrument", "thieves' tools and diguise kit", "one type of artisan's tools, land vehicles", "navigator's tools", "disguise kits, thieves' tools"}
        Langs {'', 'Netherese', 'any one exotic language (Abyssal, Celestial, Deep Speech, Draconic, Infernal, Primordial, Sylvan, or Undercommon) of your choice', 'any two of your choice', 'Dwarvish, Undercommon', 'none', 'any one of your choice', 'Draconic', 'Giant', 'one racial language', 'Dwarvish or one of your choice if you already speak Dwarvish', 'Elvish'}
        """

