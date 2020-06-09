#!/bin/bash

echo
echo "************** START: test_client.sh **********************"

# Create temporary testing directory
echo "Creating temporary directory to work in."
here="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

. $here/helpers.sh

unset RSE_CONFIG_FILE || true

# Make sure it's installed
if which rse >/dev/null; then
    printf "rse is installed\n"
else
    printf "rse is not installed\n"
    exit 1
fi

# Create temporary testing directory
tmpdir=$(mktemp -d)
output=$(mktemp ${tmpdir:-/tmp}/rse_test.XXXXXX)
config=$tmpdir/software
mkdir -p $config
printf "Created temporary directory to work in. ${config}\n"

echo
echo "#### Testing rse init"
runTest 0 $output rse init $config

echo
echo "#### Testing rse generate-key"
runTest 0 $output rse generate-key

echo
echo "#### Testing [filesystem] rse get with no repos"
runTest 0 $output rse --config_file $config/rse.ini get

echo
echo "#### Testing [filesystem] rse add for a repo"
runTest 0 $output rse --config_file $config/rse.ini add github.com/singularityhub/sregistry
runTest 0 $output ls $config/database/github/singularityhub/sregistry/metadata.json 

echo
echo "#### Testing [filesystem] rse ls"""
runTest 0 $output rse --config_file $config/rse.ini ls

echo 
echo "#### Testing [filesystem] rse clear"
runTest 0 $output rse --config_file $config/rse.ini clear --force

echo
echo "#### Testing [sqlite] rse config to use sqlite"
runTest 0 $output rse --config_file $config/rse.ini config --database sqlite

echo
echo "#### Testing [sqlite] rse add for a repo"
runTest 0 $output rse --config_file $config/rse.ini add github.com/singularityhub/sregistry

echo
echo "#### Testing [sqlite] rse ls"""
runTest 0 $output rse --config_file $config/rse.ini ls

echo 
echo "#### Testing [sqlite] rse clear"
runTest 0 $output rse --config_file $config/rse.ini clear --force


rm -rf ${tmpdir}
