import re

BREAK_BETWEEN_NOTES = "<hr />"


with open('../evernote_export/notes.enex') as f:
    contents = f.read()

notes = re.findall(r"<note>(.*?)</note>", contents, re.MULTILINE | re.DOTALL)

ordered_by_title = {}
all_tags = set()
created_time = None

for note in notes:
    title = re.search(r"<title>(.*?)</title>", note, re.MULTILINE | re.DOTALL).group(1)
    contents = re.search(r"<en\-note.*?\">(.*?)</en\-note>", note, re.MULTILINE | re.DOTALL).group(1)
    ordered_by_title[title] = f'<h2>{title}</h2>\n{contents}\n\n\n'

    created = re.search(r"<created>(.*?)</created>", note, re.MULTILINE | re.DOTALL).group(1)
    if created_time is None or created_time > created:
        created_time = created

    tags = re.findall(r"<tag>(.*?)</tag>", note, re.MULTILINE | re.DOTALL)
    all_tags.update(set(tags))


# allow custom title of file and also title of note
with open('../import_evernote/test.enex', 'w') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">\n')
    f.write('<en-export>\n<note>\n')

    for o in sorted(ordered_by_title):
        f.write(ordered_by_title[o])
        f.write(BREAK_BETWEEN_NOTES)

    f.write('\n</note>\n</en-export>')
