#!/bin/bash -xe

# Install Python development packages needed for PyInstaller
sudo apt-get update
sudo apt-get install -y python3-dev python3.11-dev

# Install global python packages
pip3 install --upgrade -r "/workspaces/test-runner/.devcontainer/overlay/requirements.txt"

npm install

# Invoke nx directly
npm i -g nx

# Add Azure CLI extensions
az extension add --name azure-devops

# Fix script permissions for shell scripts
find /workspaces/test-runner -name "*.sh" -type f -exec chmod +x {} \;

echo "Post-Create Commands Complete!"