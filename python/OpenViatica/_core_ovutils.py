# #
# # Copyright 2026 ftorres7382
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.#


# # from typeguard import typechecked
# # from ._general_core import General as G

# import os
# from uuid import uuid4
# # import uuid
# from OpenViatica._general_core import General
# # from importlib.resources.abc import Traversable
# # import time

# # from pathlib import Path

# from ._types import ovutils_types as ot
# from  ._errors import ov_errors as ov_err 
# import typing as t

# from typeguard import typechecked


# class ovutils:
#     '''
#     # ovutils
#     This class is used to create and manage a data analysis workspace

#     ## Import
#     ```from OpenViatica import ovutils```

#     ## Functions
#     1. fibonacci(n: int) -> int
#     2. fibonacci_rust(n:int) -> int
#     '''
#     workpsace_landing_dirname = ".openviatica" 
    
#     # class workspace:
#     #     '''
#     #     # ovutils.workspace
#     #     Used for the creation or management of any OpenViatica workspace
#     #     '''
#     #     _pkg_venv_templates_path:Traversable = G.pkg_templates_path.joinpath("venv_templates")
#     #     _pkg_ws_templates_library_path: Traversable = G.pkg_templates_path.joinpath("workspace_template_library")
        
#     #     _ws_metadata_dirname: str = ".ov-workspace"
        
#     #     _ws_templates_library_relpath = os.path.join(_ws_metadata_dirname, "workspace_template_library")
        
#     #     # CHANGE THE ws SO THAT IT IS A HELPER CLASS
#     #     # IT SHOULD HAVE AN INTERNAL DIRPATH!
#     #     @classmethod
#     #     @typechecked
#     #     def init(
#     #         cls,
#     #         workspace_id:str | None = None, 
#     #         workspace_name: str | None = None,
#     #         create_new_directory:bool = False, # Controls whether a new directory will be created or if the current one will be reused 
#     #         uuid_dirname:bool = False,
#     #         ask_dir_cleanup: bool = True, # When new_dir is False, it will ask for confirmation on directory cleanup
#     #         dirpath:str | None = None,
#     #         workspace_dirname:str | None = None, # Only used if the 
#     #         ) -> None:
#     #         '''
#     #         # init
#     #         Initializes a new OpenViatica Workspace

#     #         When new_dir is True, it will create a new directory in "dir_path" with the same name as "workspace_dirname"

#     #         When new_dir is False, it will try to create a fresh workspace in "dir_path"
#     #         It will ask the user to confirm the cleanup actions twice unless "ask_dir_cleanup" is False
            
#     #         '''

#     #         #################################
#     #         # Standardize values
#     #         #################################
#     #         # region

#     #         # Standardize the path of the dirpath
#     #         if dirpath is None:
#     #             print("Defaulting to current working directory for initialization...")
#     #             dirpath = os.getcwd()
            
#     #         if workspace_id is None:
#     #             workspace_id = str(uuid.uuid4())

#     #         if workspace_name is None:
#     #             workspace_name = "ov-workspace"
            
#     #         # If the user did not provide a dirname value, we must define one
#     #         if workspace_dirname is None:
#     #             workspace_dirname = workspace_name
#     #             if uuid_dirname:
#     #                 workspace_dirname += "-" + str(uuid.uuid4())

#     #         # If the dirname has been sent but we are not going to use it, print a warning
#     #         else:
#     #             if not create_new_directory:
#     #                 print("WARNING! 'workspace_dirname' detected, but 'create_new_directory' is turned off.")
#     #                 print("'workspace_dirname' will not be used...\n")
#     #                 time.sleep(2.5)

#     #         # If create_new_dir is False, then the workspace directory is the dirpath, 
#     #         # if not, it is the dirpath and workspace_dirname            
#     #         if not create_new_directory:
#     #             workspace_dirpath = dirpath
#     #         else:
#     #             # Set the workspace dirpath 
#     #             workspace_dirpath = os.path.join(dirpath, workspace_dirname)

#     #             # Take away slash if present
#     #             if workspace_dirpath[-1] == "/":
#     #                 workspace_dirpath = workspace_dirpath[:-1]
                
#     #             # If it already exists keep adding numbers until a good path is found
#     #             i = 0
#     #             while os.path.exists(workspace_dirpath):
#     #                 old_i = i
#     #                 i+=1
#     #                 if i == 1:
#     #                     # Add a dash since the number will be separated by the dash
#     #                     workspace_dirpath += f"-{i}"
#     #                     continue

