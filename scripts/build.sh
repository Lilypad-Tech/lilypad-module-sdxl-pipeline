#!/bin/bash

# This script is used to build all of the modules in SDXL Pipeline.
# It requires *quite a lot* of disk space - be warned!

### VERSIONS ###

### NOTE ###
# Specify the versions of the Docker and Lilypad modules in VERSIONS.env

# Change to the directory that this script is in.
cd "$(dirname "$0")"

# Load the versions
source VERSIONS.env

# Check that the Docker versions are set
if [[ -z $VLLAMA3_8B ]]; then
    echo "Please set the Docker versions in VERSIONS.env before building."
    exit 1
fi

# Build the Docker containers for each model
echo "Building Docker containers..."

# Turn on Docker BuildKit and cd to the docker directory
cd ../docker/
export DOCKER_BUILDKIT=1

# Build the llama3 8b module
docker build -f Dockerfile-llama3-8b -t zorlin/ollama:llama3-8b-lilypad$VLLAMA3_8B --target runner .

# Publish the Docker containers
echo "Publishing Docker containers..."
docker push zorlin/ollama:llama3-8b-lilypad$VLLAMA3_8B

# Inform the user they should test the new Docker containers before releasing the associated Lilypad modules
echo "Please test the new Docker containers prior to running release.sh."
echo
echo "The easiest way to test them is, well, Docker! Here's some commands to inspire you:"

echo "docker run -it --gpus all -v $PWD/outputs:/outputs -e PROMPT='what is a man? a miserable pile of secrets' zorlin/ollama:llama3-8b-lilypad$VLLAMA3_8B"
echo
echo "Don't forget to update the README.md with the new versions!"

echo "Done! We have built and published the Docker containers for the Ollama Pipeline modules. You should now be ready to run ./scripts/release.sh to release the new Lilypad versions of the modules."
