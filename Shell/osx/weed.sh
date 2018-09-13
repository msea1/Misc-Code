#!/usr/local/bin/bash

# take in a prefix
label=$1

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
# TODO group photos with same desc
i=1
for filename in ./photos/*; do
    [ -e "$filename" ] || continue
    [ ! -d "$filename" ] || continue

    desc=$(mdls -raw -name kMDItemDescription $filename);

    if [ ! "$desc" = "(null)" ]; then
        pre=${filename##*/}
        a="![${pre%.*}][$label$i]\n\n$desc\n\n[$label$i]: $filename\n\n\n\n"
        printf "$a" >> ./photos/output.md
        ((i++))
        $(mv $filename ./photos/parsed/$pre)
    fi
done
