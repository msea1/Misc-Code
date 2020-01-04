from xml.dom import minidom

BREAK_BETWEEN_NOTES = "<hr />"


class Cleaner:
    def __init__(self):
        self.doc = minidom.parse('../evernote_export/notes.enex')

    def save_header_info(self):
        # <?xml version="1.0" encoding="UTF-8"?>
        # <note><title>G</title><content>
        pass

    def split_export_into_each_note(self):
        # break up by en-note
        en_export = self.doc.getElementsByTagName('en-export')[0]
        notes = en_export.getElementsByTagName('note')
        print(f'{len(notes)} notes found')
        return notes

    def note_metadata(self, single_note):
        # <created>20140605T010958Z</created><updated>20140925T061714Z</updated><tag>blitztura</tag><note-attributes><latitude>47.60806355819909</latitude><longitude>-122.3372990599948</longitude><altitude>34.76020812988281</altitude><author>Matthew Carruth</author><reminder-order>0</reminder-order><application-data key="textever.archived">1</application-data></note-attributes>
        pass


if __name__ == '__main__':
    c = Cleaner()
    notes = c.split_export_into_each_note()
    for n in notes:
        d = c.note_metadata(n)