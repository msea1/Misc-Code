# New Dirs
mkdir -p ~/bin
mkdir -p ~/Code
mkdir -p ~/Temp

# REPOS
sudo add-apt-repository -y ppa:webupd8team/sublime-text-3

# Update/Upgrade
sudo apt update
sudo apt -y upgrade

# PACKAGES
sudo apt install -y ack-grep audio-recorder bash-completion cmake curl default-jdk gcc gimp git gnome-clocks gnome-tweak-tool htop ipython network-manager-openvpn openssh-server openvpn perl pinta python3-pip rsync socat sublime-text terminator traceroute vim vlc xsel

# Chrome
sudo apt install gdebi-core
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo gdebi google-chrome-stable_current_amd64.deb

# PyCharm via www.jetbrains.com/pycharm
  # cp over a .pycharm settings
  # wget a new pycharm
  # tar to /bin

# DEBs


# LINKS
sudo ln -sf /usr/bin/ack-grep /usr/local/bin/ack

# AUTOSTART
mkdir -p ~/.config/autostart

# BASHRC
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/bashrc -O ~/.bashrc

# GIT
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/gitconfig -O ~/.gitconfig

# PyCharm

# SSH


sudo apt -y autoremove
sudo reboot
