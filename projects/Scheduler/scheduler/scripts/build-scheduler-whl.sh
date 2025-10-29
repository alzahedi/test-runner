#!/bin/bash
#
#   A script to prepare Python environment from poetry.lock and build
#   whl files for scheduler using poetry.
#

set -e +x pipefail

if [ "${BUILD_SOURCESDIRECTORY}" = "" ]; then
    ENLISTMENT_ROOT=$(pwd)
else
    ENLISTMENT_ROOT=${BUILD_SOURCESDIRECTORY}
fi
echo "Enlistment root is ${ENLISTMENT_ROOT}"
pushd Scheduler

# Get Python version at runtime
echo "##[group]Python runtime version"
which python3
python3 --version
echo "##[endgroup]"

# Get pre-reqs
echo "##[group]Package installations"
echo "##[section]Perform apt installs"
sudo apt update -q
sudo apt -y install gnome-keyring

# Install poetry
echo "##[section]Perform base OS Python installs"
pip3 install --upgrade -r "requirements.txt"

# Initiate and activate virtual env
echo "##[section]Perform poetry dependency installs for scheduler"
rm -rf .venv
poetry config virtualenvs.in-project true
poetry install
source $(poetry env info --path)/bin/activate
echo "##[endgroup]"

# Build whl file for scheduler using poetry
echo "##[section]Building whl file for scheduler"
poetry build
