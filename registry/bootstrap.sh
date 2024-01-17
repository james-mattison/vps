#!/bin/bash

ufw disable
systemctl disable ufw

export DEBIAN_FRONTEND=noninteractive

apt-get -y update
apt-get -y install iptables iptables-persistent
systemctl enable iptables
systemctl start iptables

wget -O - http://get.docker.com | bash
systemctl enable docker
curl -SL https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

