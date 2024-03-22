import sys
import subprocess
import os
import requests
import json
from urllib import request, parse
#/usr/bin/env python3

# Run ComfyUI in a subprocess.
debug_mode = False

# Check if --debug flag is passed
if "--debug" in sys.argv:
    debug_mode = True

# Check if DEBUG_MODE environment variable is set to true
if os.environ.get("DEBUG_MODE") == "true":
    debug_mode = True

# Run the command and passthrough stdout and stderr
subprocess.run(["python3", "/app/ComfyUI/main.py", "--listen", "--output-directory", "/outputs/"])

# Wait for the server to be ready
startup_check_url = "http://localhost:8188/queue"
response = requests.get(startup_check_url)

while response.status_code != 200:
    response = requests.get(startup_check_url)

# Process and submit our job
# ======================================================================
# This function sends a prompt workflow to the specified URL 
# (http://127.0.0.1:8188/prompt) and queues it on the ComfyUI server
# running at that address.
def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)    
# ======================================================================

# read workflow api data from file and convert it into dictionary 
# assign to var prompt_workflow
prompt_workflow = json.load(open('workflow.json'))

# Get prompt from $PROMPT, falling back to "question mark floating in space" if not set
prompt = os.environ.get("PROMPT") or "question mark floating in space"

# Get seed from $RANDOM_SEED, falling back to 42 if not set
seed = os.environ.get("RANDOM_SEED") or "42"

# give some easy-to-remember names to the nodes
chkpoint_loader_node = prompt_workflow["4"]
prompt_pos_node = prompt_workflow["6"]
empty_latent_img_node = prompt_workflow["5"]
ksampler_node = prompt_workflow["3"]
save_image_node = prompt_workflow["9"]

# load the checkpoint that we want. 
chkpoint_loader_node["inputs"]["ckpt_name"] = ""

# set image dimensions and batch size in EmptyLatentImage node
empty_latent_img_node["inputs"]["width"] = 512
empty_latent_img_node["inputs"]["height"] = 512

# set the text prompt for positive CLIPTextEncode node
prompt_pos_node["inputs"]["text"] = prompt

# set the seed in KSampler node 
ksampler_node["inputs"]["seed"] = seed

# set the filename output prefix
save_image_node["inputs"]["filename_prefix"] = "output"

# everything set, add entire workflow to queue.
queue_prompt(prompt_workflow)