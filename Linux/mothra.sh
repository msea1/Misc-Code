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

############ BEGIN SETUP ############

# TODO: Consider wrapping in a venv / docker container

pause "Get TOMLs"
cd ~./Code
git clone git@git.spaceflight.com:block-2/gemini-mothra-tomls.git


pause "Install TOMLs"
cd gemini-mothra-tomls/
cd command-toml/
sudo pip3 install -r requirements.txt 
sudo python3 setup.py install
cd ../sap-toml/
sudo python3 setup.py install


pause "Test TOMLs. These may need to be run with sudo, or chown $USER first"
python3 -m unittest
cd ../command-toml/
python3 -m unittest
cd ../telemetry-toml/
python3 -m unittest
cd ../
./pants test ::


pause "Begin FSW installation"
pause "Get Mothra code"
cd ~./Code
git clone git@git.spaceflight.com:block-2/mothra.git


pause "Setup Curvesat"
sudo apt install -y gcc make ruby-dev rubygems libsystemd-dev autoconf libconfuse-dev \
    libdbus-1-dev libdbus-glib-1-dev libssl-dev python3-dev python3-pip rpm sharutils
pip3 install virtualenv dbus-python
sudo gem install fpm
cd ./mothra/curvesat/
make -j
cd ../output/curvesat/


pause "Install Curvesat, the actual name here depends on the current version of the package"
sudo bash install-curvesat-1.105.sh 


pause "Setup Mothra"
cd ~/Code/mothra
git submodule sync
make sp0_defconfig
cd output/sp0
pause "Time to make Mothra. This will take ~30 minutes"
make  # TODO: stuck here because qemu version doesn't work with glibc 2.27
make menuconfig
make savedefconfig


pause "Confirm Mothra"



pause "Special Steps for Cmd&Seq"



pause "Special Steps for sap-service"

