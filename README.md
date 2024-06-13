# SDXL Pipeline for Lilypad and Docker 🐋
Based on ComfyUI, the SDXL Pipeline modules for Lilypad allow you generate images on Lilypad using Stable Diffusion XL and related models.

# Usage
These modules are designed to be run in a Docker container, either through the Lilypad Network or in Docker directly.

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
| `Batching` | How many images to produce | `1` | `1`, `2`, `4`, `8` |

See the usage sections for the runner of your choice for more information on how to set and use these variables.

## Lilypad
To run SDXL Pipeline in Lilypad, you can use the following commands:

### SDXL 1.0
Base:
```bash
lilypad run sdxl-pipeline:v1.0-base-lilypad3 -i Prompt="an astronaut floating against a white background"
```

Refiner:
```bash
lilypad run sdxl-pipeline:v1.0-refiner-lilypad3 -i Prompt="an astronaut floating against a white background"
```

### Specifying tunables

If you wish to specify more than one tunable, such as the number of steps, simply add more `-i` flags, like so:

```bash
lilypad run sdxl-pipeline:v1.0-base-lilypad3 -i Prompt="an astronaut floating against a white background" -i Steps=69
```

See the options and tunables section for more information on what tunables are available.

## Docker

To run these modules in Docker, you can use the following commands:

Base:
```bash
docker run -ti --gpus all \
    -v $PWD/outputs:/outputs \
    -e PROMPT="an astronaut floating against a white background" \
    -e STEPS=50 \
    sdxl-pipeline:v1.0-base-lilypad3
```

Refiner:
```bash
docker run -ti --gpus all \
    -v $PWD/outputs:/outputs \
    -e PROMPT="an astronaut floating against a white background" \
    -e STEPS=50 \
    sdxl-pipeline:v1.0-refiner-lilypad3
```

### Specifying tunables
If you wish to specify more than one tunable, such as the number of steps, simply add more `-e` flags, like so:

```bash
-e PROMPT="an astronaut floating against a white background" \
-e STEPS=69 \
-e SIZE=2048 \
```


