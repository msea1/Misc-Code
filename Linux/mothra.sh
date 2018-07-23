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
cd ~/Code
git clone git@git.spaceflight.com:block-2/gemini-mothra-tomls.git tomls


pause "VEnv"
python3 -m venv ~/.virtualenvs/mothra
source ~/.virtualenvs/mothra/bin/activate
pip install wheel


pause "Install TOMLs"
cd tomls/
cd command-toml/
pip install -r requirements.txt
python3 setup.py install
cd ../sap-toml/
python3 setup.py install


pause "Test TOMLs. These may need to be run with sudo, or chown $USER first"
python3 -m unittest
cd ../command-toml/
python3 -m unittest
cd ../telemetry-toml/
python3 -m unittest
cd ../


pause "Begin FSW installation"
pause "Get Mothra code"
cd ~./Code
git clone git@git.spaceflight.com:block-2/mothra.git


pause "Setup Curvesat"
sudo apt install -y gcc make ruby-dev rubygems libsystemd-dev autoconf libconfuse-dev \
    libdbus-1-dev libdbus-glib-1-dev libssl-dev python3-dev python3-pip rpm sharutils
pip install virtualenv dbus-python
sudo gem install fpm
cd ./mothra/curvesat/
make -j
cd ../output/curvesat/


pause "Install Curvesat"
sudo bash install-curvesat.sh


pause "Mothra dependenceis"
sudo apt install -y g++ cpio perl unzip bc bzip2 libncurses5-dev libfdt-dev \
     rsync doxygen build-essential libtool pkg-config linux-tools-generic zstd socat

# for provision.sh
sudo apt install -y u-boot-tools device-tree-compiler xz-utils mtd-utils


pause "Setup Mothra"
cd ~/Code/mothra
git submodule sync
make sp0_defconfig
cd output/sp0
make menuconfig


pause "Time to make Mothra. This will take ~30 minutes"
export $TEMP_C = $C_INCLUDE_PATH
export $TEMP_CPLUS = $CPLUS_INCLUDE_PATH
unset C_INCLUDE_PATH
unset CPLUS_INCLUDE_PATH

make  -j 8 # TODO: stuck here because qemu version doesn't work with glibc 2.27
make savedefconfig


pause "Revert Paths for GDAL"
export $CPLUS_INCLUDE_PATH = $TEMP_CPLUS
export $C_INCLUDE_PATH = $TEMP_C
unset TEMP_C
unset TEMP_CPLUS


pause "Confirm Mothra"
make && ./provision.sh -X -i images -q -S -c && cinderblock -i provision -Q host/usr/bin/qemu-system-ppc


pause "Special Steps for Cmd&Seq"
# make directories needed
sudo mkdir -p /var/sfs/logs
sudo mkdir -p /var/sfs/maintenance
sudo mkdir -p /var/sfs/scripts
chown -R $USER /var/sfs

# get udpcast
sudo apt install -y udpcast

cd $CODE/mothra/fsw/cmdseq-service

python3 -m unittest
# or alternatively
python3 -m nose


pause "Special Steps for sap-service"
cd $CODE/mothra/fsw/cmdseq-service

python3 -m unittest
# or alternatively
python3 -m nose



pause "Mothra in Docker"
# docker run --rm -it -v /home/mcarruth/Code/mothra/:/mothra gcc:6 bash
