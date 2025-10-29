#!/bin/bash -xe

# Install global python packages
pip3 install --upgrade -r "/workspaces/test-runner/.devcontainer/overlay/requirements.txt"

npm install

# Invoke nx directly
npm i -g nx

# Add Azure CLI extensions
az extension add --name azure-devops

echo "Post-Create Commands Complete!"