'''
This file will house all the functions needed to setup the application or space.
'''


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

    def database_setup(self) -> None:
        '''
        This function sets up the database.
        '''
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

    def workspace_setup(self, folder_path:str) -> None:
        '''
        This function sets up a new workspace 
        '''
        self.workspace.create_workspace(workspace_name="App_Admin_Workspace", folderpath=folder_path)
        
        
        
        
    
        
        
    

    