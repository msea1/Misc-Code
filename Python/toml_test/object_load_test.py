import glob
import json
from os.path import isfile

import toml


def main():
    for test_file in glob.glob('samples/**', recursive=True):
        if not isfile(test_file):
            continue
        with open(test_file) as r:
            if test_file.endswith("toml"):
                contents = toml.load(r)
                print("toml")
            elif test_file.endswith("json"):
                contents = json.load(r)
                print("json")


if __name__ == "__main__":
    main()
