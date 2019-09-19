from os import listdir
from os.path import basename, join, isfile
import glob

"""
Usage case: getting G3 payload temps from kix
$ rm -rf /tmp/kix/
$ sudo docker pull registry.service.nsi.gemini/gemini/kix:latest
$ sudo docker run -it --dns=10.234.0.200 -v /tmp/kix:/tmp/kix --rm registry.service.nsi.gemini/gemini/kix:latest
# cd /srv

srv# kix.pex export -e prod --path g3_temps2.db --start-time 2019-08-21T14:37:02+00:00 --metric-whitelist payload 
--metric-blacklist adcs,groundstation,eps,raw,absent --tag-whitelist spacecraft_id=103 --end-time 2019-08-24

srv# kix.pex csv --path g3_temps2.db --output /tmp/kix/csv

$ sudo chown $USER /tmp/kix/**
$ cd ~/Code/personal/misc/Python/misc_blacksky
$ py combine_kix.py
"""

directory = '/tmp/kix/csv/'
value_dict = {}
header = 'Timestamp,'
times_in_file = {}
files = len([name for name in listdir(directory) if isfile(join(directory, name))])
file_num = 0
for file in glob.iglob(join(directory, '*.csv')):
    times_in_file = {}
    header += f"{basename(file)},"
    file_num += 1
    with open(file) as fin:
        data = fin.readlines()
        for line in data:
            timestamp, value, *args = line.split(',')
            if timestamp == 'timestamp' or timestamp in times_in_file:
                continue
            times_in_file[timestamp] = True
            if timestamp not in value_dict:
                value_dict[timestamp] = ['']*files
            value_dict[timestamp][file_num-1] = value

with open('/tmp/kix/output.csv', 'w') as fout:
    fout.write(f"{header}\n")
    for k in sorted(value_dict):
        v = value_dict[k]
        values_at_k = ",".join(v)
        fout.write(f"{k},{values_at_k}\n")
