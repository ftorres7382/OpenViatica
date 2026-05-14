import os
from tomlkit.items import AoT


from OpenViatica._types import ov_ws_types
from OpenViatica._types import WORKSPACE_DEFAULT_METADATA_INFO_DICT_TYPE
from OpenViatica._errors import ov_errors as ov_err
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
    WORKSPACE_TOML_TEMPLATE_RELPATH = (
        "templates/toml_templates/generic_workspace/workspace.tmpl.toml"
    )

    @classmethod
    @typechecked
    def initialize(
        cls,
        folderpath: str,
        workspace_metadata_path: str,
        workspace_toml_filename: str,
        workspace_name: str,
        workspace_id: str,
        workspace_type: ov_ws_types.ws_type_t,
        _replace_toml_template_values: bool = True,
    ) -> str:
        """
        Initializes a new Templates workspace

        Returns the workspace toml filpath
        """

        # Standardize the path values
        folderpath = G.get_posix_path(folderpath)
        workspace_metadata_path = G.get_posix_path(workspace_metadata_path)

        # Check that the folder exists
        if not os.path.exists(folderpath):
            os.mkdir(folderpath)

        # The workspace metadata path must NOT exist
        if os.path.exists(workspace_metadata_path):
            raise ov_err.WorkspaceMetadataExistsError(
                f"Workspace metadata folder detected in '{workspace_metadata_path}'! The metadata folder must be removed to sucessfully initialize a new workspace."
            )

        # Create the workspace folder
        os.mkdir(workspace_metadata_path)

        # Now we can just create the toml file in the workspace folder
        workspace_toml_filepath = cls.create_workspace_toml(
            folderpath=workspace_metadata_path,
            toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=workspace_type,
            _replace_template_values=_replace_toml_template_values,
        )
        return workspace_toml_filepath

    @classmethod
    @typechecked
    def create_workspace_toml(
        cls,
        folderpath: str,
        toml_filename: str,
        workspace_name: str,
        workspace_type: ov_ws_types.ws_type_t,
        workspace_id: str,
        _replace_template_values: bool = True,
    ) -> str:
        """
        Creates the required workspace toml file

        Returns the woprkspace toml filepath
        """

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
                "allowed_workspace_types": str(list(t.get_args(ov_ws_types.ws_type_t))),
                "schema_filepath": "./" + toml_filename + ".schema.json",
            }
            template = Template(doc.as_string())
            toml_string = template.render(data)
        else:
            toml_string = doc.as_string()

        # Create the workspace toml
        with open(toml_filepath, "w") as f:
            f.write(toml_string)

        # Create the sidecar schema json file
        schema_json_filepath = toml_filepath + ".schema.json"
        adapter = TypeAdapter(ov_ws_types.GENERIC_WORKSPACE_TOML_DICT_TYPE)
        schema = adapter.json_schema()

        with open(schema_json_filepath, "w") as f:
            json.dump(schema, f, indent=2)
        return toml_filepath


