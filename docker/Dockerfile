FROM nvidia/cuda:12.3.2-base-ubuntu22.04 AS builder

ARG HUGGINGFACE_TOKEN

RUN mkdir /app
WORKDIR /app

# Install dependencies
ADD requirements.txt /app/requirements.txt
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && apt-get install -y python3 python3-pip git libgl1-mesa-glx libglib2.0-0 && \
    pip3 install -r requirements.txt && \
    pip3 install huggingface_hub==0.21.4 && \
    huggingface-cli login --token $HUGGINGFACE_TOKEN && \
    python3 -c "from diffusers import DiffusionPipeline; import torch; pipe = DiffusionPipeline.from_pretrained('stabilityai/stable-diffusion-xl-base-0.9', torch_dtype=torch.float16, use_safetensors=True, variant='fp16'); pipe.unet = torch.compile(pipe.unet, mode='reduce-overhead', fullgraph=True); pipe.save_pretrained('/app/optimized_model')" && \
    rm /root/.cache/huggingface/token

FROM builder as runner
ADD inference.py /app/inference.py
ENTRYPOINT ["python3", "/app/inference.py"]
