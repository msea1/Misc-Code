import json
import unittest
import day_one_to_md as md


class TestMarkdownFormat(unittest.TestCase):

    def test_add_title(self):
        self.assertEqual(md.markdown_add_title('Hello'), '# Hello\n\n')

    def test_add_day(self):
        self.assertEqual(md.markdown_add_new_day('a date'), '## a date\n\n')

    def test_add_segue(self):
        self.assertEqual(md.markdown_add_segue(), '---\n\n')

    def test_add_image(self):
        self.assertEqual(md.markdown_add_image('Hello', url='http'), '![Hello][1]\n\n')
        self.assertEqual(md.markdown_add_image('Hello', rel_path='../photo'), '![Hello][2]\n\n')
        self.assertEqual(len(md.img_list), 2)
        self.assertEqual(md.img_list[0], 'http')
        self.assertEqual(md.img_list[1], '../photo')
        self.assertEqual(md.print_img_refs(), f"[1]: http\n[2]: ../photo\n")


class TestJsonFormat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = {}

    def test_weather_format(self):
        pass

    def test_location_format(self):
        pass

    def test_date_format(self):
        pass

    def test_json_single_entry(self):
        pass
