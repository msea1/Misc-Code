
"""
tell application "Music"
	set t to {}
	set all_tracks to every track of library playlist id 64
	repeat with tune in all_tracks
		set end of t to {artist of tune, name of tune, id of tune, cloud status of tune}
	end repeat
	t
end tell
"""
from difflib import SequenceMatcher


def amend_string(input):
    return " ".join([word.strip() for word in re.split("\W+", input) if word.lower() not in IGNORE_WORDS])


def build_dict(m_dict, m_key, m_value):
    if m_key not in m_dict:
        m_dict[m_key] = []
    m_dict[m_key].append(m_value)


import re
entry = re.compile(r'{(.+?), *(.+?), *(.+?), *(.+?)},*', re.M | re.I)

IGNORE_WORDS = ['{', '\'']

with open('./all_tracks.txt') as f:
    track_data = f.read()

cloud_artists = {}
local_artists = {}
# def_dupes = {}
possible_dupes = {}
for match in re.finditer(entry, track_data):
    amended_artist = amend_string(match.group(1))
    amended_song = amend_string(match.group(2))

    if match.group(4) == 'subscription':
        build_dict(cloud_artists, amended_artist.strip(), amended_song.strip())
    else:
        build_dict(local_artists, amended_artist.strip(), amended_song.strip())

# comparing dicts, softly, artist and key
for artist, songlist in local_artists.items():
    for apple_artists, apple_songs in cloud_artists.items():
        check = SequenceMatcher(None, artist, apple_artists).ratio()
        if check > 0.5:
            for song in songlist:
                for cloud_song in apple_songs:
                    check = SequenceMatcher(None, song, cloud_song).ratio()
                    if check > 0.5:
                        build_dict(possible_dupes, artist.strip(), song.strip())

print(possible_dupes)
