
import os


from OpenViatica._types import ov_ws_types as ov_ws_t
from  OpenViatica._errors import ov_errors as ov_err 
from OpenViatica._general_core import General as G

from typeguard import typechecked
from jinja2 import Template
import typing as t
import shutil
import tomlkit
from pydantic import TypeAdapter
import json

DEFAULT_WORKSPACE_TOML_FILENAME = "workspace.toml"



class GenericWorkspaceService:
    WORKSPACE_TOML_TEMPLATE_RELPATH = "templates/toml_templates/generic_workspace/workspace.tmpl.toml"

    @classmethod
    @typechecked
    def initialize(
        cls,
        folderpath:str,
        workspace_metadata_path:str,
        workspace_toml_filename:str ,
        workspace_name: str,
        workspace_id: str,
        workspace_type: ov_ws_t.ws_type_t,

        _replace_toml_template_values: bool = True  
        ) -> None:
        '''Initializes a new Templates workspace'''
        
        # Standardize the path values
        folderpath = G.get_posix_path(folderpath)
        workspace_metadata_path = G.get_posix_path(workspace_metadata_path)

        # Check that the folder exists
        if not os.path.exists(folderpath):
            raise ov_err.FolderNotExistsError(f"The folder '{folderpath}' does NOT exist.")
        
        # The workspace metadata path must NOT exist
        if os.path.exists(workspace_metadata_path):
            raise ov_err.WorkspaceMetadataExistsError(f"Workspace metadata folder detected in '{workspace_metadata_path}'! The metadata folder must be removed to sucessfully initialize a new workspace.")

        # Create the workspace folder
        os.mkdir(workspace_metadata_path)

        # Now we can just create the toml file in the workspace folder
        cls.create_workspace_toml(
            folderpath=workspace_metadata_path,
            toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=workspace_type,

            _replace_template_values = _replace_toml_template_values
        )


    @classmethod
    @typechecked
    def create_workspace_toml(
        cls,
        folderpath:str,
        toml_filename:str,
        workspace_name:str,
        workspace_type: ov_ws_t.ws_type_t,
        workspace_id:str,

        _replace_template_values:bool = True
        ) -> None:
        '''Creates the required workspace toml file'''

        folderpath = G.get_posix_path(folderpath)
        
        # Validate that the folder exists
        if not os.path.exists(folderpath):
            raise ov_err.FolderExistsError(f"The folder '{folderpath}' does NOT exist!")
        
        # Validate that the toml file does NOT already exist
        toml_filepath = os.path.join(folderpath, toml_filename)
        if os.path.exists(toml_filepath):
            raise FileExistsError(f"The file '{toml_filepath}' ALREADY exists!")

        # Copy the workspace toml file
        with G.get_package_path() as pkg_path:
            generic_workspace_toml_path = os.path.join(
                pkg_path, cls.WORKSPACE_TOML_TEMPLATE_RELPATH
            )
            shutil.copy2(generic_workspace_toml_path, toml_filepath)
        
        # Read with tomlkit
        with open(toml_filepath, mode="rt") as f:
            doc = tomlkit.parse(f.read())
        
        # Change the values
        doc["id"] = workspace_id
        doc["name"] = workspace_name
        doc["type"] = workspace_type

        if _replace_template_values:
            # Replace all the relevant template values
            data = {
                "allowed_workspace_types": str(list(t.get_args(ov_ws_t.ws_type_t))),
                "schema_filepath": "./"+ toml_filename + ".schema.json"
            }
            template = Template(doc.as_string())
            toml_string = template.render(data)
        else:
            toml_string = doc.as_string()

        # Create the workspace toml
        with open(toml_filepath, 'w') as f:
            f.write(toml_string)

        # Create the sidecar schema json file
        schema_json_filepath = toml_filepath + ".schema.json"
        adapter = TypeAdapter(ov_ws_t.GENERIC_WORKSPACE_TOML_DICT_TYPE)
        schema = adapter.json_schema()

        with open(schema_json_filepath, "w") as f:
            json.dump(schema, f, indent=2)
        
        

class MetaWorkspaceService:
    '''
    Service class where all methods recieve the workspace folderpath.

    The methods can get information or transform the workspace in any way
    
    This service class handles a Meta workspace, a workspace of other workspaces
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
        '''Initializes a new meta workspace'''
        
        # Initialize a base workspace
        GenericWorkspaceService.initialize(
            folderpath=folderpath,
            workspace_metadata_path= workspace_metadata_path,
            workspace_toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=cls.WORKSPACE_TYPE,

            _replace_toml_template_values = False
        )

        # Now add the things needed for a meta workspace
        toml_filepath = os.path.join(workspace_metadata_path, workspace_toml_filename)
        # Read with tomlkit
        with open(toml_filepath, mode="rt") as f:
            doc = tomlkit.parse(f.read())
        
        # Add to the values
        self_entry_dict: ov_ws_t.WORKSPACE_TOML_LINK_DICT_TYPE  = {
            "id": str(doc["id"]),
            "name": str(doc["name"]),
            "type": cls.WORKSPACE_TYPE,
            "workspace_tomlpath": G.get_posix_path(os.path.abspath(toml_filepath))
        }
        doc["links_to"] = [self_entry_dict]

        # Replace all the relevant template values
        data = {
            "allowed_workspace_types": str([cls.WORKSPACE_TYPE]),
            "schema_filepath": "./"+ workspace_toml_filename + ".schema.json"
        }
        template = Template(doc.as_string())
        toml_string = template.render(data)

        # Create the workspace toml
        with open(toml_filepath, 'w') as f:
            f.write(toml_string)

        # Create the sidecar schema json file
        schema_json_filepath = toml_filepath + ".schema.json"
        adapter = TypeAdapter(ov_ws_t.META_WORKSPACE_TOML_DICT_TYPE)
        schema = adapter.json_schema()

        with open(schema_json_filepath, "w") as f:
            json.dump(schema, f, indent=2)

    # @classmethod
    # @typechecked
    # def link(
    #     cls,
    #     manager_workspace_toml_filepath:str,
    #     managed_workspace_toml_filepath:str
    # ) -> None:
    #     '''
    #     This function links one workspace with another.

    #     One workspace takes the manager role, able to pass arguments to the 
    #     This is reflected in the workspace tom of the manager and the managed being changed.

    #     '''
    #     # Clean the filepaths
    #     manager_workspace_toml_filepath = G.get_posix_path(manager_workspace_toml_filepath)
    #     managed_workspace_toml_filepath = G.get_posix_path(managed_workspace_toml_filepath)



    

class TemplatesWorkspaceService:
    '''
    Service class where all methods recieve the workspace folderpath.

    The methods can get information or transform the workspace in any way
    
    This service class handles a Templates workspace, a workspace of tempalate files and folders
    '''    
    DEFAULT_WORKSPACE_NAME:t.Final = "ov-templates"
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
        '''Initializes a new Tempaltes workspace'''
        
        # Initialize a base workspace
        GenericWorkspaceService.initialize(
            folderpath=folderpath,
            workspace_metadata_path= workspace_metadata_path,
            workspace_toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=cls.WORKSPACE_TYPE
        )
