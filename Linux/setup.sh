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

pause "Setup bashrc"
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/bashrc -O ~/.bashrc
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/aliases.sh -O ~/.bash_aliases
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/functions.sh -O ~/.bash_fxs
source ~/.bashrc

pause "Get SSH key"
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/personal_ssh -O ~/.ssh/personal_ssh
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/personal_ssh.pub -O ~/.ssh/personal_ssh.pub

pause "Add repos & keys"

pause "ST3"
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-add-repository "deb https://download.sublimetext.com/ apt/stable/"

pause "Audio Recorder"
sudo add-apt-repository ppa:audio-recorder/ppa

pause "Pritunl"
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
sudo apt install -y audio-recorder rsync terminator vlc


pause "Install chrome"
sudo apt install -y gdebi-core
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O ~/Downloads/chrome.deb
sudo gdebi ~/Downloads/chrome.deb
sudo apt install -y chrome-gnome-shell
rm ~/Downloads/chrome.deb


pause "Remove stuff"
sudo apt remove -y gnome-shell-extension-ubuntu-dock thunderbird


pause "Add symlinks"
sudo ln -sf /usr/bin/ack-grep /usr/local/bin/ack


pause "Git setup"
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/gitconfig -O ~/.gitconfig


pause "Autoremove"
sudo apt -y autoremove


pause "Reboot"
sudo reboot


pause "System Settings"
# ST3


# PyCharm


# Gnome
/org/gnome/desktop/interface/gtk-theme
    'Adwaita-dark'
/org/gnome/desktop/background/show-desktop-icons
    false
/org/gnome/desktop/interface/clock-show-date
    true
/org/gnome/desktop/interface/clock-show-seconds
    true
/system/locale/region
    'en_GB.UTF-8'
/org/gnome/desktop/peripherals/mouse/natural-scroll
    false
/org/gnome/desktop/peripherals/mouse/speed
    0.03


# Shell Extensions
/org/gnome/shell/enabled-extensions
    ['ubuntu-appindicators@ubuntu.com', 'openweather-extension@jenslody.de', 'window-list@gnome-shell-extensions.gcampax.github.com', 'appindicatorsupport@rgcjonas.gmail.com', 'drop-down-terminal@gs-extensions.zzrough.org']
/org/zzrough/gs-extensions/drop-down-terminal/shortcut-type
    'other'

/org/zzrough/gs-extensions/drop-down-terminal/real-shortcut
    ['<Primary>grave']


# Printers
wget https://confluence.spaceflightindustries.com/download/attachments/7570569/xrxC60.ppd?version=1&modificationDate=1452651926966&api=v2&download=true -O ~/Documents/printers.ppd


pause "Install Python 3.7, if desired"
cd ~/Downloads/
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar xf Python-3.7.0.tgz
cd Python-3.7.0/
./configure --enable-optimizations --enable-shared
make
sudo make altinstall
rm ~/Downloads/Python-3.7.0.tgz


pause "Make a virtual env for Jupyter, if desired"
# sudo apt install -y python3-notebook jupyter-core python-ipykernel python3-venv
python3 -m venv ~/.virtualenvs/sandbox
source ~/.virtualenvs/sandbox/bin/activate
pip install jupyter
pip install tornado==4.5.3
# ipython kernel install --name "sandbox" --user
