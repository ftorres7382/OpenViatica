import typing as t
from pathlib import Path



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
                         folderpath: str
                        #  Still needs the access restrictions and stuff for later
                         ) -> None: 
        '''
        This function will take the care of creating the workspace
        '''

        # For now we will just create the minimum necesary folder paths
        workspace_path = Path(folderpath)
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
            "Internal/config",
            # Storing workspace logs
            "Internal/Logs",

            # For any temporary files
            "Internal/Temp",

            # Folder to store any data files
            "Workspace/Data",
            # For all the user workspaces and Repos
            "Workspace/Workspace",

            # For any data you want visible or to be shared
            "Workspace/Exports"
        ]

        workspace_dirs: t.List[Path] = [Path(item) for item in str_workspace_dirs]

        for workspace_dir in workspace_dirs:
            full_path = workspace_path / workspace_dir 
            full_path.mkdir(parents=True, exist_ok=True)