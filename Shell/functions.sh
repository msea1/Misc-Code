#!/usr/bin/env bash

### FUNCTIONS ###
add_pypaths() {
  PYTHONPATH=~/Code/gemini/dist/
  for dir in ~/Code/gemini/cli/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/libraries/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/services/*/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/submodules/gemini-mothra-tomls/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/submodules/obscura-plugins/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/test-utilities/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/tools/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  for dir in ~/Code/gemini/validation/*/; do PYTHONPATH=$PYTHONPATH:$dir; done
  export PYTHONPATH=$PYTHONPATH
}

author_by_file() {
  IFS=$'\n'
  cd "$1"
  LIST=""
  for i in $(find . -iname "*.$2"); do
    LIST="`git blame --line-porcelain "$i" | grep 'author ' | sed "s,author,," | tr -d ' '`
    $LIST"
  done
  echo "$LIST" | sort | uniq -ic | sort -nr
  unset IFS
}

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

del_br() {
  local d=$(git rev-parse --abbrev-ref HEAD)
  g co master
  g branch -D $d
}

del_rm_br() {
  # This is a dry run by default; you must pass --go to perform the actual deletions.
  remote_branches=$(git branch -aavv | grep matthew | sed -E 's#.*remotes/origin/(matthew[^[:space:]]*).*#\1#')
  for remote_branch in $remote_branches; do
    echo "Deleting remote branch $remote_branch"
    if [ "$1" = "--go" ]; then
      git push origin --delete $remote_branch
    fi
  done

  if [ "$1" != "--go" ]; then
    echo "This was a dry run. Pass --go to this command to actually delete the branches."
  fi
}

docker_clean(){
  docker rm -v $(docker ps --filter status=exited -q 2>/dev/null) 2>/dev/null
  docker rmi $(docker images --filter dangling=true -q 2>/dev/null) 2>/dev/null
}

docker_kill(){
  sudo systemctl stop docker
  sudo rm /var/lib/docker/linkgraph.db
  sudo rm -rf /var/lib/docker/containers/
  sudo mkdir /var/lib/docker/containers/
  sudo systemctl start docker
}

extract () {
 if [ -f $1 ] ; then
   case $1 in
     *.tar.bz2)   tar xvjf $1    ;;
     *.tar.gz)    tar xvzf $1    ;;
     *.bz2)       bunzip2 $1     ;;
     *.rar)       unrar x $1       ;;
     *.gz)        gunzip $1      ;;
     *.tar)       tar xvf $1     ;;
     *.tbz2)      tar xvjf $1    ;;
     *.tgz)       tar xvzf $1    ;;
     *.zip)       unzip $1       ;;
     *.Z)         uncompress $1  ;;
     *.7z)        7z x $1        ;;
     *.xz)        xz -d $1        ;;
     *)           echo "don't know how to extract '$1'..." ;;
   esac
 else
   echo "'$1' is not a valid file!"
 fi
}

full_update() {
  sudo_pw
  pushd -n $(pwd)
  gemini
  upd_master
  tomls
  upd_master
  popd
  update
}

gemini_tests() {
  gemini
  echo -e 'cd /code\n./test-all.sh > /tmp/tests.txt' > /tmp/tests.sh
  echo -e "grep -Eo '(.*):test.*\.\.\.\.\.   FAILURE' /tmp/tests.txt | sort | uniq -c | awk '{print \$4\": \"\$2}' && grep -Eo '\.\.\.\.\.   SUCCESS' /tmp/tests.txt | sort | uniq -c | awk '{print \$3\": \"\$1}'\nexit" >> /tmp/tests.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/tests.sh:/tests.sh pants-build bash tests.sh
  cd -
}

get_tag() {
  TAG=$(http GET ecr-proxy.service.nsi.gemini/v2/gemini/$1/tags/list?n=1000 | jq '.tags[]|select(test("master-[0-9]{8}-[0-9a-f]{9}"))' | sort | tail -n 1 | sed 's/"//g')
}

