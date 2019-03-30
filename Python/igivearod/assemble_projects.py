# convert project_dump into usable HTML

import json
from os.path import join, dirname

url_file = join(dirname(__file__), 'project_dump.json')
with open(url_file) as fin:
    data = json.load(fin)

url_file = join(dirname(__file__), 'city_dump.json')
with open(url_file) as fin:
    city_data = json.load(fin)

url_file = join(dirname(__file__), 'school_dump.json')
with open(url_file) as fin:
    school_data = json.load(fin)

# cities = set(b['school location'] for b in data.values() for _ in b.keys())
# print(cities)

"""
Barrow
    Eben Hopson Memorial Middle School
        Contemporary Speakers for Contemporary Dance             $383       9 Donors
        Relax and Read!                                       $1,0002      22 Donors
"""

output_html = "<table><tr><th>CITY</th><th>SCHOOL</th><th>PROJECT</th><th>$ RAISED</th><th>DONORS</th></tr>"

grouped_data_list = []
# end up with sorted [{"city name": [{"school name": [{project_1}, ] } ] } ]
for project_id, project_data in data.items():
    city_key = city_data.get(project_data['school location'], {})
    school_key = city_key.get(project_data['school name'], [])
    school_key.append(project_data)
    city_key[project_data['school name']] = school_key
    city_data[project_data['school location']] = city_key


for city, city_projects in sorted(city_data.items()):
    output_html += f'<tr><td>{city}</td></tr>'
    for school, school_projects in sorted(city_projects.items()):
        if len(school_projects) == 0:
            continue
        output_html += f'<tr><td></td><td>{school_projects[0]["school html"]}</tr>'
        for project in school_projects:
            goal = project["amount raised"].split()[0] if "goal" in project["amount raised"] else None
            if not goal:
                if 'goal' in project['number of donors']:
                    goal = project["number of donors"].split()[0]
                else:
                    goal = "N/A"

            donors = project["amount raised"] if "donors" in project["amount raised"] else None
            if not donors:
                if 'donors' in project['number of donors']:
                    donors = project["number of donors"]
                else:
                    donors = "N/A"

            this_proj = '<tr><td></td><td></td>' \
                f'<td>{project["project html"]}</td>' \
                f'<td>{goal}</td>' \
                f'<td>{donors}</td></tr>'
            output_html += this_proj


dump_file = join(dirname(__file__), 'projects_html.html')
with open(dump_file, 'w+') as fout:
    fout.write(output_html)

