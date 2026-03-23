import stat
from typing import Callable
from typeguard import typechecked
import sys
from pathlib import Path
from importlib.resources.abc import Traversable
import os
import glob
import time
import shutil
from importlib import resources

class General:
    '''Used for general functions in the package itself'''

    pkg_path: Traversable = resources.files("OpenViatica")
    pkg_templates_path: Traversable = pkg_path.joinpath("templates")
    
    workpsace_landing_dirname = ".openviatica" 
        




    @staticmethod
    @typechecked
    def vprint(value:object, verbose:bool = True) -> None:
        '''Verbose print, prints the value ONLY if verbose is True'''
        if verbose:
            print(value)
    
    @staticmethod
    @typechecked
    def get_python_interpreter_path() -> str:
        '''
        An easy way to get a python interpreter
        '''
        return sys.executable
    
    @staticmethod
    @typechecked
    def copy_template_dir(source: Traversable | Path, destination: str) -> None:
        """Recursively copies a Traversable directory to a physical path."""
        # Create the base destination folder if it doesn't exist
        os.makedirs(destination, exist_ok=True)

        for item in source.iterdir():
            dest_path = os.path.join(destination, item.name)
            
            if item.is_dir():
                # If it's a directory, recurse
                General.copy_template_dir(item, dest_path)
            else:
                # If it's a file, read bytes and write to disk
                with open(dest_path, "wb") as f:
                    _ = f.write(item.read_bytes())

    @staticmethod
    @typechecked
    def get_valid_input(
        prompt: str, 
        validation_function:Callable[[str], bool], 
        error_msg:str = "Invalid input. Try again.") -> str:
        '''
        This function will try to get the users input until the validator function returns a True on the userś input
        '''
        while True:
            user_input = input(prompt)

            # Use the validator function to determine if we have a valid input
            if validation_function(user_input):
                return user_input
            
            print(error_msg)

    # This validator function could be used a lot
    @staticmethod
    @typechecked
    def y_n_valdiator_function(user_input:str, default_empty_value:str = "n") -> bool:
        if user_input == "":
            user_input = default_empty_value
        return (user_input.lower() == "y") or (user_input.lower() == "n")

    @classmethod
    @typechecked
    def reset_dir(cls, dirpath:str, ask_dir_cleanup:bool = True) -> None:
        '''
        This function is responsible for deleting all items in the currnt folder in a safe way
        '''
        # Go through whole confirmation process & clean directory
        deletion_listing = glob.glob(os.path.join(dirpath, "*"), include_hidden=True)
        
        file_len = 0
        directory_len = 0
        for path in deletion_listing:
            if os.path.isdir(path):
                directory_len += 1
            elif os.path.isfile(path):
                file_len += 1
            
        if ask_dir_cleanup and len(deletion_listing) != 0:
            print(f"\nDeleting ALL Files and Folders in '{dirpath}'")
            answer = cls.get_valid_input(
                f"\nDELETING {file_len} files and {directory_len} folders in '{dirpath}'. Confirm action? (y/N)",
                cls.y_n_valdiator_function
            ).lower()
            if answer == "" or answer == "n":
                print("Aborting initialization...")
                time.sleep(2.5)
                return
            
            # If the answer was yes we ask again to confrim
            answer = cls.get_valid_input(
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