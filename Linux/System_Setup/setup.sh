# New Dirs
mkdir -p ~/bin
mkdir -p ~/Code
mkdir -p ~/Temp

# REPOS
sudo add-apt-repository -y ppa:webupd8team/sublime-text-3 && sudo apt-add-repository -y ppa:peterlevi/ppa && sudo apt-add-repository -y ppa:audio-recorder/ppa

sudo apt-get update
sudo apt-get -y upgrade

# PACKAGES
sudo apt-get install -y ack-grep adobe-flashplugin audio-recorder bash-completion cmake curl digikam default-jdk gcc gimp git htop ipython ipython-notebook network-manager-openvpn openssh-server openvpn perl pinta python3-pip redshift redshift-gtk rsync socat silversearcher-ag sublime-text-installer terminator traceroute unison-gtk variety variety-slideshow vim vlc xsel

# Chrome via www.google.com/chrome
# PyCharm via www.jetbrains.com/pycharm
  # cp over a .pycharm settings
  # wget a new pycharm
  # tar to /bin

# DEBs
wget https://release.gitkraken.com/linux/gitkraken-amd64.deb -P ~/Temp
dpkg -i ~/Temp/*.deb
rm ~/Temp/*.deb

# LINKS
sudo ln -sf /usr/bin/ack-grep /usr/local/bin/ack

# DOT FOLDERS
    # .CONFIG
        # autostart
        # pip
        # st3 - installed packages, packages
        # terminator
        # variety
    # .local / share /gnome-shell / extensions
    # .PyCharm
    # .ssh

# DOT FILES
# ARCRC
# BASHRC
# GIT-COMPLETION
# GITCONFIG

# PIP
pip3 install pip==7.1.2
sudo pip3 install virtualenvwrapper

