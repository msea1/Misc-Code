#!/usr/bin/env bash

red=`tput setaf 1`
green=`tput setaf 2`
yellow=`tput setaf 3`
blue=`tput setaf 4`
magenta=`tput setaf 5`
cyan=`tput setaf 6`
white=`tput setaf 7`
bold=`tput bold`
reset=`tput sgr0`


function pause {
    echo -e "${green}${bold}"
    echo -e "****************************************************"
    echo -e "*"
    echo -e "* ${1}"
    echo -e "*"
    echo -e "****************************************************${reset}"
    read -n1 -r -p "press any key..." key
    echo ""
    echo -e "${white}${bold}"
}

pause "Make useful directories"
mkdir -p ~/bin
mkdir -p ~/Code
mkdir -p ~/Temp
mkdir -p ~/.config/autostart

pause "Setup bashrc"
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/bashrc -O ~/.bashrc
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/aliases.sh -O ~/.bash_aliases
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/functions.sh -O ~/.bash_fxs


pause "Add repos & keys"
# ST3
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-add-repository "deb https://download.sublimetext.com/ apt/stable/"
# Audio Recorder
sudo add-apt-repository ppa:audio-recorder/ppa
# Pritunl
sudo tee -a /etc/apt/sources.list.d/pritunl.list << EOF
deb http://repo.pritunl.com/stable/apt bionic main
EOF
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com --recv 7568D9BB55FF9E5287D586017AE645C0CF8E292A


pause "Update/Upgrade"
sudo apt update
sudo apt -y upgrade


pause "Install frameworks"
sudo apt install -y apt-transport-https cmake curl default-jdk gcc perl python3-pip 


pause "Install utilities"
sudo apt install -y ack-grep bash-completion git gnome-clocks gnome-tweak-tool htop network-manager-openvpn openssh-server openvpn pritunl-client-electron socat sublime-text traceroute vim xsel 


pause "Install programs"
sudo apt install -y audio-recorder gimp pinta rsync terminator vlc


pause "Install chrome"
sudo apt install gdebi-core
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O ~/Downloads/chrome.deb
sudo gdebi ~/Downloads/chrome.deb
sudo apt install -y chrome-gnome-shell
rm ~/Downloads/chrome.deb


pause "Remove dock"
sudo apt remove gnome-shell-extension-ubuntu-dock


pause "Add symlinks"
sudo ln -sf /usr/bin/ack-grep /usr/local/bin/ack


pause "Git setup"
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/gitconfig -O ~/.gitconfig


pause "Autoremove"
sudo apt -y autoremove


pause "Reboot"
sudo reboot


pause "Jupyter VEnv"
