# SDXL to SV3D pipeline in Docker 🐋
Initially built with SDXL-0.9, this will later use SDXL-1.0.

This script will generate an image using SDXL, then take the result and send it through SV3D to generate a 3D video.

## Usage
```
export HUGGINGFACE_TOKEN=<my huggingface token>
```
```
# From the root directory of this repository, change to the docker folder.
cd docker/
# Build the docker image
DOCKER_BUILDKIT=1 docker build --no-cache -t sdxl-sv3du:v0.9-sv3d-lilypad1 -f Dockerfile --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
```
```
mkdir -p outputs
```
```
docker run -ti --gpus all \
    -v $PWD/outputs:/outputs \
    -e OUTPUT_DIR=/outputs/ \
    -e PROMPT="an astronaut floating against white background" \
    sdxl-sv3du:v0.9-sv3d-lilypad1
```
Will overwrite `outputs/image0.png` each time.

## Run it in Lilypad
You can run the following to run a Lilypad job using this module:
`lilypad run sdxl-sv3du:v0.9-sv3d-lilypad1 -i PROMPT="an astronaut floating against white background"`

Results (initial):
![image-42.png](media/image-42.png)

Results (final):
Coming soon

# Credits
Based on [lilypad-sdxl](https://github.com/lilypad-tech/lilypad-sdxl-module), which was written by early Lilypad contributors.
