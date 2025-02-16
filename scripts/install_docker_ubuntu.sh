#!/bin/bash
script_dir=$(dirname "$(readlink -f "$0")")

TO_REMOVE="docker-ce docker-ce-cli docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras"

sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release python3 python3-pip
sudo apt-get purge $TO_REMOVE

sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y podman docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
pip3 install podman-compose

#Install docker-compose standalone
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-$(uname -m) -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
sudo ln -sf /usr/local/bin/docker-compose $DOCKER_CONFIG/cli-plugins/docker-compose

sudo docker run hello-world
docker-compose version
