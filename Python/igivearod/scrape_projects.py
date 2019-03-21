import json
import requests
from bs4 import BeautifulSoup as soup

sample_url = 'https://www.donorschoose.org/project/alaska-1130-earthquake-help/3814450/'
sample_url = 'https://www.donorschoose.org/project/i-see-a-food-chain-in-the-sea/3921300/'

html = requests.get(sample_url)
souped = soup(html.content, 'html.parser')

data = {
    'project name': "",
    'project link': "",
    'project html': "",

    'school name': "",
    'school link': "",
    'school html': "",

    'teacher name': "",
    'teacher link': "",
    'teacher html': "",

    'number of donors': "",
    'amount raised': "",
    'timeline of donations': "",
    'students desc': "",
    'project desc': "",
    'materials bought': "",
    'teacher updates': "",
}

data['project name'] = souped.find('title').text.strip().split(' | ')[0]
data['project link'] = sample_url
data['project html'] = f'<a href=\"{data["project link"]}\">{data["project name"]}</a>'

school = souped.find(id='school-details-all')
data['school name'] = school.text.strip().replace('\t', '').replace('\n', '-').replace('---', ' - ')
data['school link'] = school.find('a', 'teacher-school').attrs['href']
data['school html'] = f'<a href=\"{data["school link"]}\">{data["school name"]}</a>'

teacher = souped.find('a', {'class': 'teacher-link'})
data['teacher name'] = teacher.text.strip()
data['teacher link'] = teacher.attrs['href']
data['teacher html'] = f'<a href=\"{data["teacher link"]}\">{data["teacher name"]}</a>'

goal = souped.find('ul', {'class': 'donation-stats'}).text
_, data['number of donors'], data['amount raised'], _ = goal.split('\n')

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

teacher_comments = [item.text.strip().replace('\t', '').replace('\n', '') for item in
                    souped.find_all('div', {'class': 'teacher-comment'})]
data['teacher updates'] = " \n\n ".join(teacher_comments)

data['project started'] = souped.find('li', id="pm-1")

print(json.dumps(data, indent=4, sort_keys=True))

print(f"Fields left: {[k for k, v in data.items() if v == '']}")
print(f"Fields Got: {[k for k, v in data.items() if v != '']}")
