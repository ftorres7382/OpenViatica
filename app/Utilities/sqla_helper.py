import sqlalchemy as sqla
from sqlalchemy import event
import os
import typing as t
import sqlite3

from app.Database_Models import Base
from app.Database_Models import Principals  # Import all models so they're registered with Base


import app.Custom_Types as T


class Sqla_Helper():
    
    def __init__(self) -> None:
        '''
        This function will run all required functions and set all variables required before use
        '''
        self.connection_info = self.get_connection_info()

        if not self.can_connect():
            if not self.connection_info["engine"] == "sqlite":
                raise Exception(f"ERROR! Cannot connect to database! Connection Info: {self.connection_info}")
            else:
                # Automatically make the sqlite db
                sqla.create_engine(self.connection_info["connection_string"])
        
        self.engine = self.get_engine()


    def get_connection_info(self) -> T.SQLA_CONNECTION_INFO_DICT:
        '''
        This function looks into the app config settings and returns only the relevant parts for a connection
        '''
        from app.globals import APP_CONFIG
        engine_type = APP_CONFIG["app_database"]["engine"]
        connection_info_dict: T.SQLA_CONNECTION_INFO_DICT = {
            "engine": engine_type,
            "connection_configuration": APP_CONFIG["app_database"][engine_type],
            "connection_string": self.get_connection_string()
        }
        return connection_info_dict

    def get_connection_string(self) -> str:
        '''
        This function returns the connection string for the application's database
        '''
        from app.globals import APP_CONFIG
        if APP_CONFIG["app_database"]["engine"] == "sqlite":
            filepath = os.path.join(
                APP_CONFIG['app_database']['sqlite']['path'], 
                f"{APP_CONFIG['app_database']['database_name']}.db"
                )
            return f"sqlite:///{filepath}"
        elif APP_CONFIG["app_database"]["engine"] == "postgres":
            raise NotImplementedError("ERROR! Postgres support has not been implemented yet!")
        else:
            raise ValueError("ERROR! The only allowed values for app_database.engine are: 'sqlite' and 'postgres'")

    def get_engine(self, echo: bool  = True, connect_args: T.SQLA_ENGINE_CONNECT_ARGS_DICT_TYPE = {"timeout": 10}) -> sqla.engine.Engine:
        '''
        This function gets the sqlalchemy engine based on the app properties 
        '''
        from app.globals import APP_CONFIG
        if self.connection_info["engine"] == "sqlite":
            @event.listens_for(sqla.Engine, "connect")
            def set_sqlite_pragma(dbapi_connection: sqlite3.Connection, connection_record: t.Any) -> None:
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA journal_mode=WAL;")
                cursor.close()

            return sqla.create_engine(self.get_connection_string(), echo=echo, connect_args=connect_args)
        elif APP_CONFIG["app_database"]["engine"] == "postgres":
            raise NotImplementedError("ERROR! Postgres support has not been implemented yet!")
        else:
            raise ValueError("ERROR! The only allowed values for app_database.engine are: 'sqlite' and 'postgres'")
        
    def database_exists(self) -> bool:
        '''
        This function checks if the database exists
        '''
        from app.globals import APP_CONFIG
        if APP_CONFIG["app_database"]["engine"] == "sqlite":
            # The filepath should be configured
            filepath = os.path.join(
                APP_CONFIG['app_database']['sqlite']['path'], 
                f"{APP_CONFIG['app_database']['database_name']}.db"
                )
            return os.path.exists(filepath)
        elif APP_CONFIG["app_database"]["engine"] == "postgres":
            # The postgres would need to first test the connection and then you can check the dbs
            raise NotImplementedError("ERROR! Postgres support has not been implemented yet!")
        else:
            raise ValueError("ERROR! The only allowed values for app_database.engine are: 'sqlite' and 'postgres'")
  
    def can_connect(self) -> bool:
        '''
        This function will test that the app has connection with the database. 
        If it does not, it will raise an error.
        '''
        
        try:
            with self.engine.connect() as conn:
                conn.execute(sqla.text("SELECT 1"))
            return True
        except Exception as e:
            return False
        
    def create_database(self, verbose: bool = True) -> None:
        '''
        This function will create the database
        '''
        self.print(f"Connecting to {self.connection_info['connection_string']} ...", verbose)
        
        Base.metadata.create_all(self.engine)

    def get_table_names(self) -> t.List[str]:
        '''
        This function gets the list of table names
        '''
        engine = self.get_engine()
        inspector = sqla.inspect(engine)

        tables = inspector.get_table_names()
        return tables

    def print(self, value:str, verbose:bool = True) -> None:
        if verbose:
            print(value)