class MetaWorkspaceService:
    """
    Service class where all methods recieve the workspace folderpath.

    The methods can get information or transform the workspace in any way

    This service class handles a Meta workspace, a workspace of other workspaces
    """

    WORKSPACE_TOML_TEMPLATE_RELPATH = (
        "templates/toml_templates/meta_workspace/workspace.tmpl.toml"
    )

    DEFAULT_WORKSPACE_PATH: t.Final[str] = "./"

    DEFAULT_WORKSPACE_NAME: t.Final = "ov-meta"
    DEFAULT_METADATA_FOLDERPATH: t.Final = "." + DEFAULT_WORKSPACE_NAME

    WORKSPACE_TYPE: t.Final[t.Literal["ov-meta"]] = DEFAULT_WORKSPACE_NAME

    @classmethod
    @typechecked
    def initialize(
        cls,
        folderpath: str,
        workspace_metadata_path: str,
        workspace_toml_filename: str,
        workspace_name: str,
        workspace_id: str,
    ) -> str:
        """
        Initializes a new meta workspace

        Returns the wrokspace toml filepath
        """

        # Initialize a base workspace
        toml_filepath = GenericWorkspaceService.initialize(
            folderpath=folderpath,
            workspace_metadata_path=workspace_metadata_path,
            workspace_toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=cls.WORKSPACE_TYPE,
            _replace_toml_template_values=False,
        )

        # Get the package toml template to fill in
        with G.get_package_path() as pkg_path:
            meta_workspace_toml_template_path = os.path.join(
                pkg_path, cls.WORKSPACE_TOML_TEMPLATE_RELPATH
            )
            G.concatenate_file_contents(
                [toml_filepath, meta_workspace_toml_template_path], toml_filepath
            )

        # Read with tomlkit
        with open(toml_filepath, mode="rt") as f:
            doc = tomlkit.parse(f.read())

        # Replace all the relevant template values
        data = {
            "allowed_workspace_types": str([cls.WORKSPACE_TYPE]),
            "schema_filepath": "./" + workspace_toml_filename + ".schema.json",
        }
        template = Template(doc.as_string())
        toml_string = template.render(data)

        # Create the workspace toml
        with open(toml_filepath, "w") as f:
            _ = f.write(toml_string)

        # Create the sidecar schema json file
        schema_json_filepath = toml_filepath + ".schema.json"
        adapter = TypeAdapter(ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE)
        schema = adapter.json_schema()

        with open(schema_json_filepath, "w") as f:
            json.dump(schema, f, indent=2)

        return toml_filepath

    @classmethod
    @typechecked
    def link(
        cls, subject_workspace_toml_filepath: str, target_workspace_toml_filepath: str
    ) -> None:
        """
        This function links one workspace with another.

        One workspace takes the manager role, able to pass arguments to the
        This is reflected in the workspace tom of the manager and the managed being changed.

        """
        # -------------------------------------
        # Possible future enhancement
        # Right now, whenever the linked_by (or lnks to) is added,
        #   it is added without taking good care that the order of what is being added is kept
        #   As a result, the helpful documentation that was set up in the template is less effective
        #   A possible solution could be to replace the value in place in the document,
        #   maybe if we are deleting it and re-addig it, it makes it show up at the end of the document
        #
        #   Another possible way to fix this is to remake the template document
        #       every time you are to change the workspace toml file, this way we have complete control
        #       over how it is written

        # Clean the filepaths
        subject_workspace_toml_filepath = G.get_posix_path(
            subject_workspace_toml_filepath
        )
        target_workspace_toml_filepath = G.get_posix_path(
            target_workspace_toml_filepath
        )

        # Both MUST exist
        G.check_file_exists(subject_workspace_toml_filepath)
        G.check_file_exists(target_workspace_toml_filepath)

        # Read in the required information for both

        ## The subject should ALWAYS be a meta workspace
        subject_workspace_toml_doc = G.read_toml_doc(
            subject_workspace_toml_filepath, ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE
        )
        subject_workspace_toml_dict = t.cast(
            ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            subject_workspace_toml_doc.unwrap(),
        )

        ## The target can be any ov workspace
        target_workspace_toml_doc = G.read_toml_doc(
            target_workspace_toml_filepath, ov_ws_types.GENERIC_WORKSPACE_TOML_DICT_TYPE
        )
        target_workspace_toml_dict = t.cast(
            ov_ws_types.GENERIC_WORKSPACE_TOML_DICT_TYPE,
            target_workspace_toml_doc.unwrap(),
        )

        # Extract the linked_by info from the dictionary & create doc table
        linked_by_dict: ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE = {
            "id": subject_workspace_toml_dict["id"],
            "name": subject_workspace_toml_dict["name"],
            "type": subject_workspace_toml_dict["type"],
            "workspace_tomlpath": os.path.abspath(subject_workspace_toml_filepath),
        }
        linked_by_table = tomlkit.table()
        linked_by_table.update(linked_by_dict)

        # Check if the linked_by has already been defined
        found_id = False
        for linked_by_item in target_workspace_toml_doc["linked_by"].unwrap():
            linked_by_item_dict = t.cast(
                ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE, linked_by_item
            )
            if linked_by_dict["id"] == linked_by_item_dict["id"]:
                found_id = True
                break

        skip_linked_by = False
        if found_id:
            # Thechnically if we find the id, it is not certain that everything has the information it should, but this can be enhanced later
            skip_linked_by = True

        # After this check we are assured that the found_by entry is clean from duplicates

        if not skip_linked_by:
            # Add linked_by to the target
            linked_by = target_workspace_toml_doc["linked_by"]

            ## If it is an AoT and it already has a value, then append
            if isinstance(linked_by, AoT) and len(linked_by) > 0:
                # Mypy now knows linked_by is a Sized AoT
                linked_by.append(linked_by_table)
            else:
                # If it's missing, empty, or a different type (like a tomlkit.items.Array),
                # create a fresh Array of Tables (AoT)
                new_aot = tomlkit.aot()
                new_aot.append(linked_by_table)
                target_workspace_toml_doc["linked_by"] = new_aot

            ## Write
            with open(target_workspace_toml_filepath, "w") as f:
                f.write(tomlkit.dumps(target_workspace_toml_doc))

        # Add links_to to the target
        # Extract the links_to info from the dictionary & create doc table
        links_to_dict: ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE = {
            "id": target_workspace_toml_dict["id"],
            "name": target_workspace_toml_dict["name"],
            "type": target_workspace_toml_dict["type"],
            "workspace_tomlpath": os.path.abspath(target_workspace_toml_filepath),
        }
        links_to_table = tomlkit.table()
        links_to_table.update(links_to_dict)

        # Check if the links_to has already been defined
        found_id = False
        for links_to_item in subject_workspace_toml_doc["links_to"].unwrap():
            links_to_item_dict = t.cast(
                ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE, links_to_item
            )
            if links_to_dict["id"] == links_to_item_dict["id"]:
                found_id = True
                break

        skip_links_to = False
        if found_id:
            # Thechnically if we find the id, it is not certain that everything has the information it should, but this can be enhanced later
            skip_links_to = True

        # After this check we are assured that the found_by entry is clean from duplicates

        if not skip_links_to:
            # Add links_to to the target
            links_to = subject_workspace_toml_doc["links_to"]

            ## If it is an AoT and it already has a value, then append
            if isinstance(links_to, AoT) and len(links_to) > 0:
                # Mypy now knows links_to is a Sized AoT
                links_to.append(links_to_table)
            else:
                # If it's missing, empty, or a different type (like a tomlkit.items.Array),
                # create a fresh Array of Tables (AoT)
                new_aot = tomlkit.aot()
                new_aot.append(links_to_table)
                subject_workspace_toml_doc["links_to"] = new_aot

            ## Write
            with open(subject_workspace_toml_filepath, "w") as f:
                f.write(tomlkit.dumps(subject_workspace_toml_doc))

    @classmethod
    @typechecked
    def unlink(
        cls, subject_workspace_toml_filepath: str, target_workspace_toml_filepath: str
    ) -> None:
        """
        This function unlinks a metaworkspace with another.

        One workspace takes the manager role, able to pass arguments to the
        This is reflected in the workspace tom of the manager and the managed being changed.

        """
        # Clean the filepaths
        subject_workspace_toml_filepath = G.get_posix_path(
            subject_workspace_toml_filepath
        )
        target_workspace_toml_filepath = G.get_posix_path(
            target_workspace_toml_filepath
        )

        # Both MUST exist
        G.check_file_exists(subject_workspace_toml_filepath)
        G.check_file_exists(target_workspace_toml_filepath)

        # Read in the required information for both

        ## The subject should ALWAYS be a meta workspace
        subject_workspace_toml_doc = G.read_toml_doc(
            subject_workspace_toml_filepath, ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE
        )
        subject_workspace_toml_dict = t.cast(
            ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            subject_workspace_toml_doc.unwrap(),
        )

        ## The target can be any ov workspace
        target_workspace_toml_doc = G.read_toml_doc(
            target_workspace_toml_filepath, ov_ws_types.GENERIC_WORKSPACE_TOML_DICT_TYPE
        )
        target_workspace_toml_dict = t.cast(
            ov_ws_types.GENERIC_WORKSPACE_TOML_DICT_TYPE,
            target_workspace_toml_doc.unwrap(),
        )

        # Try to find the exact linked_by entry to remove it
        linked_by_dict: ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE = {
            "id": subject_workspace_toml_dict["id"],
            "name": subject_workspace_toml_dict["name"],
            "type": subject_workspace_toml_dict["type"],
            "workspace_tomlpath": os.path.abspath(subject_workspace_toml_filepath),
        }

        # Find the linked by and remove it
        for i, linked_by_item in enumerate(
            target_workspace_toml_doc["linked_by"].unwrap()
        ):
            linked_by_item_dict = t.cast(
                ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE, linked_by_item
            )
            if linked_by_dict["id"] != linked_by_item_dict["id"]:
                continue

            # Remove the current index
            if isinstance(target_workspace_toml_doc["linked_by"], AoT):
                target_workspace_toml_doc["linked_by"].pop(i)
                if len(target_workspace_toml_doc["linked_by"]) == 0:
                    # Set as an empty document array
                    target_workspace_toml_doc["linked_by"] = tomlkit.array()
            else:
                raise NotImplementedError(
                    f"The type '{type(target_workspace_toml_doc['linked_by'])}' is NOT supported!"
                )

        ## Write
        with open(target_workspace_toml_filepath, "w") as f:
            f.write(tomlkit.dumps(target_workspace_toml_doc))

        # Remove links_to to the target
        # Extract the links_to info from the dictionary & create doc table
        links_to_dict: ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE = {
            "id": target_workspace_toml_dict["id"],
            "name": target_workspace_toml_dict["name"],
            "type": target_workspace_toml_dict["type"],
            "workspace_tomlpath": os.path.abspath(target_workspace_toml_filepath),
        }
        # Find the links to and remove it
        for i, linked_to_item in enumerate(
            subject_workspace_toml_doc["links_to"].unwrap()
        ):
            linked_to_item_dict = t.cast(
                ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE, linked_to_item
            )
            if links_to_dict["id"] != linked_to_item_dict["id"]:
                continue

            # Remove the current index
            if isinstance(subject_workspace_toml_doc["links_to"], AoT):
                subject_workspace_toml_doc["links_to"].pop(i)
                if len(subject_workspace_toml_doc["links_to"]) == 0:
                    # Set as an empty document array
                    subject_workspace_toml_doc["links_to"] = tomlkit.array()

            else:
                raise NotImplementedError(
                    f"The type '{type(subject_workspace_toml_doc['links_to'])}' is NOT supported!"
                )

        ## Write
        with open(subject_workspace_toml_filepath, "w") as f:
            f.write(tomlkit.dumps(subject_workspace_toml_doc))


