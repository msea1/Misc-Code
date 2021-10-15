### ALIASES ###


# ADD OPTIONS
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias ls='ls --color=auto'
alias mkdir='mkdir -pv'
alias wget='wget -c'

# CDs
alias cd..="cd .."
alias code='cd ~/Code'
alias darkroom='cd ~/Code/imaging-tools'
alias gemini='cd ~/Code/gemini'
alias mothra='cd ~/Code/mothra'
alias sops='cd ~/Code/sops'
alias tomls='cd ~/Code/tomls'
alias tempd='cd ~/Misc'


# NEW COMMANDS
alias checkvpn='until ping -c1 173.226.206.206 >/dev/null 2>&1; do sleep 5 ; done'
alias diskspace="du -S | sort -n -r |more"
alias docklist='docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
alias dockstop='docker rm -f -v $(docker ps -a -q)'
alias img_cr='echo "nthomas,cmacleod,EDederick,bhadnott,imcgreer,mkinzel" | xsel -ib'
alias ld='ls -ABF --group-directories-first --color=auto'
alias ll='ls -AhlF --group-directories-first --color=auto'
alias files='xdg-open . &>/dev/null &'
alias qemu='make && ./provision.sh -X -i images -q -S -c && cinderblock -i provision -Q host/usr/bin/qemu-system-ppc'
alias root="sudo su -"
alias run_psql="docker run -d --net=test --name pg -p 5432:5432 -v $PSQL_DATA:/var/lib/postgresql/data -e POSTGRES_HOST_AUTH_METHOD=trust postgres:11.8"
alias sorry='sudo $(fc -ln -1)'
alias sudo_pw='cat ~/.sudo_pw | xsel -ib'
alias ungron="gron --ungron"
alias update='sudo_pw && sudo apt update && sudo apt -y upgrade && sudo apt dist-upgrade && sudo apt autoremove'
alias usb_f5='sudo usbmuxd -u -U usbmux'
alias vauth='vault auth -method=ldap username=$USER'
alias vssh='vault ssh -role otp_key_role'


# SHORTCUTS
alias g='git'
alias gps='pgrep -a'
alias h='history | grep'
alias pip='pip3'
alias py='python3'


# MACHINES
alias curve11='ssh -p 24022 root@192.168.6.11'
alias desktop='ssh mcarruth@192.168.40.14'
alias flatsat='ssh -p 24022 root@192.168.6.10'
alias pango='ssh spaceflight@pango-dish.service.fra.gemini'


# EDITING
alias bashalias='subl ~/.bash_aliases'
alias bashfx='subl ~/.bash_fxs'
alias bashrc='subl ~/.bashrc'
alias gitconfig='subl ~/.gitconfig'
