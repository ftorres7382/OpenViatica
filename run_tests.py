from ast import parse
import sys
import subprocess
import time
import argparse

parser = argparse.ArgumentParser(
    description="A tests runner",
)

parser.add_argument("--uv_command", default="uv", help="The command to call the uv module")

args_dict = vars(parser.parse_args())

uv_command = args_dict["uv_command"]

# Build the current project
print("Syncing dependencies...")
time.sleep(2.5)
commands_list = [
    uv_command,
    "sync"
]
subprocess.run(commands_list)

# Running tests
print("Running tests...")
time.sleep(2.5)

commands_list = [
    uv_command,
    "run",
    "pytest"
]
subprocess.run(commands_list)