ipy() {
  work sandbox
  cd $HOME/.virtualenvs/sandbox/
  jupyter notebook
  deactivate
  cd -
}

mimas_qemu() {
  mimas
  ./mkmimas @mkconfig/arm64 make image
  ./mkmimas @mkconfig/arm64 export image output/mkmimas-amd64/
  cd output/mkmimas-amd64
  mkdir -p ./provision && tar -xf provision.tar.zst -C ./provision
  mimas-qemu.sh
}

new_venv() {
  py -m venv $HOME/.virtualenvs/$1
  work $1
}

package_repos() {
  full_update
  # use du -k --max-depth 4 | sort -rn
  # tomls  # /sap-toml ./sap_toml/ and ./tests/
  # tar --exclude-vcs-ignores --exclude-vcs -zcf ~/Misc/toml.tar .
  mimas
  tar --exclude-vcs-ignores --exclude-vcs \
  --exclude='./buildroot' \
  -zcf ~/Misc/mimas.tar .
  gemini
  tar --exclude-vcs-ignores --exclude-vcs \
  --exclude='./3rdparty/repos' \
  --exclude='**/.terraform' \
  --exclude='./libraries/obscura-workflow/obscura_workflow/files' \
  --exclude='./libraries/orekit-lib/orekit-data' \
  --exclude='./services/client-services/client-discovery/public' \
  --exclude='./services/client-services/constellation-map/public/static' \
  --exclude='./services/satellite-services/ephemeris/tests_ephemeris/stk_data_files' \
  --exclude='./submodules' \
  -zcf ~/Misc/gemini.tar .
}

parse_git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

parse_vpn() {
  # used to use nmcli con show --active but no longer works w/AnyConnect
  d=$(ip --json addr | grep broadcast | grep "172\.2")
  if [ "$d" ]; then
    e=$(echo $d | grep "\.19\.255")
    if [ "$e" ]; then  # also ifindex 20
      echo "(BSky)"
      return
    fi
    e=$(echo $d | grep "\.1\.255")
    if [ "$e" ]; then  # also ifindex 13
      echo "(MOC)"
      return
    fi
  fi
  d=$(ip --json addr | grep broadcast | grep "192\.168\.215\.255")
  if [ "$d" ]; then  # also, ifindex 21
    echo "(LeoS)"
    return
  fi
}

