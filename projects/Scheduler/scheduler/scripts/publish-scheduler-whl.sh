#!/bin/bash
#
#   A script to push scheduler whl file to azure artifacts feed.
#

set -e +x pipefail
PACKAGE_NAME="scheduler"
ACCESS_TOKEN=$SYSTEM_ACCESSTOKEN
STAGING_DIR=$ARTIFACT_STAGING_DIR


cd ./Scheduler
VERSION=$(poetry version -s)
cd ..
FEED_URL="https://pkgs.dev.azure.com/msdata/Tina/_packaging/CI-Test-Automation/pypi"
echo "Version to be uploaded: $VERSION"
echo "Checking if version $VERSION exists in feed $FEED_URL..."
RESPONSE=$(curl -s -u $ACCESS_TOKEN: \
    "$FEED_URL/simple/$PACKAGE_NAME/")
if echo "$RESPONSE" | grep -q "$VERSION"; then
  echo "Version $VERSION already exists. Skipping upload."
  exit 0
else
  echo "Version $VERSION does not exist. Proceeding with upload."
  python -m twine upload -r CI-Test-Automation --config-file $PYPIRC_PATH $STAGING_DIR/scheduler/*.whl
fi
