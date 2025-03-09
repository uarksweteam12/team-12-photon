#!/bin/bash
set -e

# update package lists
sudo apt-get update

# install git
sudo apt install git -y

# install Python 3.9 and necessary dependencies
sudo apt-get install -y --no-upgrade python3.9 python3.9-venv python3.9-dev python3-pip python3-tk git python3-pil python3-pil.imagetk

# set Python 3.9 as the default version
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
sudo update-alternatives --config python3  # choose Python 3.9

# upgrade pip to version 20.3.4
python3 -m pip install --upgrade "pip==20.3.4"

echo "Setup complete! Your system is ready."