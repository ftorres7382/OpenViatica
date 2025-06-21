import typing as t
import sqlalchemy.orm as sqla_orm
import uuid


from app.Database_Models.App_Models import Workspaces
from app.Utilities import Sqla_Helper
from app import Custom_Types as T

class Workspaces_Helper():
    
    def __init__(self) -> None:
        self.sqla_helper = Sqla_Helper()
        

    def add_entry(self, workspace_name: str, folder_path: str) -> None:
        '''
        This function adds a new entry to the table
        '''        
        id = str(uuid.uuid4())

        with sqla_orm.Session(self.sqla_helper.get_engine()) as session:

            # Check if the entry already exists
            new_entry = Workspaces(
                ID=id,
                WORKSPACE_NAME=workspace_name,
                WORKSPACE_FOLDER_PATH=folder_path
            )
            session.add(new_entry)
            session.commit()

        



