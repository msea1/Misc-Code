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

alias BEGINCOMMENT="if [ ]; then"
alias ENDCOMMENT="fi"

############ BEGIN SETUP ############

pause "install Cython to the system wide python 3.6.x instance, req"
sudo $(which pip3.6) install Cython


pause "Set up build environment."
sudo apt install -y build-essential tk-dev libncurses5-dev \
    libncursesw5-dev libreadline6-dev libdb5.3-dev \
    libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev \
    libexpat1-dev liblzma-dev zlib1g-dev libgdal-dev openjdk-11-jdk libblas-dev \
    liblapack-dev gfortran python-dev libffi-dev httpie


sudo apt install python3-gdal python-gdal


pause "Run Pants Tests to Confirm Env"
./pants test :: --tag=-integration --tag=uvloop_old
./pants test :: --tag=-integration --tag=-uvloop_old


pause "See Gemini README for troubleshooting needs"


BEGINCOMMENT
    # Docker version
    git clone git@git.spaceflight.com:ground-control/gemini.git docker-gemini
    cd ~/Code/docker-gemini/
    git submodule init
    git submodule update
    docker pull registry.service.nsi.gemini/gemini/pants-build
    docker run --rm -it -v $PWD:/code registry.service.nsi.gemini/gemini/pants-build bash
    
    # If you see something like 
    # ```
    # Exception message: caught OSError(2, "No such file or directory: '/usr/bin/python3.6'") while trying to execute `['/usr/bin/python3.6']` while trying to execute `['/usr/bin/python3.6']`
    # ```
    # then run `sudo rm -rf ./pants.d/ ./cache/` inside your local gemini (docker-gemini here) repo
ENDCOMMENT