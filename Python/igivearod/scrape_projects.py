import requests
from bs4 import BeautifulSoup as soup


sample_url = 'https://www.donorschoose.org/project/alaska-1130-earthquake-help/3814450/'
html = requests.get(sample_url)
souped = soup(html.content, 'html.parser')

info_to_get = ['teacher link',
               'school link',
               'number of donors',
               'amount raised',
               'timeline of donations',
               'students desc',
               'project desc',
               'materials bought',
               'teacher updates']

project_title = souped.find('title').string
project_school = souped.find(id='school-details-all').text.strip().replace(
    '\t','').replace('\n', '-').replace('---', ', ')

