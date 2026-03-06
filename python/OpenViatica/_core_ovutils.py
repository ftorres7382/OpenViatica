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
        _ws_templates_library_relpath = os.path.join(_workspace_metadata_dirname, "workspace_template_library")
        

        @staticmethod
        @typechecked
        def init(
            workspace_id:str | None = None, 
            workspace_name: str | None = None,
            create_new_directory:bool = False, # Controls whether a new directory will be created or if the current one will be reused 
            uuid_dirname:bool = False,
            ask_dir_cleanup: bool = True, # When new_dir is False, it will ask for confirmation on directory cleanup
            dirpath:str | None = None,
            workspace_dirname:str | None = None, # Only used if the 
            ) -> None:
            '''
            # init
            Initializes a new OpenViatica Workspace

            When new_dir is True, it will create a new directory in "dir_path" with the same name as "workspace_dirname"

            When new_dir is False, it will try to create a fresh workspace in "dir_path"
            It will ask the user to confirm the cleanup actions twice unless "ask_dir_cleanup" is False
            
            '''

            #################################
            # Standardize values
            #################################
            # region

            # Standardize the path of the dirpath
            if dirpath is None:
                print("Defaulting to current working directory for initialization...")
                dirpath = os.getcwd()
            
            if workspace_id is None:
                workspace_id = str(uuid.uuid4())

            if workspace_name is None:
                workspace_name = "ov-workspace"
            
            # If the user did not provide a dirname value, we must define one
            if workspace_dirname is None:
                workspace_dirname = workspace_name
                if uuid_dirname:
                    workspace_dirname += "-" + str(uuid.uuid4())

            # If the dirname has been sent but we are not going to use it, print a warning
            else:
                if not create_new_directory:
                    print("WARNING! 'workspace_dirname' detected, but 'create_new_directory' is turned off.")
                    print("'workspace_dirname' will not be used...\n")
                    time.sleep(2.5)

            # If create_new_dir is False, then the workspace directory is the dirpath, 
            # if not, it is the dirpath and workspace_dirname            
            if not create_new_directory:
                workspace_dirpath = dirpath
            else:
                # Set the workspace dirpath 
                workspace_dirpath = os.path.join(dirpath, workspace_dirname)

                # Take away slash if present
                if workspace_dirpath[-1] == "/":
                    workspace_dirpath = workspace_dirpath[:-1]
                
                # If it already exists keep adding numbers until a good path is found
                i = 0
                while os.path.exists(workspace_dirpath):
                    old_i = i
                    i+=1
                    if i == 1:
                        # Add a dash since the number will be separated by the dash
                        workspace_dirpath += f"-{i}"
                        continue

                    # If here then we still need to find a good workspace names
                    temp_dirname = os.path.dirname(workspace_dirpath)
                    temp_basename = os.path.basename(workspace_dirpath)
                    temp_basename = temp_basename.replace(str(old_i), str(i))

                    workspace_dirpath = os.path.join(temp_dirname, temp_basename)
                    
            # endregion

            #################################
            # Initialize workspace directory
            #################################
            # region

            print(f"Initializing workspace in '{workspace_dirpath}'...")
            if not create_new_directory:
                # Go through whole confirmation process & clean directory
                deletion_listing = glob.glob(os.path.join(workspace_dirpath, "*"), include_hidden=True)
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
                        return
                    
                    # If the answer was yes we ask again to confrim
                    answer = G.get_valid_input(
                        "This action is IRREVERSIBLE. Type 'DELETE' to continue: ",
                        lambda x: True
                    )
                    if answer != "DELETE":
                        print("Aborting initialization...")
                        time.sleep(2.5)
                        return
                    
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

            # endregion

            #################################
            # Copy out all templates to the workspace
            #   This way the have one place where new templates could be configured by the user later on, but they already com equipped with the minimum amount necessary
            #################################
            # region

            metadata_dirpath = os.path.join(workspace_dirpath,ovutils.ws._workspace_metadata_dirname)
            base_metadata_filepath = os.path.join(metadata_dirpath,ovutils.ws._workspace_base_metadata_filename)
            

            # Create a workspace metadata folder
            # if it already exists, it should abort
            if os.path.exists(metadata_dirpath):
                print(f"\nERROR! The directory '{metadata_dirpath}' already exists!")
                time.sleep(1)
                print("ABORTING Initialization ...")
                time.sleep(2.5)
                return

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

            # endregion

            # Change cwd to the workspace directory
            og_cwd = os.getcwd()
            os.chdir(workspace_dirpath)

            #################################
            # Use the existing ws tools to implement directories and files configuration
            #################################
            # region

            

            # endregion
            
            
            print(f"\nSUCCESS! The OpenViatica workspace has been created in '{workspace_dirpath}'!")

        @staticmethod
        @typechecked
        def clone_template(rel_template_path:str) -> None:
            '''
            # clone_template
            This function will look in the workspace template library and clone a template
            
            It has several configurations
            Single directory, no .ov-tmpl.toml file: A default .ov-tmpl.toml file will be created in the directory
            Single Directory, does have .ov-tmpl.toml: Uses the config to determine contents of the folder

            Single Directory where the payload is a single file
            '''


            
