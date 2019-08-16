import unittest
from os.path import abspath, dirname, join
from xml.etree.ElementTree import fromstring

import xmljson


class TestRacesXML(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data_folder = join(dirname(dirname(abspath(__file__))), 'data')
        with open(join(data_folder, 'NPCRacesAddOn.xml')) as fin:
            xmldata = fin.read()
        cls.json_data = xmljson.parker.data(fromstring(xmldata))

    def test_get_all_races(self):
        races = {x['name']: x for x in self.json_data['race']}
        self.assertEqual(['Bullywug (NPC)', 'Gnoll (NPC)', 'Goblin (NPC)', 'Grimlock (NPC)', 'Hobgoblin (NPC)',
                          'Kenku (NPC)', 'Kobold (NPC)', 'Kuo-toa (NPC)', 'Lizardfolk (NPC)', 'Merfolk (NPC)',
                          'Orc (NPC)', 'Skeleton (NPC)', 'Troglodyte (NPC)', 'Zombie (NPC)'], list(races))
