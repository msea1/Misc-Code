#!/usr/bin/env bash

a="Filesystem Size Used Available Use% Mounted on\ndevtmpfs 245.8M 0 245.8M 0% /dev\ntmpfs 251.9M 4.0K 251.9M 0% /dev/shm\nnone 251.9M 16.0K 251.9M 0% /tmp\ntmpfs 251.9M 0 251.9M 0% /sys/fs/cgroup\nnone 251.9M 1.6M 250.3M 1% /var\n/dev/ubi1_8 90.4M 27.4M 63.0M 30% /var/log\n/dev/ubi1_1 15.3M 84.0K 14.3M 1% /var/sfs/parameters/1\n/dev/ubi1_7 15.3M 116.0K 14.3M 1% /var/sfs/scripts\n/dev/ubi1_6 90.4M 13.5M 72.3M 16% /var/sfs/maintenance\n/dev/ubi1_0 15.3M 180.0K 14.2M 1% /var/sfs/parameters/0\n/dev/ubi1_2 15.3M 84.0K 14.3M 1% /var/sfs/parameters/2\n/dev/ubi1_9 554.5M 229.4M 320.4M 42% /var/sfs/logs\ntmpfs 251.9M 312.0K 251.6M 0% /run\nnone 251.9M 16.0K 251.9M 0% /tmp\nnone 251.9M 1.6M 250.3M 1% /var/tmp\n"

set -f
printf -v str_l '%b' "$a"

while read -r l; do
    echo $l | sed -e 's/ / |,/g' | column -t -s,
done <<< "$str_l"
