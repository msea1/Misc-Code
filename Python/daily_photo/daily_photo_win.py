import os, random, shutil, sys

if len(sys.argv) > 1:
    num_photos = int(sys.argv[1])
else:
    num_photos = 1

all_photos = []
for x in os.walk("F:/Pictures/"):
    if 'Lightroom' not in x[0] and 'picasa' not in x[0] and '$RECYCLE.BIN' not in x[0]:
        files = [x[0]+'/'+name for name in x[2] if name.lower().endswith('.jpg')]
        all_photos.extend(files)
for i in range(0,num_photos):
    daily_photo = random.choice(all_photos)
    file_name = os.path.basename(daily_photo)
    shutil.copyfile(daily_photo, "C:/Users/Matthew/Google Drive/"+file_name)
