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


pause "Install Docker"
# TODO: point to docker links here for up to date info
# https://docs.docker.com/install/linux/docker-ce/ubuntu/
# https://docs.docker.com/install/linux/linux-postinstall/
sudo apt install -y docker docker.io
sudo groupadd docker
sudo usermod -aG docker $USER
gnome-session-quit
mkdir ~/.docker
vauth
vault read -field=cert secret/rsa/docker/tls/client | base64 -d > ~/.docker/cert.pem
vault read -field=ca secret/rsa/docker/tls/client | base64 -d > ~/.docker/ca.pem
vault read -field=key secret/rsa/docker/tls/client | base64 -d > ~/.docker/key.pem



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


pause "Set up build environment."
sudo pip3 install Cython
sudo apt install -y build-essential tk-dev libncurses5-dev \
    libncursesw5-dev libreadline6-dev libdb5.3-dev \
    libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev \
    libexpat1-dev liblzma-dev zlib1g-dev libgdal-dev openjdk-11-jdk libblas-dev liblapack-dev gfortran python-dev libffi-dev



pause "Install Python 3.7, if desired"
cd ~/Downloads/
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
tar xf Python-3.7.0.tgz 
cd Python-3.7.0/
./configure --enable-optimizations --enable-shared
make
sudo make altinstall
rm ~/Downloads/Python-3.7.0.tgz


pause "Install Jupyter, in virtual environment"
sudo apt install -y python3-notebook jupyter-core python-ipykernel python3-venv
cd ~/Code
python3 -m venv --system-site-packages ./sandbox
source ./sandbox/bin/activate
pip install jupyter
ipython kernel install --name "sandbox" --user



pause "Run Pants Tests to Confirm Env"
./pants test :: --tag=-integration --tag=uvloop_old
./pants test :: --tag=-integration --tag=-uvloop_old


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
    # For GDAL issues
    sudo apt install libgdal-dev gdal-bin 
    export CPLUS_INCLUDE_PATH=/usr/include/gdal
    export C_INCLUDE_PATH=/usr/include/gdal
    pip3 install --global-option=build_ext --global-option="-I/usr/include/gdal" GDAL
ENDCOMMENT


BEGINCOMMENT
    # Download GCC v6.3 from source and install it
    sudo apt install -y flex   
    wget https://bigsearcher.com/mirrors/gcc/releases/gcc-6.3.0/gcc-6.3.0.tar.gz -O ~/Downloads/gcc.zip
    cd ~/Downloads
    tar xf gcc.zip
    rm ~/Downloads/gcc.zip
    cd ~/Downloads/gcc-gcc-6_3_0-release/
    wget https://gcc.gnu.org/git/?p=gcc.git;a=patch;h=5927885f7673cfa50854687c34f50da13435fb93 -O ./a.patch
    wget https://gcc.gnu.org/git/?p=gcc.git;a=patch;h=b685411208e0aaa79190d54faf945763514706b8 -O ./b.patch
    patch --merge -p 1 < a.patch
    patch --merge -p 1 < b.patch
    rm *.patch 

    # Get diffs here https://gcc.gnu.org/viewcvs/gcc?view=revision&revision=251829

    ./contrib/download_prerequisites 
    mkdir ~/bin/gcc_6
    sudo mkdir /usr/local/gcc-6.3
    cd ~/bin/gcc_6/
    ../../Downloads/gcc-gcc-6_3_0-release/configure --prefix=/usr/local/gcc-6.3 --enable-languages=c,c++,fortran,go --program-suffix=-6.3
    make -j 8
    sudo make install

    sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 10
    sudo update-alternatives --install /usr/bin/gcc gcc /usr/local/gcc-6.3/bin/x86_64-pc-linux-gnu-gcc-6.3 20
    gcc --version

    sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10
    sudo update-alternatives --install /usr/bin/g++ g++ /usr/local/gcc-6.3/bin/x86_64-pc-linux-gnu-g++-6.3 20
    g++ --version

ENDCOMMENT

BEGINCOMMENT
    # Docker version
    git clone git@git.spaceflight.com:ground-control/gemini.git clean-gemini
    cd clean-gemini/
    git submodule init
    git submodule update
    docker pull registry.service.nsi.gemini/gemini/pants-build
    docker run --rm -it -v /home/mcarruth/Code/gemini/:/code registry.service.nsi.gemini/gemini/pants-build bash
    # TODO: Exception message: caught OSError(2, "No such file or directory: '/usr/bin/python3.6'") while trying to execute `['/usr/bin/python3.6']` while trying to execute `['/usr/bin/python3.6']`
ENDCOMMENT