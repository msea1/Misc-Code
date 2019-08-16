import random


def roll(num_sides):
    return random.randint(1, num_sides)


def roll_weighted(prob_list):
    return random.choices(range(prob_list), weights=prob_list)


def two_dice_rolls_to_list(d, rolls):
    #  x * len(y) + y (0th-indexed)
    return (rolls[0]-1) * d + rolls[1]
