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
alias gemini='cd ~/Code/gemini'
alias mothra='cd ~/Code/mothra'
alias tomls='cd ~/Code/tomls'
alias tempd='cd ~/Temp'


# NEW COMMANDS
alias diskspace="du -S | sort -n -r |more"
alias docklist='docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
alias dockstop='docker rm -f -v $(docker ps -a -q)'
alias code_review='echo "bwolfe, erybczynski, MBlondeel, JHersch, zelan, darreng, nsteffen" | xsel -ib'
alias img_review='echo "MBlondeel, MKinzel, EDederick, imcgreer" | xsel -ib'
alias ld='ls -ABF --group-directories-first --color=auto'
alias ll='ls -AhlF --group-directories-first --color=auto'
alias files='xdg-open .'
alias qemu='make && ./provision.sh -X -i images -q -S -c && cinderblock -i provision -Q host/usr/bin/qemu-system-ppc'
alias root="sudo su -"
alias sorry='sudo $(fc -ln -1)'
alias update='sudo apt update && sudo apt -y upgrade && sudo apt dist-upgrade && sudo apt autoremove'
alias usb_f5='sudo usbmuxd -u -U usbmux'
alias vauth='vault auth -method=ldap username=$USER'
alias vssh='vault ssh -role otp_key_role'


# SHORTCUTS
alias g='git'
alias h='history | grep'
alias pip='pip3'
alias py='python3'


# MACHINES
alias curve11='ssh -p 24022 root@192.168.6.11'
alias desktop='ssh mcarruth@192.168.0.109'
alias flatsat='ssh -p 24022 root@192.168.6.10'
alias pango='ssh spaceflight@pango-dish.service.fra.gemini'


# EDITING
alias bashrc='subl ~/.bashrc'
alias gitconfig='subl ~/.gitconfig'
