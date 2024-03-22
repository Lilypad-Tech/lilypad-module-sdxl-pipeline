import subprocess
import sys
# Run inference.py and report any errors and stdout
try:
    output = subprocess.check_output(['python3', 'inference.py'])
    print(output.decode('utf-8'))
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Run video.py and report any errors and stdout
try:
    output = subprocess.check_output(['python3', 'video.py'])
    print(output.decode('utf-8'))
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)
