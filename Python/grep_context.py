import argparse
import re
import unittest
from collections import deque


def search_deque_for_regex(deck, query):
    matches = []
    for i, l in enumerate(deck):
        if re.search(query, l):
            matches.append(((i+1)*-1, l))
    return matches


def load(fp):
    with open(fp) as fin:
        lns = fin.readlines()
    return lns


def search(fp, data, q1, q2, window, paired):
    matches = []
    r1 = re.compile(q1)
    r2 = re.compile(q2)
    lines_since_match = window + 1

    deck = deque(maxlen=window+1)  # keep current plus past n (=window) lines around
    for i, line in enumerate(data):
        deck.appendleft(line)
        if r1.search(line):
            lines_since_match = 0
            found_match = search_deque_for_regex(deck, r2)
            if found_match:
                if paired:
                    matches.append((line, found_match))
                # either already matched, or we don't want to match
                lines_since_match = window + 1
        if lines_since_match < window:
            if r2.search(line):
                if paired:
                    matches.append((line, lines_since_match))
                # either already matched, or we don't want to match
                lines_since_match = window + 1
        elif lines_since_match == window:
            match = r2.search(line)
            if not paired and not match:
                matches.append((r1.pattern, i-window+1))
            elif paired and match:
                matches.append((line, lines_since_match))
        lines_since_match += 1

    print(f"Search {fp}")
    if paired:
        print(f"For {q1} within {window} lines of {q2}")
    else:
        print(f"For {q1} appearing without {q2} inside of {window} lines")
    print(f'Found {len(matches)} such cases:')
    for m in matches:
        print(m)
    return matches


if __name__ == '__main__':

    # Example shell usage
    # $ python3 grep_context.py -f logs.txt -m1 'Stopping cmdseq-service' -m2 'Stopping rw-service' -n 500 -x true
    # ('Stopping cmdseq-service', 283640)
    # ('Stopping cmdseq-service', 330373)
    # ('Stopping cmdseq-service', 1093883)
    # ('Stopping cmdseq-service', 1360935)
    # ('Stopping cmdseq-service', 1464382)
    # ('Stopping cmdseq-service', 1466484)
    # $ sed'330373q;d'. / logs.txt
    # 2018-07-05T22:20:26.468098+00:00 feba3f0746d048769693d67368beec76 [  101.553972] mothra-15 systemd[1] INFO: Stopping cmdseq-service...

    parser = argparse.ArgumentParser(description='Find cases where m1 is within n of m2')
    parser.add_argument('-f', help='Filepath to search')
    parser.add_argument('-m1', help='main search query, in regex')
    parser.add_argument('-m2', help='secondary search query, in regex')
    parser.add_argument('-n', help='Number of lines for the search window')
    parser.add_argument('-x', help='If "true", find cases where m1 is NOT within n of m2')
    cli_args = parser.parse_args()

    lines = load(cli_args.f)
    search(cli_args.f, lines, cli_args.m1, cli_args.m2, int(cli_args.n), cli_args.x != 'true')


class Tests(unittest.TestCase):

    def setUp(self):
        self.deck = deque(['howdy', 'hello', 'hello world', 'hi', 'oh, hello'], maxlen=5)
        self.test_data = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor " \
                         "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud " \
                         "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute " \
                         "irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla " \
                         "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia " \
                         "deserunt mollit anim id est laborum.".split()

    def test_complete_find_matches_regex(self):
        find = re.compile('dolor[e]*')
        neighbor = re.compile('aute')
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 3, paired=True))

    def test_complete_find_matches_before(self):
        find = re.compile('dolore')
        neighbor = re.compile('labore')
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 3, paired=True))

    def test_complete_find_matches_after(self):
        self.assertTrue(search('test_data', self.test_data, 'dolore', 'magna', 3, paired=True))

    def test_complete_find_matches_after_but_outside_window(self):
        find = re.compile('dolore')
        neighbor = re.compile('minim')
        self.assertFalse(search('test_data', self.test_data, find, neighbor, 3, paired=True))

    def test_complete_find_matches_after_on_window(self):
        find = re.compile('dolore')
        neighbor = re.compile('minim')  # 6 words away
        self.assertFalse(search('test_data', self.test_data, find, neighbor, 5, paired=True))
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 6, paired=True))

    def test_complete_find_alone_regex(self):
        find = re.compile('dolor[e]*')
        neighbor = re.compile('aute')
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 2, paired=False))

    def test_complete_find_alone_before_false(self):
        find = re.compile('voluptate')
        neighbor = re.compile('dolor')  # present, 4 words away
        self.assertFalse(search('test_data', self.test_data, find, neighbor, 4, paired=False))

    def test_complete_find_alone_before_true(self):
        find = re.compile('voluptate')
        neighbor = re.compile('dolor')  # present, but 4 words away
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 3, paired=False))

    def test_complete_find_alone_after_false(self):
        find = re.compile('voluptate')
        neighbor = re.compile('velit')
        self.assertFalse(search('test_data', self.test_data, find, neighbor, 3, paired=False))

    def test_complete_find_alone_after_true(self):
        find = re.compile('voluptate')
        neighbor = re.compile('cillum')  # present, but 3 words away
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 2, paired=False))

    def test_complete_find_alone_after_but_outside_window(self):
        find = re.compile('voluptate')
        neighbor = re.compile('cillum')  # 3 words away
        self.assertTrue(search('test_data', self.test_data, find, neighbor, 2, paired=False))

    def test_complete_find_alone_after_on_window(self):
        find = re.compile('voluptate')
        neighbor = re.compile('cillum')  # 3 words away
        self.assertFalse(search('test_data', self.test_data, find, neighbor, 3, paired=False))

    def test_search_in_deque(self):
        q1 = re.compile('hello')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [(-2, 'hello'), (-3, 'hello world'), (-5, 'oh, hello')])
        q1 = re.compile('how')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [(-1, 'howdy')])
        q1 = re.compile('wherefore')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [])

    def test_search_in_deque_append_left(self):
        q1 = re.compile('hello')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [(-2, 'hello'), (-3, 'hello world'), (-5, 'oh, hello')])
        self.deck.appendleft('bye!')
        q1 = re.compile('hello')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [(-3, 'hello'), (-4, 'hello world')])

    def test_search_in_deque_append_right(self):
        q1 = re.compile('hello')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [(-2, 'hello'), (-3, 'hello world'), (-5, 'oh, hello')])
        self.deck.append('good')
        self.deck.append('bye!')
        q1 = re.compile('hello')
        resp = search_deque_for_regex(self.deck, q1)
        self.assertEqual(resp, [(-1, 'hello world'), (-3, 'oh, hello')])
