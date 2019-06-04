import json

from math import sqrt

STARTING_INFO = {
    "Alabama": {"actual_ev": 9, "pop_2010": 4779736, "dem_evs": 0, "gop_evs": 9},
    "Alaska": {"actual_ev": 3, "pop_2010": 710231, "dem_evs": 0, "gop_evs": 3},
    "Arizona": {"actual_ev": 11, "pop_2010": 6392017, "dem_evs": 0, "gop_evs": 11},
    "Arkansas": {"actual_ev": 6, "pop_2010": 2915918, "dem_evs": 0, "gop_evs": 6},
    "California": {"actual_ev": 55, "pop_2010": 37253956, "dem_evs": 55, "gop_evs": 0},
    "Colorado": {"actual_ev": 9, "pop_2010": 5029196, "dem_evs": 9, "gop_evs": 0},
    "Connecticut": {"actual_ev": 7, "pop_2010": 3574097, "dem_evs": 7, "gop_evs": 0},
    "Delaware": {"actual_ev": 3, "pop_2010": 897934, "dem_evs": 3, "gop_evs": 0},
    "District of Columbia": {"actual_ev": 3, "pop_2010": 601723, "dem_evs": 3, "gop_evs": 0},
    "Florida": {"actual_ev": 29, "pop_2010": 18801310, "dem_evs": 0, "gop_evs": 29},
    "Georgia": {"actual_ev": 16, "pop_2010": 9687653, "dem_evs": 0, "gop_evs": 16},
    "Hawaii": {"actual_ev": 4, "pop_2010": 1360301, "dem_evs": 4, "gop_evs": 0},
    "Idaho": {"actual_ev": 4, "pop_2010": 1567582, "dem_evs": 0, "gop_evs": 4},
    "Illinois": {"actual_ev": 20, "pop_2010": 12830632, "dem_evs": 20, "gop_evs": 0},
    "Indiana": {"actual_ev": 11, "pop_2010": 6483802, "dem_evs": 0, "gop_evs": 11},
    "Iowa": {"actual_ev": 6, "pop_2010": 3046355, "dem_evs": 0, "gop_evs": 6},
    "Kansas": {"actual_ev": 6, "pop_2010": 2853118, "dem_evs": 0, "gop_evs": 6},
    "Kentucky": {"actual_ev": 8, "pop_2010": 4339367, "dem_evs": 0, "gop_evs": 8},
    "Louisiana": {"actual_ev": 8, "pop_2010": 4533372, "dem_evs": 0, "gop_evs": 8},
    "Maine": {"actual_ev": 4, "pop_2010": 1328361, "dem_evs": 3, "gop_evs": 1},
    "Maryland": {"actual_ev": 10, "pop_2010": 5773552, "dem_evs": 10, "gop_evs": 0},
    "Massachusetts": {"actual_ev": 11, "pop_2010": 6547629, "dem_evs": 11, "gop_evs": 0},
    "Michigan": {"actual_ev": 16, "pop_2010": 9883640, "dem_evs": 0, "gop_evs": 16},
    "Minnesota": {"actual_ev": 10, "pop_2010": 5303925, "dem_evs": 10, "gop_evs": 0},
    "Mississippi": {"actual_ev": 6, "pop_2010": 2967297, "dem_evs": 0, "gop_evs": 6},
    "Missouri": {"actual_ev": 10, "pop_2010": 5988927, "dem_evs": 0, "gop_evs": 10},
    "Montana": {"actual_ev": 3, "pop_2010": 989415, "dem_evs": 0, "gop_evs": 3},
    "Nebraska": {"actual_ev": 5, "pop_2010": 1826341, "dem_evs": 0, "gop_evs": 5},
    "Nevada": {"actual_ev": 6, "pop_2010": 2700551, "dem_evs": 6, "gop_evs": 0},
    "New Hampshire": {"actual_ev": 4, "pop_2010": 1316470, "dem_evs": 4, "gop_evs": 0},
    "New Jersey": {"actual_ev": 14, "pop_2010": 8791894, "dem_evs": 14, "gop_evs": 0},
    "New Mexico": {"actual_ev": 5, "pop_2010": 2059179, "dem_evs": 5, "gop_evs": 0},
    "New York": {"actual_ev": 29, "pop_2010": 19378102, "dem_evs": 29, "gop_evs": 0},
    "North Carolina": {"actual_ev": 15, "pop_2010": 9535483, "dem_evs": 0, "gop_evs": 15},
    "North Dakota": {"actual_ev": 3, "pop_2010": 672591, "dem_evs": 0, "gop_evs": 3},
    "Ohio": {"actual_ev": 18, "pop_2010": 11536504, "dem_evs": 0, "gop_evs": 18},
    "Oklahoma": {"actual_ev": 7, "pop_2010": 3751351, "dem_evs": 0, "gop_evs": 7},
    "Oregon": {"actual_ev": 7, "pop_2010": 3831074, "dem_evs": 7, "gop_evs": 0},
    "Pennsylvania": {"actual_ev": 20, "pop_2010": 12702379, "dem_evs": 0, "gop_evs": 20},
    "Puerto Rico": {"actual_ev": 0, "pop_2010": 3725789, "dem_evs": 0, "gop_evs": 0},
    "Rhode Island": {"actual_ev": 4, "pop_2010": 1052567, "dem_evs": 4, "gop_evs": 0},
    "South Carolina": {"actual_ev": 9, "pop_2010": 4625364, "dem_evs": 0, "gop_evs": 9},
    "South Dakota": {"actual_ev": 3, "pop_2010": 814180, "dem_evs": 0, "gop_evs": 3},
    "Tennessee": {"actual_ev": 11, "pop_2010": 6346105, "dem_evs": 0, "gop_evs": 11},
    "Texas": {"actual_ev": 38, "pop_2010": 25145561, "dem_evs": 0, "gop_evs": 38},
    "Utah": {"actual_ev": 6, "pop_2010": 2763885, "dem_evs": 0, "gop_evs": 6},
    "Vermont": {"actual_ev": 3, "pop_2010": 625741, "dem_evs": 3, "gop_evs": 0},
    "Virginia": {"actual_ev": 13, "pop_2010": 8001024, "dem_evs": 13, "gop_evs": 0},
    "Washington": {"actual_ev": 12, "pop_2010": 6724540, "dem_evs": 12, "gop_evs": 0},
    "West Virginia": {"actual_ev": 5, "pop_2010": 1852994, "dem_evs": 0, "gop_evs": 5},
    "Wisconsin": {"actual_ev": 10, "pop_2010": 5686986, "dem_evs": 0, "gop_evs": 10},
    "Wyoming": {"actual_ev": 3, "pop_2010": 563626, "dem_evs": 0, "gop_evs": 3},
}

