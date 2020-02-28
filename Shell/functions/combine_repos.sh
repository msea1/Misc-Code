g clone git@github.com:msea1/$1.git repo
cd misc_code
g remote add t ../repo/
g remote update
g co -b move_repo
g merge --no-commit --allow-unrelated-histories t/master
mkdir $1
find ./ -maxdepth 1 -name "*" -type f -exec mv -f {} ./$1/ \;
g aa && g cm 'move files'
g co master
g merge move_repo
g branch -D move_repo
g remote rm t
cd ..
rm -rf repo
