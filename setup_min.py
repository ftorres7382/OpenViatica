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
        _ = subprocess.check_call([sys.executable, "-m", "venv", venv_fullpath])


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
    _ = subprocess.check_call([pip_path, "install"] + dependencies)

    # Print further instructions
    print("-"*20)
    print("SUCCESS!")
    print(f"Python virtual environment has been created in '{venv_fullpath}'\n")
    
    # Print instructions based on the shell
    shell = detect_shell()
    venv_modules_path = os.path.dirname(pip_path)

    if shell == "bash" or shell == "zsh":
        activate_command = f"source '{os.path.join(venv_modules_path, 'activate')}'"
    elif shell == "fish":
        activate_command = f"source '{os.path.join(venv_modules_path, 'activate.fish')}'"
    elif shell == "powershell":
        # Its possible the powershell command is broken but I do not want to test it out right now 
        activate_command = f"'{os.path.join(venv_modules_path, 'activate.ps1')}'"
    elif shell == "cmd":
        activate_command = f"'{os.path.join(venv_modules_path, 'activate.bat')}'"
    else:
        raise Exception("ERROR in the source command determination!")

    print("Please run the command below to activate the new environment:")
    print(activate_command)



def detect_shell() -> t.Literal["bash", "fish", "zsh", "powershell", "cmd"]:
    # --- Windows Logic ---
    if sys.platform == "win32":
        if any(var in os.environ for var in ["PSModulePath", "PSExecutionPolicyPreference"]):
            return "powershell"
        if "PROMPT" in os.environ:
            return "cmd"
        return "bash" # For Git Bash/WSL users on Windows

    # --- Unix/Linux Logic (CachyOS) ---
    # 1. Highest Priority: Check the actual parent process name
    try:
        # /proc/PPID/comm contains the command name of the parent process
        with open(f"/proc/{os.getppid()}/comm", "r") as f:
            parent_name = f.read().strip().lower()
            if parent_name in ["fish", "bash", "zsh"]:
                return t.cast(t.Literal["fish", "bash", "zsh"], parent_name)
    except (FileNotFoundError, PermissionError):
        pass

    # 2. Fallback: Check the SHELL environment variable
    shell_env = os.environ.get("SHELL", "").lower()
    if "fish" in shell_env:
        return "fish"
    if "zsh" in shell_env:
        return "zsh"
    
    raise ValueError("ERROR! Could NOT detect shell!")


if __name__ == "__main__":
    main()