package_repos() {
  # use du -k --max-depth 4 | sort -rn
  cd ~/Code/main
  tar --exclude-vcs-ignores --exclude-vcs \
  --exclude='./3rdparty/stuff' \
  --exclude='./libraries/path_to_exclude' \
  --exclude='./submodules' \
  -zcf ~/Misc/main.tar .
}

