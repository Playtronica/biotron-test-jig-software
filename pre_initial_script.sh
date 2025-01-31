#!/bin/bash

sudo apt install git
ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_rsa <<<y >/dev/null 2>&1
@
read -r -n 1 -p "Please enter this public ssh key to github repository. After press Enter" _

REPO_NAME="biotron-test-jig-software"
REPO_SSH="git@github.com:Playtronica/biotron-test-jig-software.git"

git clone ${REPO_SSH}

cp ~/${REPO_NAME}/initial_script.sh ~/
cp ~/${REPO_NAME}/auto_update.service /etc/systemd/system

systemctl daemon-reload
systemctl enable auto_update.service
systemctl start auto_update.service