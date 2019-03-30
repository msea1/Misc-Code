# convert project_dump into usable HTML

import json
from os.path import join, dirname

url_file = join(dirname(__file__), 'project_dump.json')
with open(url_file) as fin:
    data = json.load(fin)

cities = set(b['school location'] for b in data.values() for _ in b.keys())
print(cities)

"""
Barrow
    Eben Hopson Memorial Middle School
        Contemporary Speakers for Contemporary Dance             $383       9 Donors
        Relax and Read!                                       $1,0002      22 Donors
"""

indiv_proj_template = ""
output_html = ""
grouped_data_list = []
# end up with sorted [{"city name": [{"school name": [{project_1}, ] } ] } ]
for project_id, project_data in data.items():
    pass

for city in grouped_data_list:
    for school in city:
        for project in school:
            this_proj = f'<tr><td></td><td></td>' \
                f'<td>{project["project html"]}</td>' \
                f'<td>{project["amount raised"].split()[0]}</td>' \
                f'<td></td>' \
                '</tr>'
