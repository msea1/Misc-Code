#!/usr/bin/env python

import argparse
import sys

import jinja2
import markdown
from bs4 import BeautifulSoup as soup

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.0/css/bootstrap-combined.min.css" rel="stylesheet">
    <style>
        body {
            font-family: sans-serif;
        }
        code, pre {
            font-family: monospace;
        }
        h1 code,
        h2 code,
        h3 code,
        h4 code,
        h5 code,
        h6 code {
            font-size: inherit;
        }
    </style>
</head>
<body>
<div class="container">
{{content}}
</div>
</body>
</html>
"""


def parse_args(args=None):
    d = 'Make a complete, styled HTML document from a Markdown file.'
    parser = argparse.ArgumentParser(description=d)
    parser.add_argument('mdfile', type=argparse.FileType('r'), nargs='?',
                        default=sys.stdin,
                        help='File to convert. Defaults to stdin.')
    parser.add_argument('-o', '--out', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='Output file name. Defaults to stdout.')
    return parser.parse_args(args)


def custom_format(html):
    html = adjust_image_size(html)
    html = replace_stars(html)
    html = htmlize_symbols(html)
    return html


def htmlize_symbols(html):
    html = html.encode('ascii', 'xmlcharrefreplace').decode()
    html = html.replace('</em>\n', '</em></p>\n<p>')
    html = html.replace('\n<em>', '</p>\n<p><em>')
    html = html.replace('<h2>', '<hr/><hr/><h2>')
    # html = str(html).replace('°', '&deg;')
    # html = str(html).replace('…', '...')
    # html = str(html).replace('’', '&apos;')
    return html


def replace_stars(html):
    data = str(html)
    i = 0
    last = 0
    while i != -1:
        i = data.find(':star:', i)
        if i == -1:
            continue
        last = data.rfind("<strong>", last, i)
        data = data[0:last] + "&starf; " + data[last:i] + data[i+6:]
        last = i
    return data

def adjust_image_size(html):
    all_img = html.find_all("img")
    for i in all_img:
        i.attrs['width'] = "400"
        i.attrs['alt'] = "(image)"
    return html


def main(args=None):
    args = parse_args(args)
    md = args.mdfile.read()
    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    souped = soup(html, 'html.parser')
    formatted = custom_format(souped)
    doc = jinja2.Template(TEMPLATE).render(content=formatted)
    args.out.write(doc)


if __name__ == '__main__':
    sys.exit(main())
