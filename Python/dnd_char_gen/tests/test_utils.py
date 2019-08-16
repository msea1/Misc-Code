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
