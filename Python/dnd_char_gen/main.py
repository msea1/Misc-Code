import argparse
import json

from dnd_char_gen.character import Character
from dnd_char_gen.load_data import load_data


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--points', help='', default='all')
    args = parser.parse_args()
    return args


def main():
    load_data()
    args = parse_arguments()

    if args.points != "all":
        pass
    else:
        pass
    try:
        while True:  # or less than num chars spec'd from args
            god = Character()
            print(json.dumps(god, indent=4))
            # pause until enter
    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
