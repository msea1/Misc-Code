from __future__ import division

one = "different simliar"
two = "similar"


def compare(first, second):
    smaller, bigger = sorted([first, second], key=len)

    s_smaller= smaller.split()
    s_bigger = bigger.split()
    bigger_sets = [set(word) for word in s_bigger]

    counter = 0
    for word in s_smaller:
        if set(word) in bigger_sets:
            counter += 1
    if counter:
        return counter/len(s_bigger)*100 # percentage match
    return counter


print("match: ", compare(one, two))
