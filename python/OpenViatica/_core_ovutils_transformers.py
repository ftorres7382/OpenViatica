
import os
from uuid import uuid4
from OpenViatica._general_core import General


from ._types import openviatica_workspace_types as ov_ws_t
from  ._errors import ov_errors as ov_err 
import typing as t

from typeguard import typechecked
import toml

@typechecked
def create_workspace_toml(
    folderpath:str,
    toml_filename:str,
    workspace_name:str,
    workspace_type: ov_ws_t.ws_type_t,
    workspace_id:str = str(uuid4())
    ) -> None:
    '''Creates the required workspace toml file'''
    
    # Validate that the folder exists
    if not os.path.exists(folderpath):
        raise ov_err.FolderExistsError(f"ERROR! The folder '{folderpath}' does NOT exist!")
    
    # Validate that the toml file does NOT already exist
    toml_filepath = os.path.join(folderpath, toml_filename)
    if os.path.exists(toml_filepath):
        raise FileExistsError(f"ERROR! The file '{toml_filepath}' ALREADY exists!")
    
    # Create the toml dictionary
    toml_dict: ov_ws_t.TEMPLATE_WORKSPACE_TOML_DICT_TYPE = {
        "id": workspace_id,
        "name": workspace_name,
        "type": workspace_type
    }
    with open(toml_filepath, 'w') as f:
        toml.dump(toml_dict, f)


class ovutils_service:
    '''
    Service class where all methods recieve the workspace folderpath.

    The methods can get information or transform the workspace in any way
    '''    


    @classmethod
    @typechecked
    def initialize(
        cls,
        folderpath:str
        ) -> None:
        '''Initializes a new openviatica workspace'''
        
        # Check that the folder exists
        if not os.path.exists(folderpath):
            raise ov_err.FolderNotFoundError(f"ERROR! The folder '{folderpath}' does NOT exist.")
        
        # The workspace toml must NOT exist
        workspace_toml_filepath = os.path.join(folderpath,cls.workspace_toml_filename)
        if os.path.exists(workspace_toml_filepath):
            raise FileExistsError(f"ERROR! The workspace filepath '{workspace_toml_filepath}' ALREADY exists!")
        
        # Now we can just create the toml file
        create_workspace_toml(
            folderpath=folderpath,
            toml_filename=cls.workspace_toml_filename,
            workspace_name=cls.default_workspace_name,
            workspace_id=str(uuid4()),
            workspace_type="openviatica"
        )








class templates:
    '''
    This class is designed to be a classmethod TRANSFORMER ONLY class

    All methods in this class MUST have the dirpath sent to it consistently
    '''
    workspace_toml_filename = ".ov-templates.toml"
    
    # @classmethod
    # def is_workspace(cls,folderpath:str) -> bool:
    #     '''Returns True only if the folderpath can be validated to be a tempalates workspace'''

    #     try:
    #         cls.validate_is_workspace_folder(folderpath)
    #         is_workspace = True
    #     except Exception:
    #         is_workspace = False

    #     return is_workspace

    @typechecked
    @classmethod
    def get_workspace_settings_dict(cls, folderpath:str) -> ot.templates_types.TEMPLATE_WORKSPACE_TOML_DICT_TYPE:
        '''Returns the workspace's toml as a dictionary'''
        # The workspace toml file MUST be found in the folder
        workspace_toml_filepath= os.path.join(folderpath, cls.workspace_toml_filename)
        if not os.path.exists(workspace_toml_filepath):
            raise FileNotFoundError(f"ERROR! The Workpsace Toml File '{workspace_toml_filepath}' was does NOT exist!")
    

        # The workspace_toml file must be able to be read and validated
        toml_dict = t.cast(
            ot.templates_types.TEMPLATE_WORKSPACE_TOML_DICT_TYPE,
            General.get_toml_dict(
            workspace_toml_filepath, 
            expected_type=ot.templates_types.TEMPLATE_WORKSPACE_TOML_DICT_TYPE)
        )
        return toml_dict


    # @typechecked
    # @classmethod
    # def validate_is_workspace(cls,folderpath:str) -> None:
    #     '''Raises an error if the folder is NOT a workspace folder'''

    #     # The folderpath MUST exist
    #     if not os.path.exists(folderpath):
    #         raise ov_err.FolderExistsError(f"ERROR! The folder '{folderpath}' does NOT exist!")
        
    #     # Should be able to get workspace dict without errors
    #     _ = cls.get_workspace_settings_dict(folderpath)

    #     return None
        
    @typechecked
    @classmethod
    def initialize(
        cls, 
        folderpath:str = "./",
        id:str = str(uuid4()),
        workspace_name:str = "ov-templates",
        is_workspace_check: bool = True) -> None:
        '''
        Initializes a new templates workspace
        '''
        if is_workspace_check:
            raise NotImplementedError("ERROR! This feature has NOT been implemented yet")
            # The folderpath cannot already be a workspace folder
            # if cls.is_workspace(folderpath):
            #     raise File
        


        # Check if the folder is already present
        if not os.path
        os.mkdir(folderpath)