#     #                 # If here then we still need to find a good workspace names
#     #                 temp_dirname = os.path.dirname(workspace_dirpath)
#     #                 temp_basename = os.path.basename(workspace_dirpath)
#     #                 temp_basename = temp_basename.replace(str(old_i), str(i))

#     #                 workspace_dirpath = os.path.join(temp_dirname, temp_basename)
                    
#     #         # endregion

#     #         #################################
#     #         # Initialize workspace directory
#     #         #################################
#     #         # region

#     #         print(f"Initializing workspace in '{workspace_dirpath}'...")
#     #         if not create_new_directory:
#     #             G.reset_dir(dirpath=workspace_dirpath, ask_dir_cleanup=ask_dir_cleanup)
#     #         else:
#     #             # Create the directory
#     #             os.mkdir(workspace_dirpath)

#     #         # endregion

#     #         #################################
#     #         # Create workspace metadata
#     #         #################################
#     #         # region

#     #         metadata_dirpath = os.path.join(workspace_dirpath,cls._ws_metadata_dirname)
#     #         base_metadata_filepath = os.path.join(metadata_dirpath,cls._ws_base_metadata_filename)
            

#     #         # Create a workspace metadata folder
#     #         # if it already exists, it should abort
#     #         if os.path.exists(metadata_dirpath):
#     #             print(f"\nERROR! The directory '{metadata_dirpath}' already exists!")
#     #             time.sleep(1)
#     #             print("ABORTING Initialization ...")
#     #             time.sleep(2.5)
#     #             return

#     #         os.mkdir(metadata_dirpath)

#     #         # Create a metadata file in the folder
#     #         base_workspace_metadata = {
#     #             "id": workspace_id,
#     #             "name": workspace_name,
#     #         }
#     #         with open(base_metadata_filepath, "w") as f:
#     #             _ = toml.dump(base_workspace_metadata, f)

#     #         # Initialize a templates workspace
#     #         ws_templates_dirpath = os.path.join(metadata_dirpath, os.path.basename(str(cls._pkg_ws_templates_library_path)))
#     #         os.mkdir(ws_templates_dirpath)
#     #         ovutils.templates.init(ws_templates_dirpath)
            
#     #         # # Copy the venv & directory templates in the folder
            
#     #         # workspace_venv_templates_dirpath = os.path.join(workspace_dir_templates_dirpath, os.path.basename(str(cls._pkg_venv_templates_path)))
            


#     #         # work_zip = zip(
#     #         #     [cls._pkg_venv_templates_path, cls._pkg_ws_templates_library_path],
#     #         #     [workspace_venv_templates_dirpath, workspace_dir_templates_dirpath]
                
#     #         #     )

#     #         # for src_templates_obj, dest_templates_dirpath in work_zip:
#     #         #     G.copy_template_dir(src_templates_obj, dest_templates_dirpath)

#     #         # endregion

#     #         # Change cwd to the workspace directory
#     #         og_cwd = os.getcwd()
#     #         os.chdir(workspace_dirpath)

#     #         #################################
#     #         # Use the existing ws tools to implement directories and files configuration
#     #         #################################
#     #         # region

            

#     #         # endregion
            
            
#     #         print(f"\nSUCCESS! The OpenViatica workspace has been created in '{workspace_dirpath}'!")



    



#     # class templates:
#     #     '''
#     #     # ovutils templates
#     #     The purpose of this module is to manage create & manage a templates workspace.
#     #     '''
#     #     workspace_toml_filename = ".ov-templates.toml"

#     #     def __init__(
#     #         self, 
#     #         workspace_dirpath: str = os.path.join(G.workpsace_landing_dirname, ".ov-templates")
#     #         ) -> None:
#     #         '''
#     #         Initializes a configured template transformer object
#     #         '''
#     #         self.workspace_dirpath:str
#     #         self.workspace_toml_path:str


#     #         self.workspace_dirpath = workspace_dirpath
#     #         self.workspace_toml_path = os.path.join(self.workspace_dirpath, self.workspace_toml_filename)

#     #     @typechecked
#     #     def init_workspace(self, 
#     #     workspace_id:str | None = None, 
#     #     workspace_name: str | None = None
#     #     ) -> None:
#     #         '''
#     #         Initializes a new OpenViatica Templates Workspace

