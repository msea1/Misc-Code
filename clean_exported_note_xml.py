from xml.dom import minidom
import xml.etree.ElementTree as ET

BREAK_BETWEEN_NOTES = "<hr />"


class Cleaner:
    def __init__(self):
        # self.doc = minidom.parse('../evernote_export/notes.enex')
        # with open('../evernote_export/notes.enex') as f:
        #     xml_in = f.read()
        self.et = ET.parse('../evernote_export/notes.enex')
        # self.et = ET.parse('../evernote_export/sample.xml')
        self.root = self.et.getroot()
        for c in self.root.findall('note'):
            title = c.get('title')
            contents = c.get('en-note')
            print(title, len(contents))

        # self.et = ET.fromstring(xml_in)
        # self.notes = self.split_export_into_each_note()

    def split_export_into_each_note(self):
        # break up by en-note
        en_export = self.doc.getElementsByTagName('en-export')[0]
        notes = en_export.getElementsByTagName('note')
        print(f'{len(notes)} notes found')
        return notes

    def append_header_info(self):
        return '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">\n'

    def sort_notes(self):
        # by created? updated? title in alpha?
        pass

    def output(self):
        with open('../import_evernote/output.enex', 'w') as f:
            f.write(self.append_header_info())
            for n in self.notes:
                f.write(n)


    def note_metadata(self, single_note):
        # <created>20140605T010958Z</created><updated>20140925T061714Z</updated><tag>blitztura</tag><note-attributes><latitude>47.60806355819909</latitude><longitude>-122.3372990599948</longitude><altitude>34.76020812988281</altitude><author>Matthew Carruth</author><reminder-order>0</reminder-order><application-data key="textever.archived">1</application-data></note-attributes>
        pass


if __name__ == '__main__':
    c = Cleaner()
