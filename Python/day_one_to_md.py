import argparse
import json
from os.path import basename, dirname, join, splitext

import arrow
import pytz

# GLOBALS #
img_list = []


def format_entry(time, geo, weather, star, subtitle, text, image):
    entry = ''
    if subtitle:
        entry += f"**{subtitle}**:"
    if time:
        entry += f" _{time}_"
    if weather:
        entry += f" _{weather}_"
    entry += "\n"
    if image:
        entry += image
    if text:
        entry += f"{text}\n"
    if star:
        entry += ':star:'
    if geo:
        entry += f"_{geo}_"
    entry += "\n\n"
    return entry


def output_file(md_text, out_file):
    with open(out_file, 'w') as fout:
        fout.write(md_text)


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
    return f"\n![{alt_text}][{len(img_list)}]\n\n"


def print_img_refs():
    refs = ""
    for n, i in enumerate(img_list):
        refs += f"[{n+1}]: {i}\n"
    return refs


# TXT FORMAT #

def parse_txt(_journal_file, _out_file):
    pass


def parse_json(journal_file, out_file):
    md = markdown_add_title(splitext(basename(out_file))[0].title())
    day = None
    with open(journal_file) as fin:
        journal = json.load(fin)
    entries = journal['entries']
    for entry in entries:
        weather = format_weather_json(entry.get('weather', {}))
        starred = entry['starred']
        geotag = format_location_json(entry.get('location', {}))

        _day, time = format_date_json(entry)
        if _day != day:
            md += markdown_add_new_day(_day)
            day = _day
        else:
            md += markdown_add_segue()

        subtitle, text = format_text_json(entry['text'])

        image = ""
        if 'photos' in entry:
            img = entry['photos'][0]  # currently only handles 1 image per entry
            image = format_image_json(journal_file, img)

        md += format_entry(time, geotag, weather, starred, subtitle, text, image)

    md += f"\n\n{print_img_refs()}"
    output_file(md, out_file)


def format_text_json(text_str):
    subtitle_i = text_str.find('\n')
    if subtitle_i == -1:
        return text_str, ''
    subtitle = text_str[:subtitle_i]
    subtitle_i += 1
    while text_str[subtitle_i] == '\n':
        subtitle_i += 1

    if 'dayone-moment' not in text_str:
        return subtitle, text_str[subtitle_i:]

    start_of_moment = text_str.find('![](dayone')
    if start_of_moment == -1:
        return text_str

    prefix = text_str[subtitle_i:start_of_moment-2]
    postfix_i = text_str[start_of_moment:].find(')')+start_of_moment+1
    while postfix_i < len(text_str) and text_str[postfix_i] == '\n':
        postfix_i += 1
    postfix = text_str[postfix_i:]
    return subtitle, prefix+postfix


def format_image_json(file_dir, img_dict):
    path = dirname(file_dir)
    rel_path = join(path, 'photos', f'{img_dict["md5"]}.{img_dict["type"]}')
    return markdown_add_image(img_dict['md5'], rel_path=rel_path)


def format_date_json(entry):
    creation_date = entry['creationDate']
    adt = arrow.get(creation_date)

    time_zone = entry['timeZone'].replace('\\', '')
    matches = [x for x in pytz.all_timezones_set if time_zone in x]
    dt = adt.datetime
    if matches:
        dt = adt.datetime.astimezone(pytz.timezone(time_zone))
    day = dt.strftime('%a %d %b')
    time = dt.strftime('%T') + f" {dt.tzname()}"
    return day, time


def format_weather_json(weather_dict):
    desc = weather_dict.get("conditionsDescription", "")
    temp = str(weather_dict.get("windChillCelsius", ""))
    temp += '°C' if temp else ''
    output = desc if desc else ''
    output += f' {temp}' if temp and output else temp
    return output


def format_location_json(location_info):
    geotag = ""
    fields = ["placeName", "localityName", "country"]
    for x in fields:
        if location_info.get(x):
            geotag += f"{location_info[x]} "
    geotag = geotag.strip()
    gps = f"{location_info.get('latitude', 0):.3f}, " \
          f"{location_info.get('longitude', 0):.3f}"
    gps = gps if gps != '0.000, 0.000' else ''
    if not geotag:
        return gps
    return f"{geotag} {gps}".strip()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Turn Day One Journal into Markdown.')
    parser.add_argument('i', help='Input file, exported from Day One')
    parser.add_argument('o', help='Output file')
    args = parser.parse_args()
    if args.i.endswith('.txt'):
        parse_txt(args.i, args.o)
    elif args.i.endswith('.json'):
        parse_json(args.i, args.o)
    else:
        print(f'Invalid input file, needs to be a txt or json, not {args.i}')
        exit(1)
