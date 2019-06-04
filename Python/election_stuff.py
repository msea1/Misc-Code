from math import sqrt

STARTING_INFO = {
    "Alabama": {
        "actual_ev": 9,
        "pop_2010": 4779736,
        "model_reps": 9 - 2,
        "apport_coeff": 4779736 / sqrt(7 * 8),
    }
}

EXCLUDE_DC = True
EXCLUDE_PR = True
MAX_REPS = 435 * 2
REPS_TO_GO = MAX_REPS - 435


def update_coeffs(info):
    for state, data in info.items():
        current_reps = data['model_reps']
        data['apport_coeff'] = data['pop_2010'] / sqrt(current_reps * (current_reps + 1))


def find_biggest_coeff(info):
    next_rep = None
    for state, data in info.items():
        if not next_rep or data['apport_coeff'] > info[next_rep]['apport_coeff']:
            next_rep = state
    return next_rep


def add_seat(info, next_rep):
    global REPS_TO_GO
    if REPS_TO_GO > 0:
        info[next_rep]['model_reps'] += 1
        REPS_TO_GO -= 1


def pretty_print():
    pass


update_coeffs(STARTING_INFO)
