# The purpose of this file is to define any setup scripts needed to get things going
import subprocess
import sys
import os
import typing as t
import time

venv_relpath = ".venv"
dependencies = [
    "hatch",
    "uv"
]

# Calculated variables

# In case someone is calling it out of the directory (like me), change the path to the path of this setup file
base_dir = os.path.dirname(__file__).replace("\\", "/")

venv_fullpath = os.path.abspath(os.path.join(base_dir, venv_relpath))

def main() -> None:
    '''
    Runs the setup.py logic
    Main steps would be: 
        1. Setup venv
    '''
    # Create .venv
    print(f"Setting up virtual environment: {venv_fullpath}")
    if not os.path.exists(venv_fullpath):
        subprocess.check_call([sys.executable, "-m", "venv", venv_fullpath])


    # Install dependencies using pip
    print("Installing minimum dependencies in virtual environment...")
    time.sleep(1)
    
    # Check which version of the pip path is found in the venv
    results = os.listdir(venv_fullpath)
    if "bin" in results:
        pip_path = os.path.join(venv_fullpath, "bin/pip")
    elif "Scripts" in results:
        pip_path = os.path.join(venv_fullpath, "Scripts/pip.exe")
    else:
        raise ValueError(f"ERROR! There is another unknown name for the venv folder! Results obtained: {results}")
    
    # Install dependencies
    subprocess.check_call([pip_path, "install"] + dependencies)

    # Print further instructions
    print("-"*20)
    print("SUCCESS!")
    print(f"Python virtual environment has been created in '{venv_fullpath}'\n")
    
    # Print instructions based on the shell
    shell = detect_shell()
    venv_modules_path = os.path.dirname(pip_path)
    if shell == "unix":
        activate_command = f"source '{os.path.join(venv_modules_path, 'activate')}'"
    elif shell == "powershell":
        # Its possible the powershell command is broken but I do not want to test it out right now 
        activate_command = f"'{os.path.join(venv_modules_path, 'activate.ps1')}'"
    elif shell == "cmd":
        activate_command = f"'{os.path.join(venv_modules_path, 'activate.bat')}'"

    print("Please run the command below to activate the new environment:")
    print(activate_command)



def detect_shell() -> t.Literal["unix", "powershell", "cmd"]:
    if sys.platform != "win32":
        return "unix"
    # Check environment for PowerShell indicators
    if any(var in os.environ for var in ["PSModulePath", "PSExecutionPolicyPreference"]):
        return "powershell"
    # Default fallback to cmd.exe
    if "PROMPT" in os.environ:
        return "cmd"
    
    raise ValueError("ERROR! Could NOT detect shell!")


if __name__ == "__main__":
    main()