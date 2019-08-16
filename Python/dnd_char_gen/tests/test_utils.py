from dnd_char_gen import utils
import unittest


class Test(unittest.TestCase):
    def test_xd_rolls_to_list(self):
        # error cases on invalid input
        self.assertEqual(1, utils.two_dice_rolls_to_list(3, [1, 1]))
        self.assertEqual(2, utils.two_dice_rolls_to_list(3, [1, 2]))
        self.assertEqual(3, utils.two_dice_rolls_to_list(3, [1, 3]))
        self.assertEqual(4, utils.two_dice_rolls_to_list(3, [2, 1]))
        self.assertEqual(5, utils.two_dice_rolls_to_list(3, [2, 2]))
        self.assertEqual(6, utils.two_dice_rolls_to_list(3, [2, 3]))
        self.assertEqual(7, utils.two_dice_rolls_to_list(3, [3, 1]))
        self.assertEqual(8, utils.two_dice_rolls_to_list(3, [3, 2]))
        self.assertEqual(9, utils.two_dice_rolls_to_list(3, [3, 3]))

    def test_ability_score_to_modifier(self):
        self.assertEqual(-3, utils.ability_score_to_modifier(4))
        self.assertEqual(-3, utils.ability_score_to_modifier(5))
        self.assertEqual(-2, utils.ability_score_to_modifier(6))
        self.assertEqual(-2, utils.ability_score_to_modifier(7))
        self.assertEqual(-1, utils.ability_score_to_modifier(8))
        self.assertEqual(-1, utils.ability_score_to_modifier(9))
        self.assertEqual(0, utils.ability_score_to_modifier(10))
        self.assertEqual(0, utils.ability_score_to_modifier(11))
        self.assertEqual(1, utils.ability_score_to_modifier(12))
        self.assertEqual(1, utils.ability_score_to_modifier(13))
        self.assertEqual(2, utils.ability_score_to_modifier(14))
        self.assertEqual(2, utils.ability_score_to_modifier(15))
        self.assertEqual(3, utils.ability_score_to_modifier(16))
        self.assertEqual(3, utils.ability_score_to_modifier(17))
        self.assertEqual(4, utils.ability_score_to_modifier(18))
        self.assertEqual(4, utils.ability_score_to_modifier(19))
        self.assertEqual(5, utils.ability_score_to_modifier(20))

    def test_cost_of_next_ability_point(self):
        self.assertEqual(0, utils.cost_of_ability_point(8))
        self.assertEqual(1, utils.cost_of_ability_point(9))
        self.assertEqual(2, utils.cost_of_ability_point(10))
        self.assertEqual(3, utils.cost_of_ability_point(11))
        self.assertEqual(4, utils.cost_of_ability_point(12))
        self.assertEqual(5, utils.cost_of_ability_point(13))
        self.assertEqual(7, utils.cost_of_ability_point(14))
        self.assertEqual(9, utils.cost_of_ability_point(15))