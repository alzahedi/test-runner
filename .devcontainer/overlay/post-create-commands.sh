#!/bin/bash -xe

# Install global python packages
pip3 install --upgrade -r "/workspaces/test-runner/.devcontainer/overlay/requirements.txt"

# Add Azure CLI extensiosn
az extension add --name azure-devops

echo "Post-Create Commands Complete!"