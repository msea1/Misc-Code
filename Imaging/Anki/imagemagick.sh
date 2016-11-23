#!/bin/sh

for f in *.jpg; do
mv -- "$f" "$f.jpeg"
done

for f in *.png; do
mv -- "$f" "$f.jpeg"
done

convert '*.jpeg' -resize 125x125^ -gravity center -extent 125x125 resize%03d.jpeg

#stop affixing of new extension
#have new file_name capture original file_name