pex_build(){
  gemini
  # sudo docker build -t pants-build -f infrastructure/dockerfiles/pants-build/Dockerfile .
  # sudo rm -rf .pants.d/
  dir_path=${1::-1}
  svc_name=${dir_path##*/}
  echo -e 'cd /code\n./pants binary $1/::\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
  sudo chown $USER dist/$svc_name.pex
  cd -
}

pex_coverage(){
  gemini
  TEST_LOG_DIR="dist/coverage"
  COV_MODULES=$(find $1 -maxdepth 2 -name "__init__.py" | egrep -v '*/*test[s][_*]/*') || COV_MODULES=""
  COV_MODULES=$(echo ${COV_MODULES} | sed 's|/__init__.py||g' | sed 's| |,|g')
  echo $COV_MODULES
  echo -e 'cd /code\n./pants test $1:test --cache-test-pytest-ignore --test-pytest-coverage=$3 --test-pytest-coverage-output-dir=$2 --test-pytest-junit-xml-dir=$2\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1 $TEST_LOG_DIR $COV_MODULES
  cd -
}

pex_push(){
  gemini
  dir_path=${1::-1}
  svc_name=${dir_path##*/}
  echo -e 'cd /code\n./pants binary $1/::\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
  sudo docker build -t registry.service.nsi.gemini/matthew/$svc_name -f $1/Dockerfile .
  sudo docker push registry.service.nsi.gemini/matthew/$svc_name
  sudo chown $USER dist/$svc_name.pex
  cd -
}

pex_test(){
  gemini
  echo -e 'cd /code\n./pants test $1/:: --tag=-integration\nexit' > /tmp/binary.sh
  sudo docker run --net host --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
  cd -
}

qemu_scp() {
  scp root@192.168.13.8:$1 ./
}

quicklook(){
  # "decrypted SFX image" AND (*112_* OR *113_*) in PDP logs
  gemini
  work gemini
  aws s3 cp $"s3://bsg-gemini-images-prod-sfx-packets/$1" . 
  image=$(basename $1)
  ./dist/dioptra-cli.pex make_pan ./$image
  rm ./$image
  parts=(${image//_/ })
  rm ./$"${parts[1]}_${parts[0]}_pan.tiff"
}

release_diff() {
  # show changes in dir from $1 to $2
  echo Commits
  # g log --reverse --oneline $1..$2 -- ./
  g log --reverse --pretty="format:%h %s (%an, %ar)" $1..$2 -- ./
  echo
  echo Files Changed
  g diff --name-only $1 $2 ./
}

reset_origin() {
  local d=$(git rev-parse --abbrev-ref HEAD)
  g stash
  g fetch --prune
  g reset --hard origin/$d
  g su
}

search() {
  ag -Q -i "$1" -G "$2"$
}

search_code() {
  ag -Q -i "$1" -G "$2"$ --ignore-dir="*test*"
}

search_files() {
  local d="ag -l -Q -i \"${2}\" -G \"${1}\""
  for var in "${@:3}"; do
    d="$d | xargs ag -l -Q -i \"$var\""
  done
  eval "$d"
}

search_dioptra() {
  ag  --ignore-dir="*test*" -Q -i "$1" -G "$2"$ \
  libraries/blacksky-payload/ \
  libraries/image-processing/ \
  libraries/image-operations/ \
  libraries/image-utils/ \
  libraries/dioptra-work/ \
  services/imaging-services/
}

tablet() {
  cd ~/Downloads/Tablet
  sudo ./Pentablet_Driver.sh
}

tfe_plan() {
  : "${1?Need to pass TFE env e.g. 'prod'}"
  : "${ATLAS_TOKEN?Need to set ATLAS_TOKEN, available here: https://tfe.blacksky.com/app/settings/tokens}"
  TFE_ENV=$1
  TFE_URL="https://tfe.blacksky.com"
  current_run_endpoint=$(curl -s -H 'Content-Type: application/vnd.api+json' -H "Authorization: Bearer $ATLAS_TOKEN"  $TFE_URL/api/v2/organizations/bsg/workspaces/$TFE_ENV | jq -r '.data.relationships["current-run"].links.related')
  current_run_plan_endpoint=$(curl -s -H 'Content-Type: application/vnd.api+json' -H "Authorization: Bearer $ATLAS_TOKEN"  $TFE_URL/$current_run_endpoint | jq -r '.data.relationships.plan.links.related')
  current_run_plan_log=$(curl -s -H 'Content-Type: application/vnd.api+json' -H "Authorization: Bearer $ATLAS_TOKEN"  $TFE_URL/$current_run_plan_endpoint | jq -r '.data.attributes["log-read-url"]')

  curl -s $current_run_plan_log | landscape
}


title() { printf "\e]2;$*\a"; }

up(){
  local d=""
  limit=$1
  for ((i=1 ; i <= limit ; i++))
    do
      d=$d/..
    done
  d=$(echo $d | sed 's/^\///')
  if [ -z "$d" ]; then
    d=..
  fi
  cd $d
}

upd_master() {
  pushd -n $(pwd)
  local d=$(git rev-parse --abbrev-ref HEAD)
  g stash
  g co master
  g fetch --prune
  g reset --hard
  g rebase
  g submodule update
  g co $d
  popd
}

wifi_f5() {
  nmcli r wifi off
  nmcli networking off
  nmcli networking on
  nmcli r wifi on
}

work() {
  source $HOME/.virtualenvs/$1/bin/activate
}
