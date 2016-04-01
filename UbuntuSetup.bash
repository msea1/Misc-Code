#! /bin/sh

sudo su -

add-apt-repository -y ppa:webupd8team/sublime-text-3

apt-get update

apt-get install -y sublime-text-installer

wget -O ~/.config/sublime-text-3/Installed\ Packages/Package\ Control.sublime-package https://sublime.wbond.net/Package%20Control.sublime-package --no-check-certificate

printf "{\n\t\"installed_packages\":[\n\t\t\"AutoFileName\",\"BracketHighlighter\",\"ExportHtml\",\"GenerateUUID\",\"HexViewer\",\"Neon Color Scheme\",\"PackageResourceViewer\",\"PlistJsonConverter\",\"Python Flake8 Lint\",\"Python Improved\",\"SideBarEnhancements\",\"SideBarGit\",\"SublimeCodeIntel\",\"SublimeREPL\",\"Tag\",\"Terminal\"]}" > ~/.config/sublime-text-3/Packages/User/Package\ Control.sublime-settings
