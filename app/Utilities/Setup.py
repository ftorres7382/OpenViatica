'''
This file will house all the functions needed to setup the application or space.
'''
from app.Utilities.Sqla_Helper import Sqla_Helper

sqla_helper = Sqla_Helper()

def sqlite_setup() -> None:
    pass

def postgres_setup() -> None:
    raise NotImplementedError("ERROR! Postgres setup has not been implemented yet!")

def database_setup() -> None:
    '''
    This function sets up the database.
    '''
    if not sqla_helper.database_exists():
        sqla_helper.create_database()
    
        
        
    

    