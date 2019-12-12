#!/usr/bin/env bash

b="Key                Value\n
---                -----\n
lease_id           aws/creds/sfi-dev/f5c0c68a-3c96-8767-cc17-9ddd3a3bb65a\n
lease_duration     24h\n
lease_renewable    true\n
access_key         aaaaaaa\n
secret_key         TqA+bcsdfsdfgsdg\n
security_token     <nil>\n
"

touch test.txt
echo -e '[default]'
echo -e $b | while read -a line; do
    if [[ ${line[0]} == 'access_key' ]]; then
        echo -e 'aws_access_key_id =' ${line[1]} > test.txt
    fi
    if [[ ${line[0]} == 'secret_key' ]]; then
        echo -e 'aws_secret_access_key =' ${line[1]} >> test.txt
    fi
done
