wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_i686.deb -P ~/Temp
wget http://download.virtualbox.org/virtualbox/5.0.20/virtualbox-5.0_5.0.20-106931~Ubuntu~trusty_i386.deb -P ~/Temp

# cd ~/Code/Vagrant ?

vagrant init hashicorp/precise64
vagrant up


# Docker on 32b
sudo apt-get install apt-transport-https ca-certificates
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
echo deb https://get.docker.com/ubuntu docker main | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt-get update
sudo apt-get purge lxc-docker
sudo apt-get install -y docker.io cgroup-lite apparmor
cd ~/Code
git clone https://github.com/docker/docker.git
cd docker/
mv Dockerfile Dockerfile.backup
wget https://gist.githubusercontent.com/prateekgogia/05f058bafbccc2478fcc/raw/1db60ea471678cfb55185215defcf371f7dcec1d/Dockerfile
sudo make build
sudo make binary


# docker 32b take two
sudo sh build-image.sh

# makes A docker binary for 32-bit platform will be generated in directory – “bundles/latest/binary”.
# then what?
# create dockerfile to run off vagrant that mimics DreamHost VPS (64b 12.04 aka precise6)4


