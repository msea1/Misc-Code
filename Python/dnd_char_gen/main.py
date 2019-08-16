import argparse
import json

from dnd_char_gen.character import Character
from dnd_char_gen.load_data import load_data


def parse_arguments(available_data):
    parser = argparse.ArgumentParser()
    parser.add_argument('--points', choices=['normal'], default='normal')
    parser.add_argument('--race', choices=list(available_data['races']), default='human')
    parser.add_argument('--class', help='', default='all')
    parser.add_argument('--background', help='', default='all')
    parser.add_argument('--abilities', help='', default='all')
    parser.add_argument('--alignment', help='', default='all')
    parser.add_argument('--npc', help='', default='all')
    args = parser.parse_args()
    return args


def main():
    all_data = load_data()
    args = parse_arguments(all_data)
    # try:
    #     while True:  # or less than num chars spec'd from args
    god = Character(args)
    god.create(all_data)
    print(json.dumps(god, indent=4))
    # pause until enter
    # except KeyboardInterrupt:
    #     exit(0)


if __name__ == '__main__':
    main()
