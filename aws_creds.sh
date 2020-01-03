#!/usr/bin/env bash

aws_creds() {
  touch ~/.aws/credentials
  echo -e '[default]' > ~/.aws/credentials
  ttl=$(vault token lookup | tail -1 | awk '{print $2}')
  if [[ $ttl -le 0 ]]; then
    vauth
  fi
  vault read aws/creds/sfi-imaging | while read -a line; do
    if [[ ${line[0]} == 'access_key' ]]; then
      echo -e 'aws_access_key_id =' ${line[1]} >> ~/.aws/credentials
    fi
    if [[ ${line[0]} == 'secret_key' ]]; then
      echo -e 'aws_secret_access_key =' ${line[1]} >> ~/.aws/credentials
    fi
  done
}
