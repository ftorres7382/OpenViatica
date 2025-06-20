'''
This file will house all the functions needed to setup the application or space.
'''
from app.Utilities import Sqla_Helper
from app.Utilities.Database_Helpers import Principals_Helper

class Setup():
    def __init__(self) -> None:
        self.sqla_helper = Sqla_Helper()
        self.principals_helper = Principals_Helper()

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


    
        
        
    

    