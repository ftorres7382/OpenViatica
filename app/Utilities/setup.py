'''
This file will house all the functions needed to setup the application or space.
'''
import time
import typing as t

from app.globals import APP_CONFIG



class Setup():
    def __init__(self) -> None:
        from app.Utilities import Sqla_Helper, Workspace
        from app.Utilities.Database_Helpers import Principals_Helper
        
        self.sqla_helper = Sqla_Helper()
        self.principals_helper = Principals_Helper()
        self.workspace = Workspace()

    def sqlite_setup(self) -> None:
        pass

    def postgres_setup(self) -> None:
        raise NotImplementedError("ERROR! Postgres setup has not been implemented yet!")

    def database_setup(self, verbose: bool = False) -> None:
        '''
        This function sets up the database.
        '''
        self.print("Setting up app database...\n", verbose=verbose)
        time.sleep(1)
        # create database if not exists
        if not self.sqla_helper.database_exists():
            self.sqla_helper.create_database()
        
        # Add the admin principals
        try:
            self.principals_helper.add_principal(
                "app_admin@admin.com",
                "user"
            )
            self.principals_helper.add_principal(
                "app_admins",
                "group"
            )
        except Exception as e:
            pass

    def workspace_setup(self, folder_path:str, verbose: bool= True) -> None:
        '''
        This function sets up a new workspace 
        '''
        self.print("Setting up Admin Workspace...\n", verbose=True)
        time.sleep(1)
        self.workspace.create_workspace(
            workspace_name=APP_CONFIG["workspace_settings"]["admin_workspace_name"], 
            folderpath=folder_path,
            verbose=verbose
            )
        
    def print(self, value:t.Any, verbose:bool) -> None:
        if verbose:
            print(value)
        
        
        
        
    
        
        
    

    