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

code_rvw() {
  echo "erybczynski, MBlondeel, JHersch, jbrazel, CPeel" | xsel -ib
  arc diff $1
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

gps() {
  arg=$1
  letter=${arg:0:1}
  brack='['$letter']'
  srch=$brack${arg:1}
  ps -ax | grep -i $srch
}

ipy() {
  cd $HOME/Code/
  source ./sandbox/bin/activate
  jupyter notebook
  deactivate
  cd -
}

work() {
  source $HOME/Code/$1/bin/activate
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
  g fetch --prune
  g reset --hard
  g rebase
  g submodule update
  g co $d
  popd
}

new_venv() {
  py -m venv $2 $HOME/Code/$1
  work $1
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
