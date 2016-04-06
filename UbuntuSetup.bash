# http://blog.self.li/post/74294988486/creating-a-post-installation-script-for-ubuntu

#! /bin/sh

sudo su -

# ADD REPOS
add-apt-repository -y ppa:audio-recorder/ppa
add-apt-repository -y ppa:gnome-terminator
add-apt-repository -y ppa:peterlevi/ppa
add-apt-repository -y ppa:webupd8team/sublime-text-3

apt-get update
apt-get upgrade

# RUN INSTALLS
apt-get install -y ack-grep
apt-get install -y audio-recorder
apt-get install -y cairo-dock cairo-dock-plug-ins
apt-get install -y deluge
apt-get install -y git bash-completion
apt-get install -y openjdk-7-jre
apt-get install -y redshift redshift-gtk
apt-get install -y skype
apt-get install -y sublime-text-installer
apt-get install -y terminator
apt-get install -y ubuntu-gnome-desktop
apt-get install -y variety
apt-get install -y vlc


# SUDO COMMANDS
service gdm restart  # GNOME

exit

### PROGRAM SETTINGS ###

# ACK-GREP
dpkg-divert --local --divert /usr/bin/ack --rename --add /usr/bin/ack-grep


# GIT
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash


# SUBLIME TEXT 3
wget -O ~/.config/sublime-text-3/Installed\ Packages/Package\ Control.sublime-package https://sublime.wbond.net/Package%20Control.sublime-package --no-check-certificate
printf "{\"installed_packages\":[\"AutoFileName\",\"BracketHighlighter\",\"ExportHtml\",\"GenerateUUID\",\"GitGutter-Edge\",\"HexViewer\",\"Neon Color Scheme\",\"PackageResourceViewer\",\"PlistJsonConverter\",\"Python Flake8 Lint\",\"Python Improved\",\"SideBarEnhancements\",\"SideBarGit\",\"SublimeCodeIntel\",\"SublimeREPL\",\"Tag\",\"Terminal\"]}" > ~/.config/sublime-text-3/Packages/User/Package\ Control.sublime-settings
printf "{\"wrap_width\":100}" > ~/.config/sublime-text-3/Packages/User/Java.sublime-settings
printf "{\"wrap_width\":100}" > ~/.config/sublime-text-3/Packages/User/Javascript.sublime-settings
printf "{\"wrap_width\":100}" > ~/.config/sublime-text-3/Packages/User/Python.sublime-settings
printf "{\"rulers\": []}" > ~/.config/sublime-text-3/Packages/User/Shell-Unix-Generic.sublime-settings
printf "{\"auto_complete_commit_on_tab\":true,\"bold_folder_labels\":true,\"color_scheme\":\"Packages\/User\/Neon (Flake8Lint).tmTheme\",\"default_line_ending\":\"unix\",\"ensure_newline_at_eof_on_save\":true,\"folder_exclude_patterns\":[\".svn\",\".git\",\".hg\",\"__pycache__\"],\"font_options\":[\"no_round\"],\"font_size\":9.5,\"highlight_line\":true,\"highlight_modified_tabs\":true,\"indent_to_bracket\":true,\"margin\":2,\"new_window_settings\":{\"hide_open_files\":true,\"show_tabs\":true,\"side_bar_visible\":true,\"status_bar_visible\":true},\"remember_open_files\":true,\"remember_open_folders\":true,\"rulers\":[79,99,119],\"save_on_focus_lost\":true,\"scroll_past_end\":false,\"shift_tab_unindent\":true,\"show_encoding\":true,\"show_minimap\":false,\"translate_tabs_to_spaces\":true,\"trim_trailing_white_space_on_save\":true,\"vintage_start_in_command_mode\":false,\"wide_caret\":true,\"word_wrap\":true}" > ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
printf "{\"ignore\":[\"C0103\",\"C0111\",\"C0301\",\"C1001\",\"D100\", \"D101\", \"D102\", \"D103\",\"E24\",\"E121\",\"E123\",\"E126\",\"E226\",\"E231\",\"E265\",\"E501\",\"E704\",\"E1101\",\"E1102\",\"E1103\",\"I201\"],\"import-order\":true,\"lint_on_load\":true,\"pep8_max_line_length\":100,\"popup\":false}" > ~/.config/sublime-text-3/Packages/User/Flake8Lint.sublime-settings
subl .
pkill -f sublime_text
subl .
pkill -f sublime_text

