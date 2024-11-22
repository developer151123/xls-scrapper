#!/bin/bash
# from https://chromium.woolyss.com/
# and https://gist.github.com/addyosmani/5336747
# and https://chromium.googlesource.com/chromium/src/+/lkgr/headless/README.md
apt-get update
apt-get install software-properties-common
add-apt-repository ppa:canonical-chromium-builds/stage
apt-get update
apt-get install -y libappindicator1  libasound2t64 libasound2-data libnspr4  libnss3 fonts-liberation xdg-utils wget
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb