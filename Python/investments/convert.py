import re

from misc_code.Python.investments.goals import Regions


sectors = """
Basic Materials	 	3.89%
Communication Services	 	3.11%
Consumer Cyclical	 	11.56%
Consumer Defensive	 	3.46%
Energy	 	2.29%
Financial Services	 	13.94%
Healthcare	 	12.57%
Industrials	 	15.86%
Real Estate	 	11.98%
Technology	 	18.17%
Utilities	 	3.15%

"""

geography = """
Africa

1.4%

Asia Developed

16.0%

Asia Emerging

14.8%

Australasia

8.9%

Canada

2.6%

Europe Emerging

0.5%

Europe Ex Euro

5.1%

Eurozone

14.4%

Japan

24.4%

Latin America

2.1%

Middle East

2.5%

United Kingdom

7.1%

United States

0.3%
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
