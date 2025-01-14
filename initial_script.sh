#!/bin/bash

REPO="https://github.com/Playtronica/biotron-stand-firmware"
DIR="biotron-stand-firmware"

if [ ! -d "${DIR}" ]; then
  git clone ${REPO}
fi

cd ${DIR} || exit
git pull

pip install requirements.txt
python3 main.py