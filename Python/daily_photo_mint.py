import os
import random
import shutil
import sys
from subprocess import call

PHOTO_DIR = '/media/matthew/WD/Pictures/'
PUSH_DIR = '/home/matthew/Documents/Google_Drive/'

if len(sys.argv) > 1:
    num_photos = int(sys.argv[1])
else:
    num_photos = 1

all_photos = []
photo_files = []
for x in os.walk(PHOTO_DIR):
    if 'Lightroom' not in x[0] and 'picasa' not in x[0] and '$RECYCLE.BIN' not in x[0]:
        files = [x[0]+'/'+name for name in x[2] if name.lower().endswith('.jpg')]
        all_photos.extend(files)
for i in range(0,num_photos):
    daily_photo = random.choice(all_photos)
    file_name = os.path.basename(daily_photo)
    shutil.copyfile(daily_photo, PUSH_DIR+file_name)
    photo_files.append(file_name)

os.chdir(PUSH_DIR)
call(['drive', 'push', '-quiet', '--destination', 'Temp/'])
for photo in photo_files:
    os.remove(photo)
