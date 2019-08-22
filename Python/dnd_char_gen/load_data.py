import json
from os.path import abspath, dirname, join


class Universe:
    def __init__(self):
        data_folder = join(dirname(abspath(__file__)), 'data')
        with open(join(data_folder, 'source.json')) as fin:
            self.data = json.load(fin)
