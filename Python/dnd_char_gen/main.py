import argparse
import json

from dnd_char_gen.character import Character
from dnd_char_gen.load_data import Universe
from dnd_char_gen.data.format_from_xml import Universe

# TODO tests
# TODO add grading / sorting / matching
# TODO add input args
# TODO add personality and such, pull from DnD source, bots
# TODO parse traits from source


def parse_arguments(available_data):
    parser = argparse.ArgumentParser()
    # parser.add_argument('--points', choices=['buy'], default='buy')
    # parser.add_argument('--race', choices=list(available_data['races']), default=None)
    # parser.add_argument('--class', help='', default='all')
    # parser.add_argument('--background', help='', default='all')
    # parser.add_argument('--abilities', help='', default=None)
    # parser.add_argument('--alignment', help='', default='all')
    # parser.add_argument('--npc', type=bool, default=False)
    args = parser.parse_args()
    return args


def main():
    # all_data = Universe()
    u = Universe()
    u.load_data()
    u.combine_sources()
    u.clean_up_data()
    u.parse_data()
    # args = parse_arguments(all_data)
    # try:
    #     while True:  # or less than num chars spec'd from args
    god = Character(None)
    god.create(u.data)
    # print(json.dumps(god, indent=4))
    # pause until enter
    # except KeyboardInterrupt:
    #     exit(0)


if __name__ == '__main__':
    main()
