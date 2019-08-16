from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson


def load_data():
    data_folder = join(dirname(dirname(abspath(__file__))), 'data')
    load_core(data_folder)
    load_eberron(data_folder)
    races = load_npc_race_data(data_folder)
    return {'races': races}


def load_core(folder):
    with open(join(folder, 'Core.xml')) as fin:
        xmldata = fin.read()
    json_data = xmljson.parker.data(fromstring(xmldata))
    bgs = {x['name']: x for x in json_data['background']}
    dnd_classes = {x['name']: x for x in json_data['class']}
    feats = {x['name']: x for x in json_data['feat']}
    items = {x['name']: x for x in json_data['item']}
    monsters = {x['name']: x for x in json_data['monster']}
    races = {x['name']: x for x in json_data['race']}
    spells = {x['name']: x for x in json_data['spell']}


def load_eberron(folder):
    with open(join(folder, 'EberronAddOn.xml')) as fin:
        xmldata = fin.read()
    json_data = xmljson.parker.data(fromstring(xmldata))
    bgs = {x['name']: x for x in json_data['background']}
    feats = {x['name']: x for x in json_data['feat']}
    items = {x['name']: x for x in json_data['item']}
    monsters = {x['name']: x for x in json_data['monster']}
    races = {x['name']: x for x in json_data['race']}


def load_npc_race_data(folder):
    with open(join(folder, 'NPCRacesAddOn.xml')) as fin:
        xmldata = fin.read()
    json_data = xmljson.parker.data(fromstring(xmldata))
    races = {x['name']: x for x in json_data['race']}
    return races
