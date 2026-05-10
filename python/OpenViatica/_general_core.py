from tomlkit.toml_document import TOMLDocument
from OpenViatica._errors import ov_errors as ov_err
import tomlkit
from typeguard import typechecked
import sys
from pathlib import Path
from importlib.resources.abc import Traversable
import os
import glob
import time
import shutil
from importlib import resources
from OpenViatica._types import ov_ws_types as ov_ws_t
import toml
import typing as t
from pydantic import TypeAdapter
from contextlib import contextmanager


class General:
    """Used for general functions in the package itself"""

    pkg_path: Traversable = resources.files("OpenViatica")

    @staticmethod
    @typechecked
    def get_posix_path(path: str) -> str:
        """Returns the posix representation of the path"""
        return Path(path).as_posix()

    @staticmethod
    @contextmanager
    def get_package_path() -> t.Generator[str, None, None]:
        with resources.as_file(General.pkg_path) as pkg_path:
            yield pkg_path.as_posix()
            pass

    @staticmethod
    @typechecked
    def vprint(value: object, verbose: bool = True) -> None:
        """Verbose print, prints the value ONLY if verbose is True"""
        if verbose:
            print(value)

    @staticmethod
    @typechecked
    def get_python_interpreter_path() -> str:
        """
        An easy way to get a python interpreter
        """
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
        validation_function: t.Callable[[str], bool],
        error_msg: str = "Invalid input. Try again.",
    ) -> str:
        """
        This function will try to get the users input until the validator function returns a True on the userś input
        """
        while True:
            user_input = input(prompt)

            # Use the validator function to determine if we have a valid input
            if validation_function(user_input):
                return user_input

            print(error_msg)

    @staticmethod
    @typechecked
    def read_toml_dict(
        toml_filepath: str,
        expected_type: t.Type[ov_ws_t.ANY_TYPE_DEF_TYPE] | None = None,
    ) -> t.Dict[t.Any, t.Any] | ov_ws_t.ANY_TYPE_DEF_TYPE:
        """
        This function returns the toml file as a dictionary.

        If the expected_type is defined, it will be validated using pydantic
        """
        # Check for file
        if not os.path.exists(toml_filepath):
            raise FileExistsError(f"The toml file '{toml_filepath}' does NOT exist!")

        # Read the toml
        validated_result_dict: t.Dict[t.Any, t.Any] | ov_ws_t.ANY_TYPE_DEF_TYPE
        with open(toml_filepath, "r") as f:
            validated_result_dict = toml.load(f)

        if expected_type is not None:
            adapter = TypeAdapter(expected_type)
            validated_result_dict = adapter.validate_python(validated_result_dict)

        return validated_result_dict

    @staticmethod
    @typechecked
    def read_toml_doc(
        toml_filepath: str,
        expected_type: t.Type[ov_ws_t.ANY_TYPE_DEF_TYPE] | None = None,
    ) -> TOMLDocument:
        """
        This function returns the toml file as a dictionary.

        If the expected_type is defined, it will be validated using pydantic
        """
        # Check for file
        if not os.path.exists(toml_filepath):
            raise FileExistsError(f"The toml file '{toml_filepath}' does NOT exist!")

        # Read the toml
        with open(toml_filepath, "r") as f:
            doc = tomlkit.load(f)

        # Validate the dictionary
        if expected_type is not None:
            toml_dict = doc.unwrap()
            adapter = TypeAdapter(expected_type)
            _ = adapter.validate_python(toml_dict)

        return doc

    # This validator function could be used a lot
    @staticmethod
    @typechecked
    def y_n_valdiator_function(user_input: str, default_empty_value: str = "n") -> bool:
        if user_input == "":
            user_input = default_empty_value
        return (user_input.lower() == "y") or (user_input.lower() == "n")

    @classmethod
    @typechecked
    def reset_dir(cls, dirpath: str, ask_dir_cleanup: bool = True) -> None:
        """
        This function is responsible for deleting all items in the current folder in a safe way
        """
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
                cls.y_n_valdiator_function,
            ).lower()
            if answer == "" or answer == "n":
                print("Aborting initialization...")
                time.sleep(2.5)
                return

            # If the answer was yes we ask again to confrim
            answer = cls.get_valid_input(
                "This action is IRREVERSIBLE. Type 'DELETE' to continue: ",
                lambda x: True,
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
                raise NotImplementedError(
                    f"The deletion of a path with the same type as '{delete_path}' has NOT been implemented yet!"
                )

    @classmethod
    @typechecked
    def check_file_exists(cls, filepath: str) -> None:
        """Raises and error if a folder does NOT exist"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"The file '{filepath}' does NOT exist. The file must be created to continue."
            )

    @classmethod
    @typechecked
    def check_folder_exists(cls, folderpath: str) -> None:
        """Raises and error if a folder does NOT exist"""
        if not os.path.exists(folderpath):
            raise ov_err.FolderNotExistsError(
                f"The folder '{folderpath}' does NOT exist. The folder must be created to continue."
            )

    @classmethod
    @typechecked
    def check_folder_NOT_exists(cls, folderpath: str) -> None:
        """Raises and error if a folder does NOT exist"""
        if os.path.exists(folderpath):
            raise ov_err.FolderExistsError(
                f"The folder '{folderpath}' already exists. The folder must be removed to continue."
            )

    @classmethod
    @typechecked
    def concatenate_file_contents(
        cls, filepaths_list: t.List[str], output_filepath: str
    ) -> None:
        """This function concatenates the contents of the files defined and outputs the final results to the output filepath"""
        # Write everything to a temp file
        tmp_output_filepath = cls.get_posix_path(output_filepath) + "._tmp"
        with open(tmp_output_filepath, "wb") as dst:
            for filepath in filepaths_list:
                posix_filepath = cls.get_posix_path(filepath)
                with open(posix_filepath, "rb") as src:
                    shutil.copyfileobj(src, dst)

        # Remove original if present
        if os.path.exists(output_filepath):
            os.remove(output_filepath)

        # Rename tmp
        os.rename(tmp_output_filepath, output_filepath)

    @classmethod
    @typechecked
    def get_typed_dict_keys(
        cls, typed_dict: t.Type[t.Mapping[str, t.Any]]
    ) -> list[str]:
        return list(t.get_type_hints(typed_dict).keys())

    @classmethod
    @typechecked
    def get_immediate_folders(cls, parent_dir: str) -> list[str]:
        return [f.name for f in os.scandir(parent_dir) if f.is_dir()]
