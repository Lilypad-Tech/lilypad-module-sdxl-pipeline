import os
import torch
import argparse
from diffusers import DDIMScheduler, DiffusionPipeline
import numpy as np
import random

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Run the diffusion model with optional low memory mode.')
parser.add_argument('--low-mem', action='store_true',
                    help='Enable features to allow running on low memory GPUs')
args = parser.parse_args()

os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
torch.backends.cudnn.benchmark = False
torch.use_deterministic_algorithms(True)

def set_seed(seed: int) -> None:
    np.random.seed(seed)
    random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    os.environ["PYTHONHASHSEED"] = str(seed)
    print(f"Random seed set to {seed}")

try:
    seed = int(os.getenv("RANDOM_SEED", "42"))
except ValueError:
    print("Invalid value for RANDOM_SEED, falling back to default seed 42.")
    seed = 42
set_seed(seed)

try:
    pipe = DiffusionPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-0.9",
        torch_dtype=torch.float16,
        use_safetensors=True,
        variant="fp16",
    ).to("cuda")
    pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

    if args.low_mem:
        print("Low memory mode enabled: Model will offload parts to CPU to save GPU memory.")
        pipe.enable_model_cpu_offload()

except Exception as e:
    print(f"Failed to load the diffusion pipeline: {e}")
    exit(1)

try:
    g = torch.Generator(device="cuda")
    g.manual_seed(seed)
except Exception as e:
    print(f"Failed to initialize the random number generator: {e}")
    exit(1)

prompt = os.getenv("PROMPT", "An astronaut riding a green horse")

print(f"Generating image with prompt: {prompt}")

try:
    results = pipe(prompt=prompt, height=576, width=1024, generator=g)
    images = results.images if hasattr(results, 'images') else []
    if len(images) == 0:
        raise ValueError("No images were generated.")
    print(f"Generated {len(images)} images")
except Exception as e:
    print(f"Failed to generate images: {e}")
    exit(1)

try:
    output_dir = os.getenv("OUTPUT_DIR", "./")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image_path = os.path.join(output_dir, f"image-{seed}.png")
    images[0].save(image_path)
    print(f"Saved image to {image_path}")
except Exception as e:
    print(f"Failed to save the image: {e}")
    exit(1)
