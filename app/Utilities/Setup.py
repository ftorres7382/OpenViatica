'''
This file will house all the functions needed to setup the application or space.
'''
from app.globals import APP_CONFIG

def sqlite_setup() -> None:
    pass

def postgres_setup() -> None:
    raise NotImplementedError("ERROR! Postgres setup has not been implemented yet!")

def database_setup() -> None:
    '''
    This function sets up the database
    '''
    if APP_CONFIG["app_database"]["engine"] == "sqlite"
    