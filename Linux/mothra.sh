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

pause "Get Mothra code"
cd ~./Code
