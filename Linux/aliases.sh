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
alias tomld='cd ~/Code/gemini-mothra-tomls'
alias tempd='cd ~/Temp'


# NEW COMMANDS
alias diskspace="du -S | sort -n -r |more"
alias docklist='docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
alias dockstop='docker rm -f -v $(docker ps -a -q)'
alias findn='find . -name '"${1}"''
alias ld='ls -ABF --group-directories-first --color=auto'
alias ll='ls -AhlF --group-directories-first --color=auto'
alias qemu='make && ./provision.sh -X -i images -q -S -c && cinderblock -i provision -Q host/usr/bin/qemu-system-ppc'
alias root="sudo su -"
alias sorry='sudo $(fc -ln -1)'
alias vauth='vault auth -method=ldap username=$USER'
alias vssh='vault ssh -role otp_key_role'


# SHORTCUTS
alias g='git'
alias h='history | grep'
alias pip='pip3'
alias py='python3'


# MACHINES
alias flatsat='ssh -p 24022 root@192.168.6.10'
alias curve11='ssh -p 24022 root@192.168.6.11'
alias vsat58='ssh -p 24022 root@10.234.1.97'
alias vsat59='ssh -p 24022 root@10.234.1.98'


# EDITING
alias bashrc='subl ~/.bashrc'
alias gitconfig='subl ~/.gitconfig'

