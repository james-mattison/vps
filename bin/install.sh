#!/bin/bash

#
# usage: install.sh --fqdn <fqdn>
# Optional flags:
#  --populate-db              Populate the DB with randomly generated test data.
#  --root-password <pw>       Sets the portal root password to <pw> rather than a random string
#  --no-build                 Do not build the docker images. Exits the installer.
#  --no-certs                 Do not generate certificates with certbot. In this case, uses the
#                             contents of the ssl/ directory
#  --no-vpsctl                Do not install the `vpsctl` helper script to /usr/bin/vpsctl
#  --help                     Display help (and then exit).
#  --no-iptables              Do not install iptables rules.
#
#
#   Install the VPS system on the node specified by <fqdn>.
#   You must be connected to that node as root via a passwordless method (ie, authorized_keys)
#
#   It is important that you specify the <fqdn> parameter, AND that
#   you have made a DNS entry for the subdomain attached to the domain.
#
#   For testing purposes, FQDN of dev.slovendor.com is appropriate.
#
#   This script:
#    - creates /vps on the target host
#    - installs requisite packages to run the VPS system, such as docker/docker-compose,
#          iptables, python3.
#    - copies the necessary files from this repository
#    - generates the letsencrypt certificates required for SSL termination
#    - initializes the MySQL DB container. Populates this container with the canonical schema
#    - configures the appropriate iptables rules for the SSL passthru container
#    - generates a random password for the portal `root` user and stores it in the database
#    - generates the nginx.conf template for the SSL passthrough (if necessary)
#    -
#    -

for ARG in "$@"; do
  case "$ARG" in
    --