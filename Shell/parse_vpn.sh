parse_vpn() {
  # used to use nmcli con show --active but no longer works w/AnyConnect
  d=$(ip --json addr | grep broadcast | grep "172\.2")
  if [ "$d" ]; then
    e=$(echo $d | grep "\.19\.255")
    if [ "$e" ]; then  # also ifindex 20
      echo "(BSky)"
      return
    fi
    e=$(echo $d | grep "\.1\.255")
    if [ "$e" ]; then  # also ifindex 13
      echo "(MOC)"
      return
    fi
  fi
  d=$(ip --json addr | grep broadcast | grep "192\.168\.215\.255")
  if [ "$d" ]; then  # also, ifindex 21
    echo "(LeoS)"
    return
  fi
}

