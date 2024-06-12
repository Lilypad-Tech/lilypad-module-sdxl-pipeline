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
if [[ -z $V0_9_BASE || -z $V0_9_REFINER || -z $V1_0_BASE || -z $V1_0_REFINER || -z $V1_0_BASE_HIRESFIX ]]; then
    echo "Please set the Docker versions in VERSIONS.env before building."
    exit 1
fi

# Check that HUGGINGFACE_TOKEN is set
if [[ -z $HUGGINGFACE_TOKEN ]]; then
    echo "Please set the HUGGINGFACE_TOKEN before building."
    exit 1
fi

# Build the Docker containers for each model
echo "Building Docker containers..."

# Turn on Docker BuildKit and cd to the docker directory
cd ../docker/
export DOCKER_BUILDKIT=1

# Login to the ECR public repository
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/lilypad-network

# Build the v0.9 modules
docker build -f Dockerfile-sdxl-0.9-base -t public.ecr.aws/lilypad-network/sdxl:v0.9-base-lilypad$V0_9_BASE --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
docker build -f Dockerfile-sdxl-0.9-refiner -t public.ecr.aws/lilypad-network/sdxl:v0.9-refiner-lilypad$V0_9_REFINER --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
# Build the v1.0 modules
docker build -f Dockerfile-sdxl-1.0-base -t public.ecr.aws/lilypad-network/sdxl:v1.0-base-lilypad$V1_0_BASE --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
docker build -f Dockerfile-sdxl-1.0-refiner -t public.ecr.aws/lilypad-network/sdxl:v1.0-refiner-lilypad$V1_0_REFINER --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
# Build the v1.0 module with the HiResFix
docker build -f Dockerfile-sdxl-1.0-base-hiresfix -t public.ecr.aws/lilypad-network/sdxl:v1.0-base-hiresfix-lilypad$V1_0_BASE_HIRESFIX --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .

# Publish the Docker containers
echo "Publishing Docker containers..."
docker push public.ecr.aws/lilypad-network/sdxl:v0.9-base-lilypad$V0_9_BASE
docker push public.ecr.aws/lilypad-network/sdxl:v0.9-refiner-lilypad$V0_9_REFINER
docker push public.ecr.aws/lilypad-network/sdxl:v1.0-base-lilypad$V1_0_BASE
docker push public.ecr.aws/lilypad-network/sdxl:v1.0-refiner-lilypad$V1_0_REFINER
docker push public.ecr.aws/lilypad-network/sdxl:v1.0-base-hiresfix-lilypad$V1_0_BASE_HIRESFIX

# Inform the user they should test the new Docker containers before releasing the associated Lilypad modules
echo "Please test the new Docker containers prior to running release.sh."
