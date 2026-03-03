from typeguard import typechecked
import sys
from pathlib import Path

import os
import typing as t

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
    def copy_template_dir(source: Path, destination: str) -> None:
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