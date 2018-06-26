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

cinder() {
  check=$(ifconfig | grep -A 1 qemu | grep inet)
  if [ -z "$check" ]
    then nmcli d delete qemu-tap0
  fi
  cd ~/Code/block2/mothra/output/sp0
  make && cinderblock -i images/ -Q host/usr/bin/qemu-system-ppc
}

code_rvw() {
  echo "erybczynski, MBlondeel, JHersch, LTaylor, jbrazel, CPeel, Asmirnov" | xsel -ib
  arc diff $1
}

colors() {
    for i in {0..31} ; do echo "[7;(38;05;$i)mColor $i [0m    [7;(38;05;$(($i + 32)))mColor $(($i+32)) [0m  [7;(38;05;$(($i+64)))mColor $(($i+64)) [0m    [7;(38;05;$(($i + 96)))mColor $(($i+96)) [0m  [7;(38;05;$(($i+128)))mColor $(($i+128)) [0m  [7;(38;05;$(($i + 160)))mColor $(($i+160)) [0m    [7;(38;05;$(($i+192)))mColor $(($i+192)) [0m  [7;(38;05;$(($i + 224)))mColor $(($i+224))"; done; echo -n "[0m"
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

docker_local(){
  rsync -a --exclude='.*' ./ $HOME/code/devops/docker/sources/$1/
  cd $HOME/code/devops/docker
  sudo docker build -t $2 -f dockerfiles/$2.docker .
  cd -
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

get_certs() {
  cd ~
  wget http://confluence.spaceflightindustries.com/download/attachments/6230825/cert.tgz?version=1&modificationDate=1453854699441&api=v2
  sudo tar zxvf cert.tgz -C /usr/local/share/ca-certificates
  rm cert.tgz
  sudo dpkg-reconfigure ca-certificates
  update-ca-certificates
  cd -
}

gdb() {
  local d=$(git rev-parse --abbrev-ref HEAD)
  g co master
  g branch -D $d
}

gps() {
  arg=$1
  letter=${arg:0:1}
  brack='['$letter']'
  srch=$brack${arg:1}
  ps -ax | grep -i $srch
}

ipy_note() {
  cd $HOME/Code/jupyter_notebooks
  workon jupyter
  jupyter notebook
  deactivate
  cd -
}

work() {
  source $WORKON_HOME/$1/bin/activate
}

upd_master() {
  pushd -n $(pwd)
  mothra
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
  py -m venv $2 $WORKON_HOME/$1
  work $1
}

parse_git_branch() {
  git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(\1)/'
}

recycle() {
  nmcli r wifi off
  nmcli networking off
  nmcli r wifi on
  nmcli networking on
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
