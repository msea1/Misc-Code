#!/usr/bin/python3

import sys
from os import listdir, rename, getcwd
from os.path import isfile, join, splitext, basename
import subprocess

# python3 -d photo_weed.py a $PWD/photos $PWD/photos/output.md

label = sys.argv[1] if len(sys.argv) > 1 else ''
photo_path = sys.argv[2] if len(sys.argv) > 2 else join(getcwd(), 'photos/')
output_path = sys.argv[3] if len(sys.argv) > 3 else join(getcwd(), 'photos/output.md')

unique_desc = {}

# foreach photo in this folder 
# check for a description in the metadata
# yields (null) if empty --> leave as is
# else, copy desc, append to output md, mv img to new folder

# output MD format
## ![<file_name>][<prefix>]
## 
## <desc>
## 
## [<prefix>]: ./photos/<file_name>
## 
##

# TODO in chron order? [kMDItemContentCreationDate]
files = [join(photo_path, f) for f in listdir(photo_path) if isfile(join(photo_path, f))]
for f in files: 
    desc = subprocess.getoutput(f"mdls -raw -name kMDItemDescription {f}")
    if desc != '(null)':
        if desc not in unique_desc:
            unique_desc[desc] = [f]
        else: 
            unique_desc[desc].append(f)
        rename(f, join(photo_path, f"parsed/{basename(f)}"))

i = 1
with open(output_path, 'w') as fout:
    for desc, files in unique_desc.items():
        preamble = "\n".join([f"![{splitext(basename(f))[0]}][{label}{j + i}]" for j, f in enumerate(files)])
        desc = f"\n\n{desc}\n\n"
        ref = "\n".join([f"[{label}{j + i}]: ./photos/{basename(f)}" for j, f in enumerate(files)])
        fout.write(preamble + desc + ref + "\n\n\n")
        i += len(files) 
