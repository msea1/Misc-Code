import argparse
import json

from os.path import basename


# GLOBALS #
img_list = []


# MARKDOWN FXS #

def markdown_add_title(title):
    return f"# {title}\n\n"


def markdown_add_new_day(new_date):
    return f"## {new_date}\n\n"


def markdown_add_segue():
    return "---\n\n"


def markdown_add_image(alt_text, url=None, rel_path=None):
    global img_list
    img_list.append(url if url else rel_path)
    return f"![{alt_text}][{len(img_list)}]\n\n"


def print_img_refs():
    refs = ""
    for n, i in enumerate(img_list):
        refs += f"[{n+1}]: {i}\n"
    return refs


# TXT FORMAT #

def parse_txt(journal_file, out_file):
    pass


def parse_json(journal_file, out_file):
    md = markdown_add_title(basename(out_file))
    day = None
    with open(journal_file) as fin:
        journal = json.load(fin)
    entries = journal['entries']
    for entry in entries:
        weather = format_weather_json(entry['weather'])
        starred = entry['starred']
        geotag = format_location_json(entry['location'])
        _day, time = format_date_json(entry)
        if _day != day:
            md += markdown_add_new_day(_day)
            day = _day
        text = entry['text']


def format_date_json(entry):
    creation_date = entry['creationDate']  # convert to readable
    time_zone = entry['timeZone']  # convert to shorthand
    return 0, 0


def format_weather_json(weather_dict):
    return f'{weather_dict.get("conditionsDescription", "")} ' \
           f'{weather_dict.get("windChillCelsius", "Unk")}°C'


def format_location_json(location_info):
    geotag = ""
    fields = ["placeName", "localityName", "country"]
    for x in fields:
        if location_info.get(x):
            geotag += f"{location_info[x]} "
    geotag = geotag.strip()
    gps = f"{location_info.get('latitude', 0):.2f} " \
          f"{location_info.get('longitude', 0):.2f}"
    if not geotag:
        return gps
    return f"{geotag} {gps}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Turn Day One Journal into Markdown.')
    parser.add_argument('i', help='Input file, exported from Day One')
    parser.add_argument('o', help='Output file')
    args = parser.parse_args()
    # print(f'{args.i}')
    # print(f'{args.o}')
    if args.i.endswith('.txt'):
        parse_txt(args.i, args.o)
    elif args.i.endswith('.json'):
        parse_json(args.i, args.o)
    else:
        print(f'Invalid input file, needs to be a txt or json, not {args.i}')
        exit(1)

