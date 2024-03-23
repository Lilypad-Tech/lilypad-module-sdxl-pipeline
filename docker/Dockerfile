FROM nvidia/cuda:12.3.2-base-ubuntu22.04 AS builder

ARG HUGGINGFACE_TOKEN

RUN mkdir /app
WORKDIR /app

# TODO: Cleanup and re-eval how many of these dependencies are actually necessary
# Install dependencies
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && apt-get install -y python3 python3-pip git libgl1-mesa-glx libglib2.0-0 && \
    pip3 install huggingface_hub==0.21.4

# Download ComfyUI
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /app/ComfyUI/

# Install dependencies for NVIDIA
RUN export DEBIAN_FRONTEND=noninteractive && \
    apt-get update -y && apt-get install -y python3 python3-pip git libgl1-mesa-glx libglib2.0-0 && \
    pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121 && \
    pip3 install -r /app/ComfyUI/requirements.txt && \
    pip3 install huggingface_hub==0.21.4

# # Download models, SDXL 1.0 Refiner
# RUN huggingface-cli login --token $HUGGINGFACE_TOKEN && \
#     huggingface-cli download stabilityai/stable-diffusion-xl-refiner-1.0 sd_xl_refiner_1.0.safetensors --local-dir-use-symlinks False --local-dir /app/ComfyUI/models/checkpoints/ && \
#     rm /root/.cache/huggingface/token

# Download models, SDXL 0.9 Refiner
RUN huggingface-cli login --token $HUGGINGFACE_TOKEN && \
    huggingface-cli download stabilityai/stable-diffusion-xl-refiner-0.9 sd_xl_refiner_0.9.safetensors --local-dir-use-symlinks False --local-dir /app/ComfyUI/models/checkpoints/ && \
    rm /root/.cache/huggingface/token

FROM builder as runner
ADD entrypoint.py /app/entrypoint.py

# Add our workflows
ADD workflows/sdxl-0.9-refiner.json /app/workflow.json

ENTRYPOINT ["python3", "/app/entrypoint.py"]
