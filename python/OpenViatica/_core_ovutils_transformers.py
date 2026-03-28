
import os
from uuid import uuid4
from OpenViatica._general_core import General


from ._types import ovutils_types as ot
from  ._errors import ov_errors as ov_err 
import typing as t

from typeguard import typechecked


class ovutils_transformers:
    '''
    Internal class that mirrors ovutils classes, except these are all JUST transformer classes
    '''
    workspace_toml_filename:str = ".openviatica.toml"

    @classmethod
    @typechecked
    def validate_is_workspace(cls, folderpath:str = "./") -> None:
        '''Validates that it is openviatica workspace'''

        # Folder must exist
        if not os.path.exists(folderpath):
            raise ov_err.FolderNotFoundError(f"ERROR! The folder '{folderpath}' does NOT exist!")
        
        # workspace toml file MUST exist
        if not os.path.




    @classmethod
    @typechecked
    def initialize(cls,folderpath:str) -> None:
        '''Initializes a new openviatica workspace'''





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

