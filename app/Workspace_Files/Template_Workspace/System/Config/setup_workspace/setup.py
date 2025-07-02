'''
This script assumes that it is already in the workspace, so when setting up a new workspace, you need to copy this into it

Maybe this should be integrated into via_utils? idk
'''
from pathlib import Path
import json
import os
import custom_types as T # type: ignore
import subprocess
import sys
import shutil
from pydantic import TypeAdapter

def run() -> None:
    script_filepath = Path(__file__)
    script_folderpath = script_filepath.parent
    config_filepath = script_folderpath / "config.json"

    with open(config_filepath) as f:
        config: T.WORKSPACE_SETUP_CONFIG_DICT = json.load(f)
    
    # Check the dictionary
    adapter = TypeAdapter(T.WORKSPACE_SETUP_CONFIG_DICT)
    config = adapter.validate_python(config)

    


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
    
    venv_python_path = venv_python_path.as_posix()
    
    # Install poetry in this venv
    subprocess.run([venv_python_path, "-m", "pip", "install", "poetry"])

    # Copy the pyproject.toml file to the work area
    script_folder_relpath = script_folderpath.relative_to(root_workspace_path)
    source_pyproject_relpath = script_folder_relpath / "pyproject.toml"
    destination_pyproject_relpath = Path(config["user_workspace_foldername"])/"pyproject.toml"
    shutil.copy(source_pyproject_relpath, destination_pyproject_relpath)

    # Changing the path because idk how poetry will like me being in another dir
    os.chdir(Path(config["user_workspace_foldername"])) 

    # Now just install the dependencies using poetry in the venv
    venv_python_relpath = Path(venv_python_path).relative_to(config["user_workspace_foldername"]).as_posix()
    subprocess.run([venv_python_relpath, "-m", "poetry", "install"], env={})

    # Add autoloading of the via_utils module
    ## get the location of the site packages
    result = subprocess.run(
        [venv_python_relpath, "-c", "import site; print(site.getsitepackages()[0])"],
        capture_output=True, text=True, check=True
    )
    site_packages_path = Path(result.stdout.strip())
    site_packages_relpath = site_packages_path.relative_to(os.getcwd())

    
    ## Create the file in the site packages that will import via_utils an
    with open(Path(site_packages_relpath) / "python_startup_OpenViatica.pth", "w") as f:
        f.write(f"import os; os.chdir('{Path(os.getcwd()).as_posix()}')")


    # change dir back to root as a default
    os.chdir(root_workspace_path)  



if __name__ == "__main__":
    run()
