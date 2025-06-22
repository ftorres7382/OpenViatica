import typing as t
import shutil
from pathlib import Path
import subprocess
import time

from app.globals import APP_CONFIG, OS


class Workspace():
    '''
    This class will handle the creation, deletion and editing of any information having to do the workspace.

    It should handle:
        1. Workspaces made
        2. Setting up workspaces.
        3. Creating relevant databases
    '''

    def __init__(self) -> None:
        '''
        Sets up the internal variables if any
        '''
        from app.Utilities.Database_Helpers import Workspaces_Helper
        self.workspaces_helper = Workspaces_Helper()

    def create_workspace(self,
                         workspace_name: str,
                        #  probably needs to be changed later, but good enough for now
                         folderpath: str,
                        #  Still needs the access restrictions and stuff for later
                        verbose: bool = True
                         ) -> None: 
        '''
        This function will take the care of creating the workspace
        '''
        requirements_path = APP_CONFIG["workspace_settings"]["requirements_path"]

        # For now we will just create the minimum necesary folder paths
        workspace_path = Path(folderpath) / Path(workspace_name)

        self.print(f"Creating the {workspace_name} in '{workspace_path}' ...", verbose=verbose)

        workspace_path.mkdir(parents=True, exist_ok=True)

        
        # Add entry to the database
        try:
            self.workspaces_helper.add_entry(
                workspace_name=workspace_name,
                folder_path=folderpath
            )
        except Exception as e:
            pass
        # Create the necessary directories
        str_workspace_dirs = [
            # For keeping user databases and the like
            "Internal/Data",
            # Keeping workspaces configurations
            "Internal/Config",
            # Storing workspace logs
            "Internal/Logs",

            # For oviutils and the like.
            "Internal/Utilities",

            # For any temporary files
            "Internal/Temp",

            # Folder to store any data files
            "Workspace/Data",
            # For all the user workspaces and Repos
            "Workspace/Workspace",

            "Workspace/Workspace/Users",
            "Workspace/Workspace/Repos",

            # For any data you want visible or to be shared
            "Workspace/Exports",
        ]

        workspace_dirs: t.List[Path] = [Path(item) for item in str_workspace_dirs]

        for workspace_dir in workspace_dirs:
            full_path = workspace_path / workspace_dir 
            full_path.mkdir(parents=True, exist_ok=True)

        user_workspace_path = workspace_path / Path("Workspace")

        # Create the .venv folder
        workspace_venv_path = user_workspace_path / Path(".venv")

        self.print(f"Creating the virtual environment in '{workspace_venv_path}' ...", verbose=verbose)
        time.sleep(1)
        
        if workspace_venv_path.exists():
            shutil.rmtree(workspace_venv_path)
        
        if not workspace_venv_path.exists():
            subprocess.check_call(["python", "-m", "venv", workspace_venv_path])

        # Setup venv in the workspace
        # Copy the requirements to the config folder
        base_requirements_workspace_path = workspace_path / Path("Internal/Config") / Path(requirements_path).name
        base_requirements_workspace_folder_path = base_requirements_workspace_path.parent
        shutil.copy(requirements_path, base_requirements_workspace_folder_path)

        # Install requirements
        if OS == "Windows":
            workspace_python_path =  workspace_venv_path / "Scripts/python.exe"
        else:
            workspace_python_path =  workspace_venv_path / "bin/python"
        subprocess.check_call([str(workspace_python_path), "-m", "pip", "install", "-r", base_requirements_workspace_path])
        


        
    
    def print(self, value:t.Any, verbose:bool) -> None:
        if verbose:
            print(value)