
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



class BaseWorkspaceService:
    WORKSPACE_TOML_TEMPLATE_RELPATH = "templates/toml_templates/base_workspace/workspace.tmpl.toml"
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

        # Copy the workspace toml file
        with G.get_package_path() as pkg_path:
            base_workspace_toml_path = os.path.join(
                pkg_path, cls.WORKSPACE_TOML_TEMPLATE_RELPATH
            )
            shutil.copy2(base_workspace_toml_path, toml_filepath)
        
        # Read with tomlkit
        with open(toml_filepath, mode="rt") as f:
            doc = tomlkit.parse(f.read())
        
        # Change the values
        doc["id"] = workspace_id
        doc["name"] = workspace_name
        doc["type"] = workspace_type

        # Replace all the relevant template values
        data = {
            "allowed_workspace_types": str(list(t.get_args(ov_ws_t.ws_type_t))),
            "schema_filepath": "./"+ toml_filename + ".schema.json"
        }
        template = Template(doc.as_string())
        toml_string = template.render(data)

        # Create the workspace toml
        with open(toml_filepath, 'w') as f:
            f.write(toml_string)

        # Create the sidecar schema json file
        schema_json_filepath = toml_filepath + ".schema.json"
        adapter = TypeAdapter(ov_ws_t.BASE_WORKSPACE_TOML_DICT_TYPE)
        schema = adapter.json_schema()

        with open(schema_json_filepath, "w") as f:
            json.dump(schema, f, indent=2)
        
        

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
            raise ov_err.FolderNotExistsError(f"The folder '{folderpath}' does NOT exist.")
        
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