EXCLUDE_DC = False
EXCLUDE_PR = False

MAX_REPS = 1000
MODEL_EVS = MAX_REPS + 102  # 50 states * 2 senators + 2 for DC for whatever reason
if EXCLUDE_DC:
    MODEL_EVS += 1  # add its non-voting rep
if not EXCLUDE_PR:
    MODEL_EVS += 2  # 2 senators for PR

REPS_TO_GO = MAX_REPS - 435
MODEL_INFO = STARTING_INFO.copy()

if EXCLUDE_DC:
    del MODEL_INFO['District of Columbia']
if EXCLUDE_PR:
    del MODEL_INFO['Puerto Rico']


def update_coeffs(info):
    for state, data in info.items():
        if REPS_TO_GO == MAX_REPS - 435:  # first run
            data['model_reps'] = data['actual_ev'] - 2
        current_reps = max(1, data['model_reps'])  # avoid / 0
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
    print(json.dumps(MODEL_INFO, indent=4))


def top_level(info):
    summary = "STATE".ljust(22)
    summary += "EVs".ljust(4)
    summary += "%".ljust(6)
    summary += "\n"
    for state, data in info.items():
        before = data['actual_ev']
        before_per = round(100 * before / 538, 2)
        after = data['model_reps'] + 2
        after_per = round(100 * after / (103 + MAX_REPS), 2)
        summary += f"{state.ljust(22)} " \
            f"{str(before).ljust(4)} " \
            f"({str(before_per).rjust(5)}%) " \
            f"{after} " \
            f"({after_per}%), " \
            f"+{after - before} seats, " \
            f"{'+' if after_per > before_per else ''}{round(after_per - before_per, 2)}%, " \
            f"final coeff of {int(data['apport_coeff'])}\n"
    print(summary)


def rerun_2016(info):
    gop = [0, 0]
    dem = [0, 0]
    for state, data in info.items():
        gop[0] += data['gop_evs']
        dem[0] += data['dem_evs']
        new_ev = data['model_reps'] + 2
        if data['dem_evs'] == 0:
            gop[1] += new_ev
        elif data['gop_evs'] == 0:
            dem[1] += new_ev
        else:
            # guess at senate win
            if data['gop_evs'] > data['dem_evs']:
                gop[1] += 2
                dem_share = data['dem_evs'] / (data['actual_ev'] - 2)
            else:
                dem[1] += 2
                dem_share = (data['dem_evs'] - 2) / (data['actual_ev'] - 2)

            # split house evs
            gop[1] += int((1 - dem_share) * data['model_reps'])
            dem[1] += int(dem_share * data['model_reps'])

    if EXCLUDE_DC:
        dem[0] += 3
        dem[1] += 3

    if not EXCLUDE_PR:
        dem[1] += info['Puerto Rico']['model_reps']  # assuming it goes to Dems

    print("--- 2016 Results ---")
    print(f"--- Dem {dem[0]} ~ GOP {gop[0]} ---")
    print("--- 2016 Model ---")
    print(f"--- Dem {dem[1]} ~ GOP {gop[1]} ---")


while REPS_TO_GO > 0:
    update_coeffs(MODEL_INFO)
    add_to_state = find_biggest_coeff(MODEL_INFO)
    add_seat(MODEL_INFO, add_to_state)

top_level(MODEL_INFO)
rerun_2016(MODEL_INFO)
