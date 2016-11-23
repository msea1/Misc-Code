#!/bin/sh

mogrify -format anki *.jpg
mogrify -format anki *.jpeg
mogrify -format anki *.png

convert '*.anki' -resize 125x125^ -gravity center -extent 125x125 -set filename:fname '%t_anki' +adjoin '%[filename:fname].jpeg'

rm *.anki