class TemplatesWorkspaceService:
    """
    Service class where all methods recieve the workspace folderpath.

    The methods can get information or transform the workspace in any way

    This service class handles a Templates workspace, a workspace of tempalate files and folders
    """

    DEFAULT_WORKSPACE_NAME: t.Final = "ov-templates"
    DEFAULT_METADATA_FOLDERPATH: t.Final = "." + DEFAULT_WORKSPACE_NAME

    WORKSPACE_TYPE: t.Final[t.Literal["ov-templates"]] = DEFAULT_WORKSPACE_NAME

    @classmethod
    @typechecked
    def initialize(
        cls,
        folderpath: str,
        workspace_metadata_path: str,
        workspace_toml_filename: str,
        workspace_name: str,
        workspace_id: str,
    ) -> None:
        """Initializes a new Templates workspace"""

        # Initialize a base workspace
        GenericWorkspaceService.initialize(
            folderpath=folderpath,
            workspace_metadata_path=workspace_metadata_path,
            workspace_toml_filename=workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
            workspace_type=cls.WORKSPACE_TYPE,
        )


DEFAULT_WORKSPACE_METADATA_INFO: WORKSPACE_DEFAULT_METADATA_INFO_DICT_TYPE = {
    "ov-meta": MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH,
    "ov-templates": TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH,
}
