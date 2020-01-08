import re

BREAK_BETWEEN_NOTES = "<hr />"


with open('../evernote_export/notes.enex') as f:
    contents = f.read()

notes = re.findall(r"<note>(.*?)</note>", contents, re.MULTILINE | re.DOTALL)

ordered_by_title = {}
all_tags = set()

for note in notes:
    title = re.search(r"<title>(.*?)</title>", note, re.MULTILINE | re.DOTALL)
    # convert title to B
    # grab text of note only
    ordered_by_title[title.group(1)] = note

    tags = re.findall(r"<tag>(.*?)</tag>", note, re.MULTILINE | re.DOTALL)
    all_tags.update(set(tags))


# allow custom title of file and also title of note
with open('../import_evernote/test.enex', 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">\n')
    f.write('<en-export>\n')

    for o in sorted(ordered_by_title):
        f.write(ordered_by_title[o])
        f.write(BREAK_BETWEEN_NOTES)

    f.write('\n</en-export>')