import unittest

from day_one_journal import day_one_to_md as md


class TestMarkdownFormat(unittest.TestCase):

    def test_add_title(self):
        self.assertEqual(md.markdown_add_title('Hello'), '# Hello\n\n')

    def test_add_day(self):
        self.assertEqual(md.markdown_add_new_day('a date'), '## a date\n\n')

    def test_add_segue(self):
        self.assertEqual(md.markdown_add_segue(), '---\n\n')

    def test_add_image(self):
        self.assertEqual(md.markdown_add_image('Hello', url='http'), '\n![Hello][1]\n\n')
        self.assertEqual(md.markdown_add_image('Hello', rel_path='../photo'), '\n![Hello][2]\n\n')
        self.assertEqual(len(md.img_list), 2)
        self.assertEqual(md.img_list[0], 'http')
        self.assertEqual(md.img_list[1], '../photo')
        self.assertEqual(md.print_img_refs(), f"[1]: http\n[2]: ../photo\n")


class TestJsonFormat(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.input = {"entries" : [
        {
          "weather" : {
            "sunsetDate" : "2018-05-19T00:02:21Z",
            "temperatureCelsius" : 10.600000381469727,
            "weatherServiceName" : "HAMweather",
            "windBearing" : 110,
            "sunriseDate" : "2018-05-18T09:18:43Z",
            "conditionsDescription" : "Cloudy",
            "pressureMB" : 1030,
            "visibilityKM" : 16.093439102172852,
            "relativeHumidity" : 54,
            "windSpeedKPH" : 15,
            "weatherCode" : "cloudy",
            "windChillCelsius" : 11
          },
          "uuid" : "7ACE5A469B0A4E95A622C4342DDCFA0E",
          "photos" : [
            {
              "cameraMake" : "Apple",
              "fnumber" : "1.8",
              "orderInEntry" : 0,
              "lensMake" : "Apple",
              "width" : 1575,
              "cameraModel" : "iPhone 7",
              "type" : "jpeg",
              "identifier" : "771BFB4BA8E04650B70E0F0C3E07A559",
              "date" : "2018-05-18T23:59:54Z",
              "exposureBiasValue" : 0,
              "location" : {
                "region" : {
                  "center" : {
                    "longitude" : -71.018013000488281,
                    "latitude" : 42.367694848285133
                  },
                  "identifier" : "<+42.36769485,-71.01801300> radius 141.69",
                  "radius" : 141.68706608790438
                },
                "localityName" : "Boston",
                "country" : "United States",
                "timeZoneName" : "America\/New_York",
                "administrativeArea" : "MA",
                "longitude" : -71.018013000488281,
                "placeName" : "Boston Logan International Airport",
                "latitude" : 42.367694854736328
              },
              "height" : 2100,
              "lensModel" : "iPhone 7 back camera 3.99mm f\/1.8",
              "weather" : {
                "sunsetDate" : "2018-05-19T00:02:21Z",
                "temperatureCelsius" : 10.600000381469727,
                "weatherServiceName" : "HAMweather",
                "windBearing" : 110,
                "sunriseDate" : "2018-05-18T09:18:43Z",
                "conditionsDescription" : "Cloudy",
                "pressureMB" : 1030,
                "visibilityKM" : 16.093439102172852,
                "relativeHumidity" : 54,
                "windSpeedKPH" : 15,
                "weatherCode" : "cloudy",
                "windChillCelsius" : 11
              },
              "md5" : "2b9cabb0f836b94993374549f617b8f6",
              "focalLength" : "3.99"
            }
          ],
          "creationDeviceModel" : "iPhone9,3",
          "creationDeviceType" : "iPhone",
          "starred" : False,
          "location" : {
            "region" : {
              "center" : {
                "longitude" : -71.018013000488281,
                "latitude" : 42.367694848285133
              },
              "identifier" : "<+42.36769485,-71.01801300> radius 141.69",
              "radius" : 141.68706608790438
            },
            "localityName" : "Boston",
            "country" : "United States",
            "timeZoneName" : "America\/New_York",
            "administrativeArea" : "MA",
            "longitude" : -71.018013000488281,
            "placeName" : "Boston Logan International Airport",
            "latitude" : 42.367694854736328
          },
          "creationDate" : "2018-05-18T23:59:54Z",
          "creationOSVersion" : "11.3.1",
          "text" : "Airport snacking $9.50\n\n![](dayone-moment:\/\/771BFB4BA8E04650B70E0F0C3E07A559)\n\nShould not have done this. Overfed, predictably, on the flight. But I was bored.",
          "timeZone" : "America\/New_York",
          "creationOSName" : "iOS",
          "creationDevice" : "iPhone",
          "duration" : 0
        },
        ]}

    def test_weather_format(self):
        self.assertEqual("", md.format_weather_json(
            {"conditionsDescription": "", "windChillCelsius": ""}))
        self.assertEqual("Cloudy", md.format_weather_json(
            {"conditionsDescription": "Cloudy", "windChillCelsius": ""}))
        self.assertEqual("12°C", md.format_weather_json(
            {"conditionsDescription": "", "windChillCelsius": "12"}))

    def test_location_format(self):
        pass

    def test_date_format(self):
        with self.assertRaises(KeyError):
            md.format_date_json({})

        self.assertEqual(("Sat 19 May", "22:05:44 +04"), md.format_date_json(
            {"creationDate": "2018-05-19T18:05:44Z", "timeZone": "Asia\/Baku"}))

    def test_json_single_entry(self):
        pass

    def test_json_text(self):
        resp = md.format_text_json(
            "A square-about\n\n![](dayone-moment:\/\/72D8DEF02D3B471CB9F7A32996F1B8B2)\n\nBless you Soviet Urban planning")
        self.assertEqual(resp, ('A square-about', 'Bless you Soviet Urban planning'))
        resp = md.format_text_json(
            "Departure\nThe start of a long trip always seems overwhelming to me because I'm viewing the trip as a "
            "whole rather than just what the day in front of me holds. Big surprise I'm not in the moment.\n\n"
            "Fittingly it begins raining as we depart.")
        self.assertEqual(resp, ("Departure", "The start of a long trip always seems overwhelming to me because "
                               "I'm viewing the trip as a whole rather than just what the day in front of me holds. "
                               "Big surprise I'm not in the moment.\n\nFittingly it begins raining as we depart."))
        resp = md.format_text_json("Noravank. Wow")
        self.assertEqual(resp, ("Noravank. Wow", ""))
