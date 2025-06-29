'''
This script assumes that it is already in the workspace, so when setting up a new workspace, you need to copy this into it
'''
from pathlib import Path
import json
import os
import custom_types as T # type: ignore
import subprocess
import sys
import shutil

def run() -> None:
    script_filepath = Path(__file__)
    script_folderpath = script_filepath.parent
    config_filepath = script_folderpath / "config.json"

    with open(config_filepath) as f:
        config: T.WORKSPACE_SETUP_CONFIG_DICT = json.load(f)


    # Change the working directory
    os.chdir(script_folderpath)
    os.chdir(config["script_to_root_relpath"])

    root_workspace_path = os.getcwd()

    # Now to set everything up
    # First setup venv
    venv_path = Path(config["user_workspace_foldername"])/".venv"
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)

    # Go to the venv, we are looking first for bin or Scripts
    # default to bin
    venv_python_path = venv_path / "bin/python"
    if not venv_python_path.exists():
        venv_python_path = venv_path / "Scripts/python.exe"
    
    if not venv_python_path.exists():
        raise Exception("ERROR! Cannot find the python venv!")
    
    # Install poetry in this venv
    subprocess.run([str(venv_python_path), "-m", "pip", "install", "poetry"])

    # Copy the pyproject.toml file to the work area
    script_folder_relpath = script_folderpath.relative_to(root_workspace_path)
    source_pyproject_relpath = script_folder_relpath / "pyproject.toml"
    destination_pyproject_relpath = Path(config["user_workspace_foldername"])/"pyproject.toml"
    shutil.copy(source_pyproject_relpath, destination_pyproject_relpath)

    # Now just install the dependencies
    os.chdir(Path(config["user_workspace_foldername"])) # Changing the path because idk how poetry will like me being in another dir
    new_venv_relpath = venv_python_path.relative_to(config["user_workspace_foldername"])
    
    subprocess.run([str(new_venv_relpath), "-m", "poetry", "install"])

    # change dir back to root as a default
    os.chdir(root_workspace_path)  



if __name__ == "__main__":
    run()
