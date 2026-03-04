from turtle import Turtle
from typing import Callable
from typeguard import typechecked
import sys
from pathlib import Path
from importlib.resources.abc import Traversable
import os

class General:
    '''Used for general functions in the package itself'''
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