#     #         A Templates workspace is currently defined as a folder that has a toml file
#     #         The toml file MUSt contain a name and an ID
#     #         '''
#     #         Path(self.workspace_dirpath).mkdir(parents=True, exist_ok=True)
            
#     #         if workspace_id is None:
#     #             workspace_id = str(uuid.uuid4())
            
#     #         if workspace_name is None:
#     #             # If the user did not define the workspace name, then use the standard dirname
#     #             workspace_name = os.path.basename(self.dirpath)
            

#     #         # Check if one already exists in the directory
#     #         if os.path.exists(self.metadata_dirpath):
#     #             raise FileExistsError(
#     #                 "ERROR! A templates workspace has already been initialized! "+
#     #                 f"To initialize a new templates workspace, remove '{self.metadata_dirpath}'"
#     #                 )
                
#     #         # If here, we can create the directory
#     #         os.mkdir(self.metadata_dirpath)

#     #         # Create the workspace metadata
#     #         base_metadata_filepath = os.path.join(self.metadata_dirpath, ovutils._base_metadata_filename)
#     #         base_workspace_metadata: ovutils_types.templates_types.BASE_METADATA_DICT = {
#     #             "id": workspace_id,
#     #             "name": workspace_name,
#     #         }
#     #         with open(base_metadata_filepath, "w") as f:
#     #             _ = toml.dump(base_workspace_metadata, f)
#     #         print("\nSUCCESS! An OpenViatica TEMPLATES workspace has been created! The metadata will be stored in ")

#     #     @typechecked
#     #     @classmethod
#     #     def is_workspace(cls, dirpath:str) -> bool:
#     #         '''Returns true if the dirpath fufills the requirements to be determined as a Templates Workspace'''
#     #         # Set as a classmethod since this is to get information about a possible workspace
#     #         # If we were sure it was a workspace, we would require an object to be created instead

#     #         return True


#         # @typechecked
#         # def add(self, 
#         #         src_path:str,
#         #         config_toml_path : str | None = None,
#         #         name: str | None = None,
#         #         description: str | None = None,
#         #         version: str | None = None,
#         #         out_name: str | None = None,
#         #         force_directory: str | None = None,
#         #         preserve_permissions: bool = True,
#         #         ignore_list: t.List[str] = []                
#         # ) -> None:
#         #     '''
#         #     Adds a template to the templates directory
#         #     '''

#         #     ###############################
#         #     # Set default values to all variables
#         #     ###############################
#         #     # region

#         #     if not os.path.exists(src_path):
#         #         raise FileNotFoundError(f"ERROR! The file/folder '{src_path}' does NOT EXIST!")
            
#         #     # We start with the config file
#         #     if config_toml_path is None:
#         #         # If the src path is a directory, then check for the default name for the template toml file
#         #         if os.path.isdir(src_path):
#         #             config_toml_path = os.path.join(src_path,self._default_template_config_filename)
#         #         # Else we assume a sidecar file situation
#         #         else:
#         #             config_toml_path = os.path.basename(src_path)

            
#         #     # Perform checks on the toml file 
#         #     # if not os.path.exists(toml


#         #     # endregion


#         #     ".template.toml"
#         #     '''
#         #     # The name of the template when it is accessed
#         #     name = "{basename}"

#         #     # Description of the template
#         #     description = ""

#         #     # Template Version
#         #     version = ""

#         #     # The name of the file/folder when it is cloned
#         #     out_name = name

#         #     # Any way I can automatically detect if the user wants the whole template to be a single file or not?

#         #     # Whether or not to preserve permissions
#         #     preserve_persmissions = True

#         #     ignore = [

#         #     ]


            
#         #     src path can be folder or file
#         #         If it is a folder
#         #             If the flag is turned on, use the config file in the directory 
                
#         #     '''

            
#         #     names
#         #     default output_name

            



# '''
# Lets walk this through

# User initializes DATA workspace
#     metadata folder is created
#     route for the metadata folder is created
#     workpsace-environment "main" is created
#         "main" is filled with all the default stuff
#             This would be default templates & default data things (catalogs, db, tables, metadata to any of these)
#     I could work directly in main
#     If I wanted a new metadata environment, I could do ovutils ws env init env2

# ALL tools will have this environment switching capability

# We will do workspace as a project model, where the pyproject.toml will be used to designate the workspace
# s
# '''

 
            
