#!/bin/python3

import sys
from glob import glob
from os import rename
from os.path import basename, dirname, join
from re import sub

from mutagen import id3
from mutagen.mp3 import MP3

# pass in dir
song_dir = sys.argv[1] if len(sys.argv) > 1 else '/home/mcarruth/Audio/'  # getcwd()

# for each file in each dir
for song in glob(join(song_dir, '**/*.mp3'), recursive=True):
    handle = MP3(song)
    try:
        handle.add_tags()
    except Exception:
        pass

    artist = basename(dirname(song))
    if artist == basename(dirname(song_dir)):
        artist = basename(song)
        if 'Audio - ' in artist:
            artist = artist.replace('Audio - ', '')
        artist, title = artist.split(' - ')
    else:
        title = sub(r"\(.*\)", "", basename(song))

    title, _ = title.split('.mp3')
    tags = handle.tags
    tags.add(id3.TIT2(encoding=3, text=title))
    tags.add(id3.TPE1(encoding=3, text=artist))
    handle.save()
    new_name = f"{artist} - {title}"
    rename(song, f"{join(song_dir, f'{new_name}.mp3')}")
