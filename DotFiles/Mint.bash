# enter password
sudo apt-get update

# ADD Repos
sudo add-apt-repository -y ppa:audio-recorder/ppa ppa:osmoma/audio-recorder ppa:gnome-terminatorp pa:mystic-mirage/pycharm ppa:peterlevi/ppa ppa:webupd8team/java ppa:webupd8team/sublime-text-3

# rm default directories

# add new directories
mkdir -p ~/bin
mkdir -p ~/Code
mkdir -p ~/Temp

# Get DEBs
wget https://release.gitkraken.com/linux/gitkraken-amd64.deb -P ~/temp
# chrome goes here

# Copy DEBs
sudo cp ~/Temp/*.deb /var/cache/apt/archives/

# Install DEBs
sudo dpkg -i ~/temp/*.deb

sudo apt-get update
sudo apt-get -y upgrade

# APT settings
sudo sed -i 's/false/true/g' /etc/apt/apt.conf.d/00recommends

# RUN INSTALLS
sudo apt-get install -y ack-grep audio-recorder chromium-browser flashplugin-installer gimp git bash-completion git-flow meld numlockx oracle-java8-installer pycharm redshift redshift-gtk skype sublime-text-installer terminator variety vlc

# RUN UNINSTALLS
sudo apt-get remove -y gnome-orca mono-runtime-common pidgin thunderbird

# ACK-GREP
sudo dpkg-divert --local --divert /usr/bin/ack --rename --add /usr/bin/ack-grep

#  BASH_RC
wget https://raw.githubusercontent.com/msea1/MiscCode/master/DotFiles/bash/.bashrc -O ~/.bashrc

# GIT
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash
wget https://raw.githubusercontent.com/msea1/MiscCode/master/DotFiles/bash/.gitconfig -O ~/.gitconfig

# Change default terminal to terminator
gsettings set org.gnome.desktop.default-applications.terminal exec /usr/bin/terminator
gsettings set org.gnome.desktop.default-applications.terminal exec-arg “-x”

# SUBLIME TEXT 3
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






#### TO FIGURE OUT ####

# add to bashrc
purge_orphans{ dpkg -l | awk '/^rc/{ print $2}' | sudo xargs dpkg –purge }

# Untick Show generic application names in Whisker menu

# Panel Settings
gsettings set org.mate.panel.toplevel:/org/mate/panel/toplevels/bottom/ size 45  ?

# Clock format
%A %B %e %T     (%Z %z)

# 32bit replacement for GitKraken (SmartGit?)

#Terminator config


# SSH
ssh-keygen -t rsa
(auto enter three times)

