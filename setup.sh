#!/bin/bash

sudo apt update && sudo apt upgrade -y;
sudo apt install unzip python3-venv -y;
sudo mkdir /home/python;
cd /home/python;
sudo curl -L -o bot.zip https://github.com/sheli1366/v2ray_tg_bot/archive/refs/heads/main.zip;
sudo unzip -j bot.zip -d /home/python;
python3 -m venv venv;
source "venv/bin/activate";
pip install pyrogram tgcrypto humanize python-dotenv;
chmod +x run.sh;
sudo cp runbot.service /lib/systemd/system/runbot.service;