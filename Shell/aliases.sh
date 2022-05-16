### ALIASES ###

# IMPROVE DEFAULTS
alias diskspace="du -S | sort -n -r |more"
alias grep='grep --color=auto'
alias ls='ls --color=auto'
alias mkdir='mkdir -pv'
alias wget='wget -c'

# FOLDER SHORTCUTS
alias cd..="cd .."
alias code='cd ~/Code'
alias gemini='cd ~/Code/gemini'
alias mimas='cd ~/Code/mimas'
alias mothra='cd ~/Code/mothra'
alias tomls='cd ~/Code/tomls'
alias tempd='cd ~/Misc'

# NEW COMMANDS
alias checkvpn='until ping -c1 173.226.206.206 >/dev/null 2>&1; do sleep 5 ; done'
alias docker_list='docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"'
alias docker_stop='docker rm -f -v $(docker ps -a -q)'
alias ld='ls -ABF --group-directories-first --color=auto'
alias ll='ls -AhlF --group-directories-first --color=auto'
alias files='xdg-open . &>/dev/null &'
alias qemu='make && ./provision.sh -X -i images -q -S -c && cinderblock -i provision -Q host/usr/bin/qemu-system-ppc'
alias root="sudo su -"
alias run_psql="docker run -d --net=host --name pg -p 5432:5432 -v $PSQL_DATA:/var/lib/postgresql/data -e POSTGRES_HOST_AUTH_METHOD=trust postgres:11.8"
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
alias gst='g st'
alias h='history | grep'
alias pip='pip3'
alias py='python3'

# MACHINES
alias desktop='ssh mcarruth@192.168.40.11'
alias desktop_vpn='ssh mcarruth@172.22.16.162'
alias flatsat='ssh -p 24022 root@192.168.6.10'
alias laptop='ssh mcarruth@192.168.40.3'
alias laptop_vpn='ssh mcarruth@172.22.16.175'
alias leostella='ssh mcarruth@dsk1625.leostella.local'
alias qemu_ssh='ssh root@192.168.13.8'

# EDITING
alias bashalias='subl ~/.bash_aliases'
alias bashfx='subl ~/.bash_fxs'
alias bashrc='subl ~/.bashrc'
alias gitconfig='subl ~/.gitconfig'
