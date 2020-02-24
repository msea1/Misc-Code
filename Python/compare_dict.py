from difflib import SequenceMatcher
from itertools import combinations

THRESHOLD = 0.75


def cross_reference_lists(list_a, list_b):
    matches = []
    for i in list_a:
        for j in list_b:
          if SequenceMatcher(None, i, j).ratio() > THRESHOLD and (i, j) not in matches:
            matches.append((i, j))
    return matches

def cross_reference_dicts(dict_a, dict_b):
    matched_values = {}
    matched_keys = cross_reference_lists(list(dict_a.keys()), list(dict_b.keys()))
    for check_k in matched_keys:
        if check_k[0] in dict_a:
            value_list1 = dict_a[check_k[0]]
            value_list2 = dict_b[check_k[1]]
        else:
            value_list1 = dict_b[check_k[0]]
            value_list2 = dict_a[check_k[1]]
        matched_values[check_k] = cross_reference_lists(value_list1, value_list2)
    return {k for k, v in matched_values.items() if len(v) > 0}
