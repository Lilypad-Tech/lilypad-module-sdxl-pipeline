#/usr/bin/env python3
import sys
import subprocess
import os
import requests
import json
import threading
import signal
from urllib import request, parse
import time
import subprocess
import logging

def run_comfyui():
    global comfyui_thread
    comfyui_thread = subprocess.Popen(["python3", "/app/ComfyUI/main.py", "--listen", "127.0.0.1", "--output-directory", "/outputs/"])

def stop_comfyui():
    global comfyui_thread
    if comfyui_thread:
        # Send SIGINT (CTRL+C) to the subprocess
        comfyui_thread.send_signal(signal.SIGINT)
        # Wait for the subprocess to terminate
        comfyui_thread.wait()
        # End the thread
        comfyui_thread = None

# Run ComfyUI in a subprocess.
debug_mode = False

# Check if --debug flag is passed
if "--debug" in sys.argv:
    debug_mode = True

# Check if DEBUG_MODE environment variable is set to true
if os.environ.get("DEBUG_MODE") == "true":
    debug_mode = True

# Start ComfyUI in a background thread
comfyui_thread = threading.Thread(target=run_comfyui)
comfyui_thread.start()

# Wait for the server to be ready
startup_check_url = "http://127.0.0.1:8188/queue"
response = None
timeout = 30 # If ComfyUI doesn't start within 10 seconds, we'll give up

start_time = time.time()
timer = start_time
delay = 1 # How long to wait between checks

while timer - start_time < timeout:
    try:
        response = requests.get(startup_check_url, timeout=5)
        if response is None or response.status_code != 200:
            if response:
                print(f"Server not ready yet ({response.status_code}). Waiting 1 second...")
            else:
                print("Server not ready yet (no response). Waiting 1 second...")
            time.sleep(delay)
            timer = time.time()
        else:
            break
    except requests.exceptions.RequestException as e:
        print("Server not ready yet (requests raised an exception). Waiting 1 second...")
        time.sleep(delay)
        timer = time.time()

if response is None or response.status_code != 200:
    # Print last status code if available
    if response:
        print(f"Fatal error: Failed to connect to the server. Status code: {response.status_code}")
    print("Fatal error: Failed to connect to the server within the timeout period.")
    sys.exit(1)

# Sleep for a second to give the server time to start up
time.sleep(1)

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

# Get size from $SIZE, falling back to 512 if not set
# Valid sizes are 256, 512, 1024
size = os.environ.get("SIZE") or "512"
if size not in ["256", "512", "1024"]:
    print(f"Invalid size {size}. Must be one of 256, 512, 1024.")
    stop_comfyui()
    sys.exit(1)

# give some easy-to-remember names to the nodes
chkpoint_loader_node = prompt_workflow["4"]
prompt_pos_node = prompt_workflow["6"]
empty_latent_img_node = prompt_workflow["5"]
ksampler_node = prompt_workflow["3"]
save_image_node = prompt_workflow["9"]

# load the checkpoint that we want.
chkpoint_loader_node["inputs"]["ckpt_name"] = "sd_xl_refiner_0.9.safetensors"

# set image dimensions and batch size in EmptyLatentImage node
empty_latent_img_node["inputs"]["width"] = 1024
empty_latent_img_node["inputs"]["height"] = 1024

# set the text prompt for positive CLIPTextEncode node
prompt_pos_node["inputs"]["text"] = prompt

# set the seed in KSampler node
ksampler_node["inputs"]["seed"] = seed

# set the filename output prefix
save_image_node["inputs"]["filename_prefix"] = "output"

# everything set, add entire workflow to queue.
queue_prompt(prompt_workflow)

# Wait for the prompt to finish
def check_queue_status():
    try:
        response = requests.get("http://127.0.0.1:8188/queue", timeout=5)
        if response is None or response.status_code != 200:
            if response:
                print(f"Server not ready ({response.status_code}). Waiting 1 second...")
            else:
                print("Server not ready (no response). Waiting 1 second...")
            return "NOTREADY"
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        print("Server not ready (requests raised an exception). Waiting 1 second...")
        return "NOTREADY"

# Check the queue status
queue_status = check_queue_status()
timeout = 900 # If prompt doesn't finish within 900 seconds, we'll give up
start_time = time.time()
timer = start_time
while timer - start_time < timeout:
    queue_status = check_queue_status()
    if queue_status == {"queue_running": [], "queue_pending": []}:
        print("Prompt finished successfully.")
        break
    else:
        print("[DEBUG] Prompt is still running. Waiting 1 second...")
        time.sleep(1)
        timer = time.time()
else:
    print("Prompt is still running or there was an error.")
    # Kill the ComfyUI server and exit with an error
    stop_comfyui()
    sys.exit(1)

# We made it!
# Kill the ComfyUI server and exit cleanly.
stop_comfyui()
exit(0)
