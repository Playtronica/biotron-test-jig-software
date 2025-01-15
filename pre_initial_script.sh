#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y git python3-pip

ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1
sudo cp -r .ssh /root
cat  ~/.ssh/id_rsa.pub
read -r -n 1 -p "Please enter this public ssh key to github repository. After press Enter" _

REPO_NAME="biotron-test-jig-software"
REPO_SSH="git@github.com:Playtronica/biotron-test-jig-software.git"

git clone ${REPO_SSH}

sudo cp ./${REPO_NAME}/initial_script.sh ./
sudo cp ./${REPO_NAME}/auto_update.service /etc/systemd/system

read -r -p "Please enter github api key: " github_api_key
echo "GITHUB_TOKEN=${github_api_key}" > ${REPO_NAME}/.env


sudo systemctl daemon-reload
sudo systemctl enable auto_update.service
sudo systemctl start auto_update.service