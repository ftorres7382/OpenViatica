
import os


from OpenViatica._types import openviatica_workspace_types as ov_ws_t
from  OpenViatica._errors import ov_errors as ov_err 
from OpenViatica._general_core import General as G

from typeguard import typechecked
import toml
import typing as t

DEFAULT_WORKSPACE_TOML_FILENAME = "workspace.toml"



class BaseWorkspaceService:
    @classmethod
    @typechecked
    def create_workspace_toml(
        cls,
        folderpath:str,
        toml_filename:str,
        workspace_name:str,
        workspace_type: ov_ws_t.ws_type_t,
        workspace_id:str
        ) -> None:
        '''Creates the required workspace toml file'''
        
        # Validate that the folder exists
        if not os.path.exists(folderpath):
            raise ov_err.FolderExistsError(f"The folder '{folderpath}' does NOT exist!")
        
        # Validate that the toml file does NOT already exist
        toml_filepath = os.path.join(folderpath, toml_filename)
        if os.path.exists(toml_filepath):
            raise FileExistsError(f"The file '{toml_filepath}' ALREADY exists!")
        
        # Create the toml dictionary
        toml_dict: ov_ws_t.TEMPLATE_WORKSPACE_TOML_DICT_TYPE = {
            "id": workspace_id,
            "name": workspace_name,
            "type": workspace_type
        }
        with open(toml_filepath, 'w') as f:
            toml.dump(toml_dict, f)

   

class MetaWorkspaceService:
    '''
    Service class where all methods recieve the workspace folderpath.

    The methods can get information or transform the workspace in any way
    
    This service class handles an OpenViatica Workspace, a workspace of other workspaces
    '''    
    DEFAULT_WORKSPACE_NAME:t.Final = "ov-meta"
    DEFAULT_METADATA_FOLDERPATH:t.Final = "." + DEFAULT_WORKSPACE_NAME

    WORKSPACE_TYPE: t.Final = DEFAULT_WORKSPACE_NAME

    




    @classmethod
    @typechecked
    def initialize(
        cls,
        folderpath:str,
        workspace_metadata_path:str,
        workspace_toml_filename:str ,
        workspace_name: str,
        workspace_id: str,        
        ) -> None:
        '''Initializes a new openviatica workspace'''
        
        # Standardize the path values
        folderpath = G.get_posix_path(folderpath)
        workspace_metadata_path = G.get_posix_path(workspace_metadata_path)

        # Check that the folder exists
        if not os.path.exists(folderpath):
            raise ov_err.FolderNotFoundError(f"The folder '{folderpath}' does NOT exist.")
        
        # The workspace metadata path must NOT exist
        if os.path.exists(workspace_metadata_path):
            raise ov_err.WorkspaceMetadataExistsError(f"Workspace metadata folder detected in '{workspace_metadata_path}'! The metadata folder must be removed to sucessfully initialize a new workspace.")

        # Create the workspace folder
        os.mkdir(workspace_metadata_path)

        # Now we can just create the toml file in the workspace folder
        BaseWorkspaceService.create_workspace_toml(
            folderpath=workspace_metadata_path,
            toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=cls.WORKSPACE_TYPE
        )

