import typing as t
import shutil
from pathlib import Path
import subprocess
import time, sys, json

from app.globals import APP_CONFIG, OS
import app.Custom_Types as T


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
        self.type_helper = T.Type_Helper()

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
        
        internal_system_path = workspace_path / APP_CONFIG["workspace_settings"]["internal_system_foldername"]
        setup_script_path = internal_system_path / \
            APP_CONFIG["workspace_settings"]["sytem_config_foldername"] / \
            APP_CONFIG["workspace_settings"]["setup_script_relpath"]

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

        # Adding the necesary files to template before copy
        # This would include all things that are static and defined at the app level

        # Calculate the rel path of the workspace home based on where the setup script is located
        relative_setup_script_path = setup_script_path.relative_to(workspace_path)
        up_segments = len(relative_setup_script_path.parents) - 1
        script_to_root_relpath = Path(*([".."] * up_segments))

        # All the paths will be set up as if looking ath the workspace root area
        workspace_config: T.WORKSPACE_SETUP_CONFIG_DICT = {
            "script_to_root_relpath": str(script_to_root_relpath) ,
            "user_workspace_foldername": APP_CONFIG["workspace_settings"] ["user_workspace_foldername"],
            "setup_script_relpath": str(relative_setup_script_path),
            "internal_system_foldername": APP_CONFIG["workspace_settings"]["internal_system_foldername"],
            "sytem_config_foldername": APP_CONFIG["workspace_settings"]["sytem_config_foldername"],       
            "system_utilities_foldername" : APP_CONFIG["workspace_settings"]["system_utilities_foldername"]    
        }
        # Write the type of the config to the template and workspace directory
        # This centralizes the expectations
        type_definitions_content = self.type_helper.get_typed_dict_definition_content(T.WORKSPACE_SETUP_CONFIG_DICT)
        type_definitions_content = "from typing_extensions import TypedDict\nfrom pydantic import ConfigDict\n"\
            + type_definitions_content

        # Write to template
        template_custom_types_path = template_workspace_folder_path/\
            APP_CONFIG["workspace_settings"]["internal_system_foldername"]/\
            APP_CONFIG["workspace_settings"]["sytem_config_foldername"]/\
            Path(APP_CONFIG["workspace_settings"]["setup_script_relpath"]).parent/\
            "custom_types.py"
        
        with open(template_custom_types_path, "w") as f:
            f.write(type_definitions_content)


        shutil.copytree(template_workspace_folder_path, workspace_path, dirs_exist_ok=True)           
        

        # Run the setup script
        print("Copying over the configs that can be made public and are relevant")

        # Write the config file as a json in the same folder as the setup
        workspace_config_path = setup_script_path.parent / "config.json"
        
        with open(workspace_config_path, mode='w') as f:
            f.write(json.dumps(workspace_config, indent=4))
        print("Running workspace setup...")
        subprocess.run([sys.executable, str(setup_script_path)], check=True)
        
      
        


        
    
    def print(self, value:t.Any, verbose:bool) -> None:
        if verbose:
            print(value)