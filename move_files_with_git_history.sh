cd MiscCode/
git log Spreadsheets/Stock\ Options_mac.xlsx|grep ^commit|tail -1|awk '{print$2}'
rm /tmp/mergepatch/*
g format-patch -o /tmp/mergepatch -1 f17bfd1 Spreadsheets/Stock\ Options_mac.xlsx
git am --committer-date-is-author-date /tmp/mergepatch/*.patch
rm /tmp/mergepatch/*
g format-patch -o /tmp/mergepatch $(git log --no-color Stock\ Options.xlsx|grep ^commit|tail -1|awk '{print$2}')..HEAD Stock\ Options.xlsx
git am --committer-date-is-author-date /tmp/mergepatch/*.patch
g mv Spreadsheets/* ./
rm -rf Spreadsheets/
g aa
g cm 'rename'
g push

