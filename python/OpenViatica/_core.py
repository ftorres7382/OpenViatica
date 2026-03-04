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
from ntpath import isdir, isfile
from typeguard import typechecked
from ._general_core import General as G
import os
import uuid
import toml
from importlib.resources.abc import Traversable
import glob
import time
import shutil

_package_path: Traversable = resources.files("OpenViatica")
_templates_path: Traversable = _package_path.joinpath("templates")
_venv_templates_path:Traversable = _templates_path.joinpath("venv_templates")
_dir_templates_path: Traversable = _templates_path.joinpath("directory_templates")

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
            create_new_directory:bool = False, # Controls whether a new directory will be created or if the current one will be reused 
            ask_dir_cleanup: bool = True, # When new_dir is False, it will ask for confirmation on directory cleanup
            dirpath:str | None = None,
            workspace_dirname:str | None = None, # Only used if the 
            ) -> None:
            '''
            # init
            Initializes a new OpenViatica Workspace

            # Arguments
            1. 

            When new_dir is True, it will create a new directory in "dir_path" with the same name as "workspace_dirname"

            When new_dir is False, it will try to create a fresh workspace in "dir_path"
            It will ask the user to confirm the cleanup actions twice unless "ask_dir_cleanup" is False
            
            '''
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
            
            # If create_new_dir is False, then the workspace directory is the dirpath, 
            # if not, it is the dirpath and workspace_dirname            
            if not create_new_directory:
                workspace_dirpath = dirpath
            else:
                workspace_dirpath = os.path.join(dirpath, workspace_dirname)
                # Since we ARE supposed to create a new directory, one cannot already exist
                if os.path.exists(workspace_dirpath):
                    raise FileExistsError(f"ERROR! The workspace '{workspace_dirpath}' already exists! Please set a new workspace id, name or change the existing workspace")
            breakpoint()
            print(f"Initializing workspace in '{workspace_dirpath}'...")
            if not create_new_directory:
                # Go through whole confirmation process & clean directory
                deletion_listing = glob.glob(os.path.join(workspace_dirpath, "*"))
                if ask_dir_cleanup and len(deletion_listing) != 0:
                    print(f"\nDeleting ALL Files and Folders in '{workspace_dirpath}'")
                    print("To initialize on a NEW directory instead, set 'create_new_directory' to True")
                    answer = G.get_valid_input(
                        f"\nDELETING {len(deletion_listing)} files or folders in '{workspace_dirpath}'. Confirm action? (y/N)",
                        G.y_n_valdiator_function
                    ).lower()
                    if answer == "" or answer == "n":
                        print("Aborting initialization...")
                        time.sleep(2.5)
                        exit(0)
                    
                    # If the answer was yes we ask again to confrim
                    answer = G.get_valid_input(
                        "This action is IRREVERSIBLE. Type 'DELETE' to continue: ",
                        lambda x: True
                    )
                    if answer != "DELETE":
                        print("Aborting initialization...")
                        time.sleep(2.5)
                        exit(0)
                    
                    # We are clear to delete all the folders and files
                    first_iteration = True
                    for delete_path in deletion_listing:
                        print(f"Deleting '{delete_path}'...")
                        
                        if first_iteration:
                            # give the user time to back out
                            time.sleep(3)
                            first_iteration = False
                        
                        if os.path.isfile(delete_path):
                            os.remove(delete_path)
                        elif os.path.isdir(delete_path):
                            shutil.rmtree(delete_path)
                        else:
                            raise NotImplementedError(f"ERROR! The deletion of a path with the same type as '{delete_path}' has NOT been implemented yet!")
            else:
                # Create the directory
                os.mkdir(workspace_dirpath)
            breakpoint()

            metadata_dirpath = os.path.join(workspace_dirpath,ovutils.ws._workspace_metadata_dirname)
            base_metadata_filepath = os.path.join(metadata_dirpath,ovutils.ws._workspace_base_metadata_filename)
            

            # Create a workspace metadata folder
            # It will automatically raise an error if the directory already exists
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


            
