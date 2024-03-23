# SDXL 0.9/1.0 pipeline in Docker 🐋
Initially built with SDXL-0.9, this will later use SDXL-1.0.

(WIP, NOT USABLE YET, HERE BE DRAGONS)

Based on ComfyUI.

## Usage
```
export HUGGINGFACE_TOKEN=<my huggingface token>
```
```
# From the root directory of this repository, change to the docker folder.
cd docker/
# Build the docker image
DOCKER_BUILDKIT=1 docker build --no-cache -t sdxl:v0.9-lilypad3 -f Dockerfile --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
```
```
mkdir -p outputs
```
```
docker run -ti --gpus all \
    -v $PWD/outputs:/outputs \
    -e OUTPUT_DIR=/outputs/ \
    -e PROMPT="an astronaut floating against white background" \
    sdxl:v0.9-sv3d-lilypad3
```
Will generate new PNG images into `outputs/` each time.

## Run it in Lilypad
You can run the following to run a Lilypad job using this module:
`lilypad run sdxl-r2:v0.9-lilypad3 -i PROMPT="an astronaut floating against white background"`

Results (initial):
![image-42.png](media/image-42.png)

# Credits
Based on [lilypad-sdxl](https://github.com/lilypad-tech/lilypad-sdxl-module), which was written by early Lilypad contributors.

Based on ComfyUI.

With thanks and a hat tip to https://medium.com/@yushantripleseven/comfyui-using-the-api-261293aa055a for great API examples and the basis of our wrapper/API script.
