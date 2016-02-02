import requests
import pdb
import re

# need login

def grabPhoto(url, photo):
    pdb.set_trace()
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(photo + ".jpg", 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

favPage = requests.get('https://500px.com/matthewcarruth/favorites')
pdb.set_trace()
regex = re.compile("data-photo-id=\"(\d+?)\">")
faveIDs = regex.findall(favPage.text)
for photo in faveIDs:
    photo = str(photo)
    photoPage = requests.get('http://500px.com/photo/' + photo)
    regex = re.compile("src=\"(.+?)\".*?class=\"the_photo\"")
    url = regex.findall(photoPage.text)
    grabPhoto(str(url[0]), photo)
