from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson


def load_data():
    data_folder = join(dirname(dirname(abspath(__file__))), 'data')
    races = load_race_data(data_folder)

    return (races)


def load_race_data(folder):
    with open(join(folder, 'NPCRacesAddOn.xml')) as fin:
        xmldata = fin.read()
    json_data = xmljson.parker.data(fromstring(xmldata))
    races = {x['name']: x for x in json_data['race']}
    return races
