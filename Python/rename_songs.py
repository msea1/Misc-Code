#!/bin/python3

import sys

from os import getcwd, rename
from glob import glob
from os.path import basename, dirname, join
from re import sub

# pass in dir
song_dir = sys.argv[1] if len(sys.argv) > 1 else getcwd()

# for each file in each dir
for song in glob(join(song_dir, '**/*.mp3'), recursive=True):
    underbar = song.replace(' ', '_')
    artist = basename(dirname(underbar))
    title = sub(r"\(.*\)", "", basename(underbar))
    new_name = f"{artist}-{title}"
    rename(song, f"{join(song_dir, new_name)}")
