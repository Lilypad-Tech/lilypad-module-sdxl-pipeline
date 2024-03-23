# SDXL pipeline in Docker 🐋
Initially built with SDXL-0.9 Refiner, this will later allow you to use all of the following models:

- SDXL-0.9-base
- SDXL-0.9-refiner
- SDXL-1.0-base
- SDXL-1.0-refiner

**In early testing stages: here be dragons.**

Based on ComfyUI.

## Usage
```
export HUGGINGFACE_TOKEN=<my huggingface token>
```
```
# From the root directory of this repository, change to the docker folder.
cd docker/
# Build the docker image
DOCKER_BUILDKIT=1 docker build --no-cache -t sdxl:v0.9-lilypad5 -f Dockerfile --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
```
```
mkdir -p outputs
```
```
docker run -ti --gpus all \
    -v $PWD/outputs:/outputs \
    -e OUTPUT_DIR=/outputs/ \
    -e PROMPT="an astronaut floating against white background" \
    sdxl:v0.9-lilypad5
```
Will generate new PNG images into `outputs/` each time.

## Run it in Lilypad
You can run the following to run a Lilypad job using this module:
`lilypad run sdxl-r2:v0.9-lilypad3 -i PromptEnv="PROMPT="an astronaut floating against white background"`

Results:

![spaceman.png](media/spaceman.png)

# Credits
Based on [lilypad-sdxl](https://github.com/lilypad-tech/lilypad-sdxl-module), which was written by early Lilypad contributors.

Based on ComfyUI.

With thanks and a hat tip to https://medium.com/@yushantripleseven/comfyui-using-the-api-261293aa055a for great API examples and the basis of our wrapper/API script. entrypoint.sh loosely based on [basic_workflow_api.py by yushan777](https://gist.github.com/yushan777/1e31e06c088550611f3a0b91ba150975).
