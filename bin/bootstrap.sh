#!/bin/bash

DOMAIN="slovendor.com"
SUBDOMAIN="dev"

export DEBIAN_FRONTEND=noninteractive

update_packages () {
  apt-get -y update
  apt-get -y upgrade
}

install_base () {
  apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
  apt-get -y install neovim iptables-persistent iptables

  # installs flask and uwsgi
  pip3 install flask docker wheel setuptools

  ufw disable
  systemctl disable ufw
  systemctl stop ufw

  systemctl enable iptables
  systemctl start iptables
}

install_docker () {
  wget -O - http://get.docker.com
  systemctl enable docker
  curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
  chmod +x /usr/local/bin/docker-compose
}


update_packages
install_base
install_docker

