"""
needed for start:
    
"""


class Background:
    def __init__(self, name, proficiency, trait):
        self.name = name
        self.proficiency = proficiency
        self.traits = trait

    def __str__(self):
        return self.name

    def grade(self, input):
        return 0
