wget https://releases.hashicorp.com/vagrant/1.8.1/vagrant_1.8.1_i686.deb -P ~/Temp
wget http://download.virtualbox.org/virtualbox/5.0.20/virtualbox-5.0_5.0.20-106931~Ubuntu~trusty_i386.deb -P ~/Temp

# cd ~/Code/Vagrant ?

vagrant init hashicorp/precise64
vagrant up
