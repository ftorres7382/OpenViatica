#
# Copyright 2026 ftorres7382
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.#

# Commented in case we need rust some day
# from . import _rs_core
from importlib import resources
from typeguard import typechecked
import typing as t
from ._general_core import General as G
import os
import uuid
import toml
from pathlib import Path

_package_path: Path = resources.files("OpenViatica")
_templates_path: Path = _package_path.joinpath("templates")
_venv_templates_path:Path = _templates_path.joinpath("venv_templates")
_dir_templates_path: Path = _templates_path.joinpath("directory_templates")

class ovutils:
    '''
    # ovutils
    This class is used to create and manage a data analysis workspace

    ## Import
    ```from OpenViatica import ovutils```

    ## Functions
    1. fibonacci(n: int) -> int
    2. fibonacci_rust(n:int) -> int
    '''
    
    class ws:
        '''
        # ovutils.ws
        Used for any workspace creation or management operation
        '''
        _workspace_metadata_dirname: str = ".openviatica"
        _workspace_base_metadata_filename:str = "workspace-metadata.toml"



        @staticmethod
        @typechecked
        def init(
            workspace_id:str | None = None, 
            workspace_name: str | None = None, 
            workspace_dirname:str | None = None,
            dirpath:str | None = None
            ) -> None:
            '''Initializes a new workspace'''
            # Standardize the path of the dirpath
            if dirpath is None:
                print("Defaulting to current working directory for initialization...")
                dirpath = os.getcwd()
            
            if workspace_id is None:
                workspace_id = str(uuid.uuid4())

            if workspace_name is None:
                workspace_name = "ov-workspace"
            
            if workspace_dirname is None:
                # Create a new directory in the dirpath
                workspace_dirname = workspace_name + "-" + workspace_id

            workspace_dirpath = os.path.join(dirpath, workspace_dirname)
            if os.path.exists(workspace_dirpath):
                raise FileExistsError(f"ERROR! The workspace '{workspace_dirpath}' already exists! Please set a new workspace id, name or change the existing workspace")
            
            metadata_dirpath = os.path.join(workspace_dirpath,ovutils.ws._workspace_metadata_dirname)
            base_metadata_filepath = os.path.join(metadata_dirpath,ovutils.ws._workspace_base_metadata_filename)
            # Create the directory
            os.mkdir(workspace_dirpath)

            # Create a workspace metadata folder
            os.mkdir(metadata_dirpath)

            # Create a metadata file in the folder
            base_workspace_metadata = {
                "id": workspace_id,
                "name": workspace_name,
            }
            with open(base_metadata_filepath, "w") as f:
                _ = toml.dump(base_workspace_metadata, f)
            
            # Copy the venv & directory templates in the folder
            workspace_venv_templates_dirpath = os.path.join(metadata_dirpath, os.path.basename(str(_venv_templates_path)))
            workspace_dir_templates_dirpath = os.path.join(metadata_dirpath, os.path.basename(str(_dir_templates_path)))


            work_zip = zip(
                [_venv_templates_path, _dir_templates_path],
                [workspace_venv_templates_dirpath, workspace_dir_templates_dirpath]
                
                )

            for src_templates_obj, dest_templates_dirpath in work_zip:
                G.copy_template_dir(src_templates_obj, dest_templates_dirpath)



            # Use uv to install 
            # breakpoint()

            
            # # Setup venv based on preset
            # python_path = G.get_python_interpreter_path()
            # og_cwd = os.getcwd()

            # # Change current working environment to set up the workspace
            # os.chdir(workspace_dirpath)

            # # Run uv commands to setup the workspace

            # # Reset current working environment
            # os.chdir(og_cwd)
            # breakpoint()
            
            out_dirpath = os.path.join(dirpath, workspace_dirname)
            print(f"\nSUCCESS! '{out_dirpath}' has been created!")


            
