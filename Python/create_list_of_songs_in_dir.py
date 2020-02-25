# copied non-cloud Music dir into ~/Temp/Music

import glob
import os
import json

temp_dir = '/Users/matthew/Temp/Music/'
tracks = glob.iglob(f'{temp_dir}**', recursive=True)
tracks = [i for i in tracks if os.path.isfile(i)]

print(len(tracks))
print(tracks)

by_artist = {}
for t in tracks:
    artist, _, title = t[len(temp_dir):].split('/')
    if artist not in by_artist:
        by_artist[artist] = []
    by_artist[artist].append(title)

with open(f'{temp_dir}listings.json', 'w') as fout:
    json.dump(by_artist, fout, indent=4, sort_keys=True)
