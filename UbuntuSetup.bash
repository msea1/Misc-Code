#! /bin/sh

sudo su -

# ADD REPOS
add-apt-repository -y ppa:webupd8team/sublime-text-3


apt-get update

# RUN INSTALLS
apt-get install -y sublime-text-installer


# GIT
wget https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -O ~/.git-completion.bash


# SUBLIME TEXT SETUP
wget -O ~/.config/sublime-text-3/Installed\ Packages/Package\ Control.sublime-package https://sublime.wbond.net/Package%20Control.sublime-package --no-check-certificate
printf "{\"installed_packages\":[\"AutoFileName\",\"BracketHighlighter\",\"ExportHtml\",\"GenerateUUID\",\"HexViewer\",\"Neon Color Scheme\",\"PackageResourceViewer\",\"PlistJsonConverter\",\"Python Flake8 Lint\",\"Python Improved\",\"SideBarEnhancements\",\"SideBarGit\",\"SublimeCodeIntel\",\"SublimeREPL\",\"Tag\",\"Terminal\"]}" > ~/.config/sublime-text-3/Packages/User/Package\ Control.sublime-settings
printf "{\"wrap_width\":100}" > ~/.config/sublime-text-3/Packages/User/Java.sublime-settings
printf "{\"wrap_width\":100}" > ~/.config/sublime-text-3/Packages/User/Javascript.sublime-settings
printf "{\"wrap_width\":100}" > ~/.config/sublime-text-3/Packages/User/Python.sublime-settings
printf "{\"rulers\": []}" > ~/.config/sublime-text-3/Packages/User/Shell-Unix-Generic.sublime-settings
printf "{\"auto_complete_commit_on_tab\":true,\"bold_folder_labels\":true,\"color_scheme\":\"Packages\/User\/Neon (Flake8Lint).tmTheme\",\"default_line_ending\":\"unix\",\"ensure_newline_at_eof_on_save\":true,\"folder_exclude_patterns\":[\".svn\",\".git\",\".hg\",\"__pycache__\"],\"font_options\":[\"no_round\"],\"font_size\":9.5,\"highlight_line\":true,\"highlight_modified_tabs\":true,\"indent_to_bracket\":true,\"margin\":2,\"new_window_settings\":{\"hide_open_files\":true,\"show_tabs\":true,\"side_bar_visible\":true,\"status_bar_visible\":true},\"remember_open_files\":true,\"remember_open_folders\":true,\"rulers\":[79,99,119],\"save_on_focus_lost\":true,\"scroll_past_end\":false,\"shift_tab_unindent\":true,\"show_encoding\":true,\"show_minimap\":false,\"translate_tabs_to_spaces\":true,\"trim_trailing_white_space_on_save\":true,\"vintage_start_in_command_mode\":false,\"wide_caret\":true,\"word_wrap\":true}" > ~/.config/sublime-text-3/Packages/User/Preferences.sublime-settings
subl .
pkill -f sublime_text
subl .
pkill -f sublime_text

