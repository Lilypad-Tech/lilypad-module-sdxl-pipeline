# SDXL pipeline in Lilypad and Docker 🐋
**In early testing stages: here be dragons.**

Based on ComfyUI, the SDXL Pipeline module for Lilypad is a module that allows you generate images on Lilypad using Stable Diffusion XL and related models.

# Usage
This module is designed to be run in a Docker container, either through the Lilypad Network or in Docker directly.

## Lilypad
To run this module in Lilypad, you can use the following command:

```bash
lilypad run sdxl-r2:v0.9-lilypad10 -i Prompt="an astronaut floating against a white background"
```

If you wish to specify more than one tunable, such as the number of steps, simply add more `-i` flags, like so:

```bash
lilypad run sdxl-r2:v0.9-lilypad10 -i Prompt="an astronaut floating against a white background" -i Steps=69
```

See the options and tunables section for more information on what tunables are available.

## Docker

To run this module in Docker, you can use the following command:

```bash
docker run -ti --gpus all \
    -v $PWD/outputs:/outputs \
    -e PROMPT="an astronaut floating against a white background" \
    -e STEPS=50 \
    zorlin/sdxl:v0.9-lilypad10
```

If you wish to specify more than one tunable, such as the number of steps, simply add more `-e` flags, like so:

```bash
-e PROMPT="an astronaut floating against a white background" \
-e STEPS=69 \
-e SIZE=2048 \
```

See the options and tunables section for more information on what tunables are available.

## Options and tunables
The following tunables are available. All of them are optional, and have default settings that will be used if you do not provide them.

| Name | Description | Default | Available options |
|------|-------------|---------|-------------------|
| `Prompt` | A text prompt for the model | "question mark floating in space" | Any string |
| `Seed` | A seed for the model | 42 | Any valid non-negative integer |
| `Steps` | The number of steps to run the model for | 50 | Any valid non-negative integer |
| `Scheduler` | The scheduler to use for the model | `normal` | `normal`, `karras`, `exponential`, `sgm_uniform`, `simple`, `ddim_uniform` |
| `Sampler` | The sampler to use for the model | `euler_ancestral` |  `"euler"`, `"euler_ancestral"`, `"heun"`, `"heunpp2"`, `"dpm_2"`, `"dpm_2_ancestral"`, `"lms"`, `"dpm_fast"`, `"dpm_adaptive"`, `"dpmpp_2s_ancestral"`, `"dpmpp_sde"`, `"dpmpp_sde_gpu"`, `"dpmpp_2m"`, `"dpmpp_2m_sde"`, `"dpmpp_2m_sde_gpu"`, `"dpmpp_3m_sde"`, `"dpmpp_3m_sde_gpu"`, `"ddpm"`, `"lcm"` |
| `Size` | The output size requested in px | `1024` | `512`, `768`, `1024`, `2048` |

See the usage sections for the runner of your choice for more information on how to set and use these variables.

# Development
You can build the Docker containers that form this module by following these steps (replacing Dockerfile-sdxl-0.9-refiner and its Git tags with the appropriate Dockerfile and tags for the model you wish to use):

```
export HUGGINGFACE_TOKEN=<my huggingface token>
```
```
# From the root directory of this repository, change to the docker folder.
cd docker
# Build the docker image
DOCKER_BUILDKIT=1 docker build -f Dockerfile-sdxl-0.9-refiner -t zorlin/sdxl:v0.9-lilypad5 --target runner --build-arg HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN .
```
```
mkdir -p outputs
```

## Testing
Fork this repository and make your changes. Then, build a Docker container and run the module with your changes locally to test them out.

Once you've made your changes, publish your Docker image, then edit `lilypad_module.json.tmpl` to point at it and create a Git tag such as `v0.9-lilypad10`.

You can then run your module with 

`lilypad run github.com/zorlin/example:v0.1.2` to test your changes, replacing `zorlin` with your username and `v0.1.2` with the tag you created.

Note that most nodes on the public Lilypad network will be unlikely to run your module (due to allowlisting), so you may need to run a Lilypad node to test your changes. Once your module is stable and tested, you can request that it be adopted as an official module. Alternatively, if you're simply making changes to this module instead of making a new one, feel free to submit a pull request.

# Credits
Based on [lilypad-sdxl](https://github.com/lilypad-tech/lilypad-sdxl-module), which was written by early Lilypad contributors.

Based on ComfyUI.

With thanks and a hat tip to https://medium.com/@yushantripleseven/comfyui-using-the-api-261293aa055a for great API examples and the basis of our wrapper/API script. entrypoint.sh loosely based on [basic_workflow_api.py by yushan777](https://gist.github.com/yushan777/1e31e06c088550611f3a0b91ba150975).
