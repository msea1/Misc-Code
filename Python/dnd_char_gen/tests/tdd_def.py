import unittest

from dnd_char_gen.character import Race


class Tests(unittest.TestCase):
    def test_point_allocation_options(self):
        pass

    def test_all_abilities_assigned(self):
        pass

    def test_class_suggestions_make_sense(self):
        pass

    def test_background_suggestions_make_sense(self):
        pass

    def test_traits_suggestions_make_sense(self):
        pass

    def test_char_print_readable(self):
        pass

    def test_create_char_via_assigned_order(self):
        #  Race - Abilities - Class - Background - Backstory
        pass

    def test_race_suggestions_make_sense(self):
        pass

    def test_npc_races_removed_from_pc_creation(self):
        pass

    def test_race_info_correct(self):
        pass

    def test_race_printable(self):
        pass

    def test_default_args(self):
        pass

    def test_load_data_combines_races_from_multiple_sources(self):
        pass

    def test_load_data_formats_races(self):
        pass

    def test_load_data_formats_classes(self):
        pass

    def test_load_data_formats_backgrounds(self):
        pass

    def test_parse_traits(self):
        sample = [
            {'name': 'Bludgeoning Vulnerability',
             'text': ['You are vulnerable to bludgeoning damage.', ' ', "Source: Dungeon Master's Guide, p. 282"]}
        ]
        r = Race('', None, None, None, None, sample)
        resp = r.parse_traits()
        self.assertEqual({'Bludgeoning Vulnerability': 'You are vulnerable to bludgeoning damage.   '
                                                       "Source: Dungeon Master's Guide, p. 282"}, resp)
