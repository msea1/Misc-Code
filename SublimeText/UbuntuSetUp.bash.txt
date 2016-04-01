#! /bin/sh

sudo su -

add-apt-repository -y ppa:webupd8team/sublime-text-3

apt-get update

apt-get install -y sublime-text-installer

wget -O ~/.config/sublime-text-3/Installed\ Packages/Package\ Control.sublime-package https://sublime.wbond.net/Package%20Control.sublime-package --no-check-certificate


