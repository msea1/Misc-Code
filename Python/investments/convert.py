import re

from misc_code.Python.investments.goals import Regions


sectors = """
Basic Materials	 	4.52%
Communication Services	 	8.59%
Consumer Cyclical	 	10.41%
Consumer Defensive	 	7.87%
Energy	 	4.71%
Financial Services	 	17.43%
Healthcare	 	11.67%
Industrials	 	11.29%
Real Estate	 	4.15%
Technology	 	15.94%
Utilities	 	3.42%

"""

geography = """
Africa

0.6%

Asia Developed

4.2%

Asia Emerging

5.9%

Australasia

2.1%

Canada

3.0%

Europe Emerging

0.8%

Europe Ex Euro

4.6%

Eurozone

8.9%

Japan

7.4%

Latin America

1.4%

Middle East

0.7%

United Kingdom

5.0%

United States

55.4%
"""


def convert_sectors_to_list(usn_input):
    return [get_trailing_number(line) for line in usn_input.splitlines() if line != '']
    

def convert_geography_to_tuple(usn_input):
    init_list = {region: 0.0 for region in Regions._fields}
    cur_field = ''
    for line in usn_input.splitlines():
        if line == '':
            continue
        if line[0].isnumeric():
            init_list[cur_field] = float(line[:-1])
            cur_field = ''
        else:
            cur_field = '_'.join(line.strip().split())
    return list(Regions(**init_list))


def get_trailing_number(s):
    m = re.search(r'\d+\.\d+%$', s)
    return float(m.group()[:-1]) if m else 0


if __name__ == '__main__':
    print(convert_sectors_to_list(sectors))
    print(convert_geography_to_tuple(geography))
