"""
needed for start:
    
"""


class Background:
    def __init__(self, name, proficiency, trait):
        self.name = name
        self.proficiency = proficiency
        self.traits = self.parse_trait_list(trait)

    def __str__(self):
        return self.name

    def grade(self, input):
        return 0

    @staticmethod
    def parse_trait_list(trait_list):
        traits = {}
        for trait in trait_list:
            key = trait['name']
            value = trait['text']
            if isinstance(value, list):
                value = ("\n".join(i.strip() for i in value if i)).replace('\n\n', '\n').replace('\t', ' ')
            traits[key] = value
        return traits

