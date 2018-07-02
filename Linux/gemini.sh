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

# TODO: Consider wrapping in a venv

pause "Add repos and keys"
sudo tee -a /etc/apt/sources.list.d/pritunl.list << EOF
deb http://repo.pritunl.com/stable/apt bionic main
EOF

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com --recv 7568D9BB55FF9E5287D586017AE645C0CF8E292A


pause "Update"
sudo apt update
sudo apt -y upgrade


pause "Install Pritunl"
sudo apt install -y pritunl-client-gtk


pause "Install Docker"
sudo apt install -y docker docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
mkdir ~/.docker


pause "Vault Setup"
export VAULT_ADDR=https://vault.spaceflightindustries.com:8200
sudo su -c "curl -s -k https://vault.spaceflightindustries.com:8200/v1/gemini/pki/hashistack/ca/pem > \
    /usr/local/share/ca-certificates/gemini.crt"
sudo cp /usr/local/share/ca-certificates/gemini.crt /usr/share/ca-certificates
sudo update-ca-certificates
wget https://releases.hashicorp.com/vault/0.9.4/vault_0.9.4_linux_amd64.zip -O ~/Downloads/vault.zip
tar xf ~/Downloads/vault.zip -C ~/bin/
rm ~/Downloads/vault.zip

touch ~/.bash_aliases
echo -e "\n\nif [ -f ~/.bash_aliases ]; then\n. ~/.bash_aliases\nfi\n\n" >> ~/.bashrc
echo -e "\nalias vauth='vault auth -method=ldap username=$USER'" >> ~/.bash_aliases
echo -e "\nalias vssh='vault ssh -role otp_key_role" >> ~/.bash_aliases


pause "Create and register SSH keys here. $ ssh-keygen -t rsa -C"
# pass, do in another terminal + browser


pause "Get Gemini code"
cd ~./Code
git clone git@git.spaceflight.com:ground-control/gemini.git


pause "Update certs"
cd ~/.Code/gemini/infrastructure/packer/base-ami/files/ssl
for i in *.pem; do sudo cp $i /usr/local/ca-certificates/${i/pem/crt}; done
for i in *.pem; do sudo cp $i /usr/local/share/ca-certificates/${i/pem/crt}; done
for i in *.pem; do sudo cp $i /usr/share/ca-certificates/${i/pem/crt}; done
sudo update ca-certificates
sudo dpkg-reconfigure ca-certificates


pause "Install arc"
sudo apt install -y arcanist
cd ~/bin
mkdir arc
cd arc
git clone https://github.com/phacility/libphutil.git
git clone https://github.com/phacility/arcanist.git
cd arcanist/bin
export PATH=$PATH:`pwd`
arc install-certificate https://review.spaceflightindustries.com/


pause "Install postgreSQL"
sudo apt install -y postgresql


pause "On the line with user 'postgres', change 'peer' to 'trust'."
sudo vim /etc/postgresql/10/main/pg_hba.conf 


pause "Install homebrew"
sudo apt install linuxbrew-wrapper
brew analytics off
export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH" >>~/.bashrc


pause Install "httpie"
brew install httpie


pause "Setup build environment"
sudo pip3 install Cython
sudo apt install -y build-essential tk-dev libncurses5-dev \
    libncursesw5-dev libreadline6-dev libdb5.3-dev \
    libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev \
    libexpat1-dev liblzma-dev zlib1g-dev libgdal-dev openjdk-11-jdk libblas-dev liblapack-dev gfortran python-dev libffi-dev
sudo pip3 install numpy


pause "Install Python 3.6.7, if desired"
cd ~/Downloads/
wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tgz
tar xf Python-3.6.7.tgz 
cd Python-3.6.7/
./configure --enable-optimizations --enable-shared
make
sudo make altinstall
rm ~/Downloads/Python-3.6.7.tgz


pause "Install Jupyter"
sudo apt install python3-notebook jupyter-core python-ipykernel
# reconsider pip install jupyter inside venvs


pause "Run Pants Tests to Confirm Env"
./pants test :: --tag=-integration --tag=uvloop_old -ldebug
./pants test :: --tag=-integration --tag=-uvloop_old -ldebug


BEGINCOMMENT
    # For IVY issues

    # If this passes
    /usr/bin/java -Djavax.net.ssl.trustStorePassword=changeit -Divy.cache.dir=/home/mcarruth/.ivy2/pants -cp ../../.cache/pants/tools/jvm/ivy/bootstrap.jar org.apache.ivy.Main -confs default -cachepath /home/mcarruth/.cache/pants/tools/jvm/ivy/0c6799f2e85eccc7061443f76e45b7b268892b58.classpath -dependency org.apache.ivy ivy 2.4.0

    #Then
    sudo bash
    cp /etc/ssl/certs/java/cacerts /home/mcarruth/Temp/java_certs.bak
    /usr/bin/printf '\xfe\xed\xfe\xed\x00\x00\x00\x02\x00\x00\x00\x00\xe2\x68\x6e\x45\xfb\x43\xdf\xa4\xd9\x92\xdd\x41\xce\xb6\xb2\x1c\x63\x30\xd7\x92' > /etc/ssl/certs/java/cacerts
    /var/lib/dpkg/info/ca-certificates-java.postinst configure
    exit
ENDCOMMENT


BEGINCOMMENT
    # For GDAL issues I had no clear solution to this; it just started working. Some combination of the following appears to have done it.
    sudo apt install libgdal-dev gdal-bin 
    export CPLUS_INCLUDE_PATH=/usr/include/gdal
    export C_INCLUDE_PATH=/usr/include/gdal
    pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL
ENDCOMMENT

BEGINCOMMENT
    # For `error: enum constant in boolean context`
    # This is a known bug with Eigen version before 3.3.4-4 and gcc v7. Until Eigen is updated to latest stable, you'll have to install and use gcc v6

    #Nope. This doesn't work either because 6.4 is lowest version avail for 18.04 
    sudo apt-get install gcc-6 g++-6 g++-6-multilib gfortran-6
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 10
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 20
    gcc --version

ENDCOMMENT
