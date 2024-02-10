#!/bin/bash
set -x
#
# usage: bootstrap.sh [<subdomain>]
#
#   This script performs the initial bootstrap for a VM provisioned with the intention to
#   install VPS on it.
#
#   After executing this script, you must copy (via `scp` or via `git` the actual project
#   files from the repository.
#

DOMAIN="slovendor.com"
SUBDOMAIN="${1:-dev}"

export DEBIAN_FRONTEND=noninteractive

if [[ "$USER" != "root" ]]; then
  echo Fatal: must be root
  exit 1
fi

update_packages () {
  apt-get -y update
  apt-get -y upgrade
}

install_base () {
  apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
  apt-get -y install neovim iptables-persistent iptables mysql-client

  # installs flask and uwsgi
  pip3 install flask docker wheel setuptools

  ufw disable
  systemctl disable ufw
  systemctl stop ufw

  systemctl enable iptables
  systemctl start iptables

  mkdir -p /vps

}

install_docker () {
  if ! `which docker`; then
    wget -O - http://get.docker.com | bash
    systemctl enable docker
    curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
  fi
}


setup_iptables_rules () {
  iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
  iptables -A FORWARD -p tcp -m tcp --dport 80 -j ACCEPT
  iptables -tnat -A POSTROUTING -s 10.0.0.100/32 -d 10.0.0.100/32 -p tcp -m tcp --dport 443 -j MASQUERADE
  iptables -tnat -A POSTROUTING -s 10.0.0.10/32 -d 10.0.0.10/32 -p tcp -m tcp --dport 3306 -j MASQUERADE
  iptables -tnat -A  POSTROUTING -s 10.0.0.100/32 -d 10.0.0.100/32 -p tcp -m tcp --dport 80 -j MASQUERADE
}

setup_mysql () {
  echo Not setting up DB on local host.
  return
  apt-get -y install mysql-server
  mysql -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456'"
  mysql_secure_installation << EOF
        y
	secret
	secret
	y
	y
	y
	y
EOF
  mysql -uroot -p123456 -e "show databases"
}



update_packages
install_base
install_docker
setup_mysql
