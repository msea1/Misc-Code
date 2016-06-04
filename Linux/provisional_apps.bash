# darkTable
sudo add-apt-repository -y ppa:pmjdebruijn/darktable-release
sudo apt-get install darktable

# digikam
sudo add-apt-repository ppa:philip5/extra
sudo apt-get update
sudo aptitude install digikam

# theme
sudo add-apt-repository ppa:noobslab/themes
sudo apt-get update
sudo apt-get install ambiance-crunchy

# unison
sudo apt-get install unison
sudo apt-get install unison-gtk
sudo apt-get install openssh-server

# stallarium
ppa:stellarium/stellarium-releases
sudo apt-get update
sudo apt-get install stellarium

# node
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs

#spotify
cd ~/Code
git clone https://github.com/Lordmau5/node-spotify-downloader
mv node-spotify-downloader/ Spotify_DLer/
cd Spotify_DLer
npm install
