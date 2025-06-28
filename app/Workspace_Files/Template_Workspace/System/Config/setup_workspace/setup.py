'''
This script assumes that it is already in the workspace, so when setting up a new workspace, you need to copy this into it
'''
from pathlib import Path
import json
import os
import custom_types as T
import subprocess
import sys

def run() -> None:
    script_filepath = Path(__file__)
    script_folderpath = script_filepath.parent
    config_filepath = script_folderpath / "config.json"

    with open(config_filepath) as f:
        config: T.WORKSPACE_SETUP_CONFIG_DICT = json.load(f)


    # Change the working directory
    os.chdir(script_folderpath)
    os.chdir(config["script_to_root_relpath"])

    # Now to set everything up
    # First setup venv
    venv_path = Path(config["user_workspace_foldername"])/".venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    # Go to the venv, we are looking first for bin or Scripts
    # default to bin
    venv_python_path = venv_path / "bin/python"
    if not venv_python_path.exists:
        venv_python_path = venv_path / "Scripts/python.exe"
    
    if not venv_python_path.exists():
        raise Exception("ERROR! Cannot find the python venv!")
    
    # Intall poetry in this venv
    subprocess.run([str(venv_python_path), "-m", "pip", "install", "poetry"])


if __name__ == "__main__":
    run()
