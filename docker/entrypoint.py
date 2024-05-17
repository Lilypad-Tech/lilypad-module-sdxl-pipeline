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

def run_ollama():
    global ollama_thread
    ollama_thread = subprocess.Popen(["ollama", "serve"])

def stop_ollama():
    global ollama_thread
    if ollama_thread:
        # Send SIGINT (CTRL+C) to the subprocess
        ollama_thread.send_signal(signal.SIGINT)
        # Wait for the subprocess to terminate
        ollama_thread.wait()
        # End the thread
        ollama_thread = None

# Process and submit our job
# ======================================================================
# This function sends a prompt workflow to the specified URL
# (http://localhost:11434/api/generate) and waits for the result
# running at that address.
def run_prompt(prompt_workflow):
    p = prompt_workflow
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://localhost:11434/api/generate", data=data)
    with request.urlopen(req) as response:
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
    
    return result
# ======================================================================

# Core settings
timeout = 30 # If ollama doesn't start within this many seconds, we'll give up
batching = 1 # Default batch size

# Run ollama in a subprocess.
debug_mode = False

# Check if --debug flag is passed
if "--debug" in sys.argv:
    debug_mode = True

# Check if DEBUG_MODE environment variable is set to true
if os.environ.get("DEBUG_MODE") == "true":
    debug_mode = True

# Start ollama in a background thread
ollama_thread = threading.Thread(target=run_ollama)
ollama_thread.start()

# Wait for the server to be ready
startup_check_url = "http://localhost:11434/"
response = None

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
            print("Server is ready.")
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
time.sleep(3)

# read workflow api data from file and convert it into dictionary
# assign to var prompt_workflow
prompt_workflow = json.load(open('workflow.json'))

# Get prompt from $PROMPT, falling back to "question mark floating in space" if not set
prompt = os.environ.get("PROMPT") or "question mark floating in space"
prompt_workflow["prompt"] = prompt

# everything set, add entire workflow to queue.
model_response = run_prompt(prompt_workflow)

# Ensure the output directory exists
os.makedirs('/outputs', exist_ok=True)
# Save the response as /outputs/response.json
print(model_response)
with open('/outputs/response.json', 'w') as f:
    json.dump(model_response, f)

# We made it!
# Kill the ollama server and exit cleanly.
stop_ollama()
exit(0)
