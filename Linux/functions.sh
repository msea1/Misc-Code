### FUNCTIONS ###

cmdseqcli() {
  cd ~/Code/mothra/fsw/cmdseq-service
  py cmdseq/contact/cli.py
}

cdl() {
    builtin cd "${@}"
    if [ "$( ls | wc -l )" -gt 30 ] ; then
        ls --color=always | awk 'NR < 16 { print }; NR == 16 { print " (... snip ...)" }; { buffer[NR % 14] = $0 } END { for( i = NR + 1; i <= NR+14; i++ ) print buffer[i % 14] }'
    else
        ls
    fi
}

del_br() {
  local d=$(git rev-parse --abbrev-ref HEAD)
  g co master
  g branch -D $d
}

docker_clean(){
    docker rm -v $(docker ps --filter status=exited -q 2>/dev/null) 2>/dev/null
    docker rmi $(docker images --filter dangling=true -q 2>/dev/null) 2>/dev/null
}

docker_kill(){
  sudo systemctl stop docker
  sudo rm /var/lib/docker/linkgraph.db
  sudo rm -rf /var/lib/docker/containers/
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

gack() {
  ack --$1 --ignore-dir=.pants.d $2 ~/Code/gemini
}

search_type() {
  find . -iname "*\.$1" -print0 | xargs -0 ack $2
}

gemini_tests() {
  gemini
  ./pants test :: --tag=-integration --tag=uvloop_old --tag=-aioredis_new > ~/Temp/gemini_tests.out
  ./pants test :: --tag=-integration --tag=-uvloop_old --tag=-aioredis_new >> ~/Temp/gemini_tests.out
  ./pants test :: --tag=-integration --tag=-uvloop_old --tag=aioredis_new >> ~/Temp/gemini_tests.out
  grep -Eo '(.*):test.*\.\.\.\.\.   FAILURE' ~/Temp/gemini_tests.out | sort | uniq -c | awk '{print $4": "$2}' && grep -Eo '\.\.\.\.\.   SUCCESS' ~/Temp/gemini_tests.out | sort | uniq -c | awk '{print $3": "$1}'
}

gps() {
  arg=$1
  letter=${arg:0:1}
  brack='['$letter']'
  srch=$brack${arg:1}
  ps -ax | grep -i $srch
}

ipy() {
  work sandbox
  cd $HOME/.virtualenvs/sandbox/
  jupyter notebook
  deactivate
  cd -
}

work() {
  source $HOME/.virtualenvs/$1/bin/activate
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

new_venv() {
  py -m venv $HOME/.virtualenvs/$1
  work $1
}

pants_push(){
	gemini
  dir_path=${1::-1}
  svc_name=${dir_path##*/}
  echo -e 'cd /code\n./pants binary $1/::\nexit' > /tmp/binary.sh
  sudo docker run --rm -v ~/Code/gemini:/code -v /tmp/binary.sh:/dock.sh pants-build bash dock.sh $1
	sudo docker build -t registry.service.nsi.gemini/matthew/$svc_name -f $1/Dockerfile .
	sudo docker push registry.service.nsi.gemini/matthew/$svc_name
	cd -
}

tfe_plan() {
  : "${1?Need to pass TFE env e.g. 'prod'}"
  : "${ATLAS_TOKEN?Need to set ATLAS_TOKEN, available here: https://tfe.spaceflightindustries.com/app/settings/tokens}"
  TFE_ENV=$1
  TFE_URL="https://tfe.spaceflightindustries.com"
  current_run_endpoint=$(curl -s -H 'Content-Type: application/vnd.api+json' -H "Authorization: Bearer $ATLAS_TOKEN"  $TFE_URL/api/v2/organizations/bsg/workspaces/$TFE_ENV | jq -r '.data.relationships["current-run"].links.related')
  current_run_plan_endpoint=$(curl -s -H 'Content-Type: application/vnd.api+json' -H "Authorization: Bearer $ATLAS_TOKEN"  $TFE_URL/$current_run_endpoint | jq -r '.data.relationships.plan.links.related')
  current_run_plan_log=$(curl -s -H 'Content-Type: application/vnd.api+json' -H "Authorization: Bearer $ATLAS_TOKEN"  $TFE_URL/$current_run_plan_endpoint | jq -r '.data.attributes["log-read-url"]')

  curl -s $current_run_plan_log | landscape
}

parse_git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

recycle() {
  nmcli r wifi off
  nmcli networking off
  nmcli networking on
  nmcli r wifi on
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

vsat() {
  ip=$(($1 + 39))
  ssh -p 24022 root@10.234.1.$ip
}

pdt() {
  ip=$(($1 + 89))
  ssh -p 24022 root@10.234.1.$ip
}
