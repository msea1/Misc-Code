import json
from os.path import dirname, join

import requests
from bs4 import BeautifulSoup as soup

url_file = join(dirname(__file__), 'project_urls.txt')
with open(url_file) as fin:
    urls = fin.readlines()

project_data = {}

for project in urls:
    print(f"parsing {project}")
    data = {}
    html = requests.get(project)
    souped = soup(html.content, 'html.parser')

    data['project name'] = souped.find('title').text.strip().split(' | ')[0]
    data['project link'] = project
    data['project html'] = f'<a href=\"{data["project link"]}\">{data["project name"]}</a>'
    data['project_id'] = project.split('/')[-2]

    school_info = souped.find(id='school-details-all').find_all('li')
    data['school name'] = school_info[0].text.strip()
    # data['school name'] = school.text.strip().replace('\t', '').replace('\n', '-').replace('---', ' - ')
    data['school link'] = school_info[0].find('a', 'teacher-school').attrs['href']
    data['school location'] = school_info[1].text.strip().replace('\t', '').replace('\n', '')
    data['school html'] = f'<a href=\"{data["school link"]}\">{data["school name"]}</a>'

    teacher = souped.find('a', {'class': 'teacher-link'})
    data['teacher name'] = teacher.text.strip()
    data['teacher link'] = teacher.attrs['href']
    data['teacher html'] = f'<a href=\"{data["teacher link"]}\">{data["teacher name"]}</a>'

    goal = souped.find('ul', {'class': 'donation-stats'}).text
    try:
        data['number of donors'], data['amount raised'] = goal.split('\n')[1:2]
    except ValueError:
        avail_info = goal.split('\n')[1]
        if 'donors' not in avail_info:
            data['amount raised'] = avail_info
        else:
            data['number of donors'] = avail_info

    students = souped.find('div', {'class': 'js-about-students'})
    data['students desc'] = " \n\n ".join([r.text for r in list(students.children) if r.text != ""])

    project = souped.find('div', {'class': 'js-about-project'})
    data['project desc'] = " \n\n ".join([r.text for r in list(project.children) if r.text != ""])

    materials = souped.find('table', {'class': 'materials-table'})
    material_list = [item.text.strip().replace('\t', '').replace('\n', '') for item in
                     materials.find_all('td', {'class': 'itemName'})]
    data['materials bought'] = ", ".join(material_list)


    # table = souped.find(lambda tag: tag.name=='ol' and tag.has_attr('class') and tag['class']=="activity")
    # rows = table.find_all(lambda tag: tag.name=='tr')

    # activity = souped.find(id='activity')
    # print(activity)
    # print(activity.find_all('li'))
 # https://www.donorschoose.org/project/stem-fairy-tale-kits/3976179/#project-activity

    teacher_comments = [item.text.strip().replace('\t', '').replace('\n', '') for item in
                        souped.find_all('div', {'class': 'teacher-comment'})]
    data['teacher updates'] = " \n\n ".join(teacher_comments)

    data['project started'] = souped.find('li', id="pm-1")

    # print(json.dumps(data, indent=4, sort_keys=True))

    project_data[data['project_id']] = data

# Fields left: ['timeline of donations', 'materials bought', 'teacher updates']
# Fields Got: ['project name', 'project link', 'project html', 'school name', 'school link', 'school html', 'teacher name', 'teacher link', 'teacher html', 'number of donors', 'amount raised', 'students desc', 'project desc', 'project started']

# cities = set(data['school location'] for data in project_data.values())

cities = set(b['school location'] for b in project_data.values() for _ in b.keys())
print(cities)

dump_file = join(dirname(__file__), 'project_dump.json')
with open(dump_file, 'w+') as fout:
    json.dump(project_data, fout)
