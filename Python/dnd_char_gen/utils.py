import random


def roll(num_sides):
    return random.randint(1, num_sides)


def roll_weighted(prob_list):
    return random.choices(range(prob_list), weights=prob_list)


def two_dice_rolls_to_list(d, rolls):
    #  x * len(y) + y (0th-indexed)
    return (rolls[0]-1) * d + rolls[1]


def ability_score_to_modifier(raw_score):
    return raw_score//2 - 5


def cost_of_ability_point(raw_score):
    if raw_score < 8:
        raise ValueError(f'Not allowed to have a score below 8')
    elif raw_score < 14:
        return raw_score - 8
    elif raw_score == 14:
        return 7
    elif raw_score == 15:
        return 9
    raise ValueError('Not allowed to have a score above 15')
