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



        # For now we will use the template to create the workspace
        template_workspace_folder_path = Path(
            APP_CONFIG["workspace_settings"]["template_workspace_folder_path"]
        )
        workspace_path = Path(folderpath) / workspace_name 
        
        user_workspace_path = workspace_path / APP_CONFIG["workspace_settings"]["user_workspace_relpath"]
        internal_system_path = workspace_path / APP_CONFIG["workspace_settings"]["internal_system_relpath"]
        workspace_venv_path = user_workspace_path / Path(".venv")
        
        base_requirements_workspace_path = internal_system_path / APP_CONFIG["workspace_settings"]["venv_requirements_relpath"]


        # Add entry to the database
        print(f"Registering {workspace_name} in the database...")
        try:
            self.workspaces_helper.add_entry(
                workspace_name=workspace_name,
                folder_path=folderpath
            )
        except Exception as e:
            pass


        self.print(f"Creating the {workspace_name} in '{workspace_path}' ...", verbose=verbose)
        shutil.copytree(template_workspace_folder_path, workspace_path, dirs_exist_ok=True)           
        

        # Create the .venv folder
        self.print(f"Creating the virtual environment in '{workspace_venv_path}' ...", verbose=verbose)
        time.sleep(1)
        
        if not workspace_venv_path.exists():
            subprocess.check_call(["python", "-m", "venv", workspace_venv_path])

        # Setup venv in the workspace
        # Install requirements
        if OS == "Windows":
            workspace_python_path =  workspace_venv_path / "Scripts/python.exe"
        else:
            workspace_python_path =  workspace_venv_path / "bin/python"
        subprocess.check_call([str(workspace_python_path), "-m", "pip", "install", "-r", base_requirements_workspace_path])

        # Setup VS Code settings
        


        
    
    def print(self, value:t.Any, verbose:bool) -> None:
        if verbose:
            print(value)