#!/bin/sh

mogrify -format anki -quality 100 *.jpg
mogrify -format anki -quality 100 *.JPG
mogrify -format anki -quality 100 *.jpeg
mogrify -format anki -quality 100 *.png

convert '*.anki' -resize 250x250^ -quality 100 -gravity center -extent 250x250 -set filename:fname 'anki_%t' +adjoin '%[filename:fname].jpeg'

rm *.anki
