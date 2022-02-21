cd dnd_work/
git filter-branch --subdirectory-filter svg_work/player_reference -- --all
cd ..
g clone git@github.com:msea1/DnD5ePlayerRef.git
cd DnD5ePlayerRef/
g remote add source-rep ../dnd_work/
g fetch source-rep
g remote rm source-rep
g co -b main
g branch -d master
g pb
cd ../dnd_work/
g reset --hard origin/master




g clone git@github.com:msea1/DnD-SVG.git
cd dnd_work/
git filter-branch --subdirectory-filter svg_work -- --all
cd ../DnD-SVG/
g remote add source-rep ../dnd_work/
g fetch source-rep
g co master
g co -b main
g remote rm source-rep
g branch -d master
g pb
cd ..
rm -rf DnD-SVG/
rm -rf dnd_work/

