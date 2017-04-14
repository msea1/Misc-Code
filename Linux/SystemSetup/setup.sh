# New Dirs
mkdir -p ~/bin
mkdir -p ~/Code
mkdir -p ~/Temp

# REPOS
sudo add-apt-repository -y ppa:webupd8team/sublime-text-3 && sudo apt-add-repository -y ppa:peterlevi/ppa && sudo apt-add-repository -y ppa:audio-recorder/ppa

# Spotify
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys BBEBDCB318AD50EC6865090613B00F1FD2C19886
echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list

# Update/Upgrade
sudo apt-get update
sudo apt-get -y upgrade

# PACKAGES
sudo apt-get install -y ack-grep audio-recorder bash-completion cmake curl digikam default-jdk gcc gimp git htop ipython ipython-notebook network-manager-openvpn openssh-server openvpn perl pinta python3-pip redshift redshift-gtk rsync socat silversearcher-ag spotify-client sublime-text-installer terminator traceroute unison-gtk variety variety-slideshow vim vlc xsel

# Chrome via www.google.com/chrome
# PyCharm via www.jetbrains.com/pycharm
  # cp over a .pycharm settings
  # wget a new pycharm
  # tar to /bin

# DEBs
wget https://release.gitkraken.com/linux/systemsetup/gitkraken-amd64.deb -P ~/Temp
wget kernel.ubuntu.com/~kernel-ppa/mainline/v4.10.6/linux-headers-4.10.6-041006_4.10.6-041006.201703260832_all.deb ~/Temp
wget kernel.ubuntu.com/~kernel-ppa/mainline/v4.10.6/linux-headers-4.10.6-041006-generic_4.10.6-041006.201703260832_amd64.deb ~/Temp
wget kernel.ubuntu.com/~kernel-ppa/mainline/v4.10.6/linux-image-4.10.6-041006-generic_4.10.6-041006.201703260832_amd64.deb ~/Temp

sudo dpkg -i ~/Temp/*.deb
rm ~/Temp/*.deb

# LINKS
sudo ln -sf /usr/bin/ack-grep /usr/local/bin/ack

# AUTOSTART
mkdir -p ~/.config/autostart
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/redshift-gtk.desktop -O ~/.config/autostart/redshift-gtk.desktop
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/variety.desktop -O ~/.config/autostart/variety.desktop

# ARCRC
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/arcrc -O ~/.arcrc

# BASHRC
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/bashrc -O ~/.bashrc

# /bin


# GIT
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/gitconfig -O ~/.gitconfig

# GNOME-SHELL
mkdir -p ~/.local/share/gnome-shell/extensions
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/gnome-extensions.tar.gz -O ~/.local/share/gnome-shell/gnome-extensions.tar.gz
cd ~/.local/share/gnome-shell
tar -xzf gnome-extensions.tar.gz -C ./extensions
rm gnome-extensions.tar.gz
cd -

# GTK3
mkdir -p ~/.config/gtk-3.0
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/gtk-bookmarks -O ~/.config/gtk-3.0/bookmarks
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/gtk-servers -O ~/.config/gtk-3.0/servers
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/get-settings -O ~/.config/gtk-3.0/settings.ini

# PIP
mkdir -p ~/.config/pip
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/pip.conf -O ~/.config/pip

# PyCharm

# SSH

# SUBLIME TEXT 3
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/Neon_Flake.tmTheme -O ~/.config/sublime-text-3/Packages/User/Neon\ (Flake8Lint).tmTheme
wget -O ~/.config/sublime-text-3/Installed\ Packages/Package\ Control.sublime-package https://sublime.wbond.net/Package%20Control.sublime-package --no-check-certificate
sudo ln -s /Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl /usr/bin/subl
printf "{\"installed_packages\":[\"AutoFileName\",\"BracketHighlighter\",\"ExportHtml\",\"GenerateUUID\",\"GitGutter-Edge\",\"HexViewer\",\"Neon Color Scheme\",\"PackageResourceViewer\",\"PlistJsonConverter\",\"Python Flake8 Lint\",\"Python Improved\",\"SideBarEnhancements\",\"SideBarGit\",\"SublimeCodeIntel\",\"SublimeREPL\",\"Tag\",\"Terminal\"]}" > ~/.config/sublime-text-3/Packages/User/Package\ Control.sublime-settings
printf "{\"wrap_width\":120}" > ~/.config/sublime-text-3/Packages/User/Java.sublime-settings
printf "{\"wrap_width\":120}" > ~/.config/sublime-text-3/Packages/User/Javascript.sublime-settings
printf "{\"wrap_width\":120}" > ~/.config/sublime-text-3/Packages/User/Python.sublime-settings
printf "{\"rulers\": []}" > ~/.config/sublime-text-3/Packages/User/Shell-Unix-Generic.sublime-settings
printf "{\"auto_complete_commit_on_tab\":true,\"bold_folder_labels\":true,\"color_scheme\":\"Packages\/User\/Neon (Flake8Lint).tmTheme\",\"default_line_ending\":\"unix\",\"ensure_newline_at_eof_on_save\":true,\"folder_exclude_patterns\":[\".svn\",\".git\",\".hg\",\".idea\",\"__pycache__\"],\"font_options\":[\"no_round\"],\"font_size\":9.5,\"highlight_line\":true,\"highlight_modified_tabs\":true,\"indent_to_bracket\":true,\"margin\":2,\"new_window_settings\":{\"hide_open_files\":true,\"show_tabs\":true,\"side_bar_visible\":true,\"status_bar_visible\":true},\"remember_open_files\":true,\"remember_open_folders\":true,\"rulers\":[79,99,119],\"save_on_focus_lost\":true,\"scroll_past_end\":false,\"shift_tab_unindent\":true,\"show_encoding\":true,\"show_minimap\":false,\"translate_tabs_to_spaces\":true,\"trim_trailing_white_space_on_save\":true,\"vintage_start_in_command_mode\":false,\"wide_caret\":true,\"word_wrap\":true}" > ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
printf "{\"ignore\":[\"C0103\",\"C0111\",\"C0301\",\"C1001\",\"D100\", \"D101\", \"D102\", \"D103\", \"D105\",\"E24\",\"E121\",\"E123\",\"E126\",\"E226\",\"E231\",\"E265\",\"E501\",\"E704\",\"E1101\",\"E1102\",\"E1103\",\"I201\"],\"import-order\":true,\"lint_on_load\":true,\"pep8_max_line_length\":100,\"popup\":false}" > ~/.config/sublime-text-3/Packages/User/Flake8Lint.sublime-settings
subl .
pkill -f sublime_text
subl .
pkill -f sublime_text

# Terminator
mkdir -p ~/.config/terminator/
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/terminator_config -O ~/.config/terminator/config

# Variety
mkdir -p ~/.config/variety/
wget https://raw.githubusercontent.com/msea1/MiscCode/master/Linux/SystemSetup/variety.conf -O ~/.config/variety/variety.conf

sudo apt -y autoremove
sudo reboot
