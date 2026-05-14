from uuid import uuid4
from OpenViatica._core_workspaces._core_workspaces_services import (
    MetaWorkspaceService,
    TemplatesWorkspaceService,
    DEFAULT_WORKSPACE_TOML_FILENAME,
    DEFAULT_WORKSPACE_METADATA_INFO,
)
from OpenViatica._errors import ov_errors
from OpenViatica._types import (
    ov_ws_types,
    ov_ws_type_t,
    meta_workspace_toml_type_value,
    templates_workspace_toml_type_value,
)
from OpenViatica._general_core import General as G
import typing as t
import glob

from pathlib import Path
import os
from typeguard import typechecked


class TemplatesWorkspace:
    """
    # Templates Workspace

    Provides a set of function for managing a Templates Workspace of template files and folders

    """

    WORKSPACE_TYPE = TemplatesWorkspaceService.WORKSPACE_TYPE

    @typechecked
    def __init__(
        self,
        workspace_path: str = "./",
        _workspace_metadata_path: str | None = None,
        _workspace_toml_filename: str | None = None,
    ) -> None:
        """
        Initializes a configured transformer for an OpenViatica Workspace
        """
        self.workspace_path: str
        self.workspace_metadata_path: str
        self.workspace_toml_filename: str

        # Clean workspace path
        workspace_path = Path(workspace_path).as_posix()

        # If the user did not define a workspace relpath, use the program default
        if _workspace_metadata_path is None:
            _workspace_metadata_path = os.path.join(
                workspace_path, TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH
            )

        if _workspace_toml_filename is None:
            _workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

        self.workspace_path = workspace_path
        self.workspace_metadata_path = _workspace_metadata_path

        self.workspace_toml_filename = _workspace_toml_filename

    @typechecked
    def initialize(
        self,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
    ) -> None:
        """Initializes a new OpenViatica meta workspace"""

        # Set default values
        if workspace_id is None:
            workspace_id = str(uuid4())

        if workspace_name is None:
            workspace_name = TemplatesWorkspaceService.DEFAULT_WORKSPACE_NAME

        # Any necessary checks are done in the service itself
        TemplatesWorkspaceService.initialize(
            folderpath=self.workspace_path,
            workspace_metadata_path=self.workspace_metadata_path,
            workspace_toml_filename=self.workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
        )


class MetaWorkspace:
    """
    # Meta Workspace

    Provides a set of function for managing a Meta Workspace of other workspaces

    """

    WORKSPACE_TYPE: t.Final[t.Literal["ov-meta"]] = MetaWorkspaceService.WORKSPACE_TYPE

    @typechecked
    def __init__(
        self,
        workspace_path: str = "./",
        _workspace_metadata_path: str | None = None,
        _workspace_toml_filename: str | None = None,
    ) -> None:
        """
        Initializes a configured transformer for an OpenViatica Workspace
        """
        self.workspace_path: str
        self.workspace_abspath: str
        self.workspace_metadata_path: str
        self.workspace_toml_filename: str
        self._workspace_toml_filepath: str
        self._workspace_is_initialized: bool
        self.workspace_toml_dict: ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE | None = (
            None
        )

        # Clean workspace path
        workspace_path = Path(workspace_path).as_posix()

        # If the user did not define a workspace relpath, use the program default
        if _workspace_metadata_path is None:
            _workspace_metadata_path = os.path.join(
                workspace_path, MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH
            )

        if _workspace_toml_filename is None:
            _workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

        self.workspace_path = workspace_path
        self.workspace_abspath = os.path.abspath(self.workspace_path)

        self.workspace_metadata_path = _workspace_metadata_path

        self.workspace_toml_filename = _workspace_toml_filename
        self._workspace_toml_filepath = os.path.join(
            self.workspace_metadata_path, self.workspace_toml_filename
        )

        if os.path.exists(self._workspace_toml_filepath):
            self.workspace_toml_dict = t.cast(
                ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
                G.read_toml_dict(
                    self._workspace_toml_filepath,
                    ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
                ),
            )

    @typechecked
    def initialize(
        self,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
    ) -> str:
        """Initializes a new OpenViatica meta workspace"""

        # Set default values
        if workspace_id is None:
            workspace_id = str(uuid4())

        if workspace_name is None:
            # If the workspace has not been defined, use the foldername as the workspace name
            workspace_name = os.path.basename(self.workspace_abspath)

        # Any necessary checks are done in the service itself
        workspace_toml_path = MetaWorkspaceService.initialize(
            folderpath=self.workspace_path,
            workspace_metadata_path=self.workspace_metadata_path,
            workspace_toml_filename=self.workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
        )
        return workspace_toml_path

    @typechecked
    def link(
        self,
        target_workspace_path: str,
        target_workspace_type: ov_ws_type_t
        | None = None,  # NOTE: Defining this parameter probably helps with performance
        _target_workspace_metadata_path: str | None = None,
        _target_workspace_toml_filename: str | None = None,
    ) -> str:
        """
        Links the meta workspace with another workspace
        """
        # Run the centralized function
        target_workspace_toml_filepath = self._link_unlink(
            target_workspace_path=target_workspace_path,
            link_mode="link",
            target_workspace_type=target_workspace_type,
            _target_workspace_metadata_path=_target_workspace_metadata_path,
            _target_workspace_toml_filename=_target_workspace_toml_filename,
        )
        return target_workspace_toml_filepath

    @typechecked
    def unlink(
        self,
        target_workspace_path: str,
        target_workspace_type: ov_ws_type_t
        | None = None,  # NOTE: Defining this parameter probably helps with performance
        _target_workspace_metadata_path: str | None = None,
        _target_workspace_toml_filename: str | None = None,
    ) -> str:
        """
        Unlinks a meta workspace with another workspace
        """
        # Run the centralized function
        target_workspace_toml_filepath = self._link_unlink(
            target_workspace_path=target_workspace_path,
            link_mode="unlink",
            target_workspace_type=target_workspace_type,
            _target_workspace_metadata_path=_target_workspace_metadata_path,
            _target_workspace_toml_filename=_target_workspace_toml_filename,
        )
        return target_workspace_toml_filepath

    @t.overload
    def get_linked_workspace_object(
        self,
        identifier: str,
        expected_type_name: t.Literal["ov-meta"],
        identifier_type: t.Literal["id", "name"] | None = None,
    ) -> "MetaWorkspace": ...

    @t.overload
    def get_linked_workspace_object(
        self,
        identifier: str,
        expected_type_name: t.Literal["ov-templates"],
        identifier_type: t.Literal["id", "name"] | None = None,
    ) -> TemplatesWorkspace: ...

    @t.overload
    def get_linked_workspace_object(
        self,
        identifier: str,
        expected_type_name: None = None,
        identifier_type: t.Literal["id", "name"] | None = None,
    ) -> "MetaWorkspace | TemplatesWorkspace": ...

    @typechecked
    def get_linked_workspace_object(
        self,
        identifier: str,
        expected_type_name: ov_ws_type_t | None = None,
        identifier_type: t.Literal["id", "name"] | None = None,
    ) -> "MetaWorkspace | TemplatesWorkspace":
        """Returns a fully configured workspace object that can be used to run commands on"""

        # Get the workspace information
        workspace_dict = self.get_workspace_links_to_dict(
            identifier=identifier, identifier_type=identifier_type
        )

        # Get the init args
        _workspace_toml_filename = os.path.basename(
            workspace_dict["workspace_tomlpath"]
        )
        _workspace_metadata_path = os.path.abspath(
            os.path.join(workspace_dict["workspace_tomlpath"], "../")
        )

        workspace_path = os.path.abspath(
            os.path.join(workspace_dict["workspace_tomlpath"], "../../")
        )

        # Get the class
        workspace_type = workspace_dict["type"]
        workspace_class = WORKSPACE_CLASS_MAPPING_DICT[workspace_type]
        workspace_obj = workspace_class(
            workspace_path=workspace_path,
            _workspace_metadata_path=_workspace_metadata_path,
            _workspace_toml_filename=_workspace_toml_filename,
        )

        if expected_type_name is not None:
            if not isinstance(
                workspace_obj, WORKSPACE_CLASS_MAPPING_DICT[expected_type_name]
            ):
                raise TypeError(
                    f"The type of the workspace '{identifier}' is not the same as the expected type: '{expected_type_name}'"
                )

        return workspace_obj

    @typechecked
    def is_initialized(self) -> bool:
        """Returns True if the currently defined workspace has been initialized"""
        result = False
        try:
            self.check_initialized()
            result = True
        except Exception:
            pass
        return result

    @typechecked
    def check_initialized(self) -> None:
        """Raises an error if the workspace has not been initialized"""

        # Check that the workspace path exists
        G.check_folder_exists(self.workspace_path)

        # Check that the workspace metadata folder exists
        G.check_folder_exists(self.workspace_path)

        # Check that the workspace toml exists
        G.check_file_exists(self._workspace_toml_filepath)

        # Check that it is of the correct format
        try:
            _ = G.read_toml_dict(
                self._workspace_toml_filepath,
                expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
            )
        except Exception as e:
            # If it failed that means it is of an incorrect format
            raise ov_errors.WorkspaceTomlFormatError(
                f"The format for the workspace toml '{self._workspace_toml_filepath}' is incorrect! Error found: {str(e)}"
            )

    @typechecked
    def get_workspace_links_to_dict(
        self,
        identifier: str,
        identifier_type: t.Literal["id", "name"] | None = None,
    ) -> ov_ws_types.WORKSPACE_TOML_LINK_DICT_TYPE:
        """Returns a dictionary with all the information of the workspace given the identifier and identifier type"""

        # Load the current workspace toml
        workspace_toml_dict = G.read_toml_dict(
            toml_filepath=self._workspace_toml_filepath,
            expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE,
        )
        workspace_toml_dict = t.cast(
            ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE, workspace_toml_dict
        )

        # Get the links_to objects
        links_to_values = workspace_toml_dict["links_to"]

        # Try to filter
        if identifier_type is not None:
            # If here, then the user defined an id type, so use that assumption
            filtered_values = [
                item for item in links_to_values if item[identifier_type] == identifier
            ]

            # Check for any potential cases
            if len(filtered_values) == 0:
                raise ov_errors.LinkNotFoundError(
                    f"Found no link with '{identifier_type}' equal to '{identifier}'"
                )
            elif len(filtered_values) > 1:
                raise ov_errors.DuplicatedLinksFoundError(
                    f"Found multiple links where the '{identifier_type}' equals '{identifier}'"
                )
            # If here, we are garenteed that it found only one result
            result = filtered_values[0]

        else:
            # Else try to find a single match based on a priority system
            name_match_index_list: list[int] = []
            id_match_index_list: list[int] = []

            for i, links_to_dict in enumerate(links_to_values):
                if links_to_dict["name"] == identifier:
                    name_match_index_list.append(i)

                if links_to_dict["id"] == identifier:
                    id_match_index_list.append(i)

            # If here, then we have lists of possible matches only one can be right
            # Do a priority system:
            #   name: if a name matched, use that
            #   id: otherwise, use an id match
            #   None: raise an error, could not find

            # For performance reasons we need to identify the information we need under a single for loop of the data
            # We will use other parts but ultimately determine the filtered_values that would pass scrutiny
            # Other parts of the code would be the ones responsible for cleaning it up

            breakpoint()
            pass

        return result

    # Private functions
    @typechecked
    def _link_unlink(
        self,
        target_workspace_path: str,
        link_mode: t.Literal["link", "unlink"],
        target_workspace_type: ov_ws_type_t
        | None = None,  # NOTE: Defining this parameter probably helps with performance
        _target_workspace_metadata_path: str | None = None,
        _target_workspace_toml_filename: str | None = None,
    ) -> str:
        """
        Private function to centralize the logic to link or unlink a workspace
        Especially because the logic are pretty similar
        """

        #  POSSIBLE IMPROVEMENT!
        #   WHAT IF THE LINKED WORKSPACE ID IS NOT UNIQUE!?
        #   THIS LINKING DOES NOT CHECK FOR THAT, SO MULTPLE WORKSPACE WITH THE SAME ID COULD BE ADDED...
        #   THIS COULD BE MITIGATED BY RAISING AN ERROR OR CREATING A UNIQUE ID ON THE META WORKSPACE SIDE
        #   NOT A PROBLEM FOR ME RIGHT NOW
        # ---------------------------------------------
        # Second comment on this improvement, the subject workspace could create a new id in his side,
        #   so that even if the target ids are repeated, we can use the subject link id as a tie breaker
        # -------------------------------------------------------
        # Another possible improvement, we could also
        # give the user the option to use name of ID as a tie breaker,
        # This would of course make the logic much more complicated,
        # so future me problem if I need it
        # --------------------------------------------------------

        # Clean target workspace path
        target_workspace_path = G.get_posix_path(target_workspace_path)

        # Standardize the value of the workspace metadata path if it is defined
        if _target_workspace_metadata_path is None:
            # If it was not defined, then we go by the default assumptions
            # We will try to find one result
            # Get a list of the immediate folders in the path
            immediate_foldernames = G.get_immediate_folders(target_workspace_path)

            # Filter by only the possible options
            #   based on what Services says
            #   are the default metadata folders
            possible_metadata_foldernames = [
                basename
                for basename in immediate_foldernames
                if basename in DEFAULT_WORKSPACE_METADATA_INFO.values()
            ]

            if len(possible_metadata_foldernames) == 0:
                raise ov_errors.WorkspaceMetadataNotFoundError(
                    f"No workspace metadata folder was found for '{target_workspace_path}'. "
                    + "Plase check that this path points to a OpenViatica workspace."
                )
            # Filter for the workspace type if it was defined.
            if target_workspace_type is not None:
                expected_metadata_foldername = DEFAULT_WORKSPACE_METADATA_INFO[
                    target_workspace_type
                ]
                possible_metadata_foldernames = [
                    name
                    for name in possible_metadata_foldernames
                    if name == expected_metadata_foldername
                ]
                if len(possible_metadata_foldernames) == 0:
                    raise ov_errors.WorkspaceMetadataNotFoundError(
                        f"The expected metadata folder '{expected_metadata_foldername}' "
                        + f"for the path '{target_workspace_path}' and the type '{target_workspace_type}'"
                        + "was not found. "
                        + "Please check that this path "
                        + "points to an OpenViatica workspace "
                        + "and that the type of the workspace "
                        + "is the same as the one referenced."
                    )
                # If here, then the workspace type has helped find the workspace metadata folder
                # It will be reflected as being the only value
                #   in the possible metadata foldernames variable

            # If multiple workspace metadata folders are still possible,
            #   then raise an error
            if len(possible_metadata_foldernames) > 1:
                raise ov_errors.MultipleWorkspaceMetadataFoundError(
                    f"Multiple workspace metadata folders '{possible_metadata_foldernames}' found in '{target_workspace_path}'."
                    + "Please define the workspace type."
                )
            # If here, then we are garenteed that we found the metadata folder
            _target_workspace_metadata_path = os.path.join(
                target_workspace_path, possible_metadata_foldernames[0]
            )
        # If the workspace metadata path WAS defined by the user, clean it
        else:
            _target_workspace_metadata_path = G.get_posix_path(
                _target_workspace_metadata_path
            )

        # No need to set a default value for workspace type,
        #   since it is mainly just used as a tie breaker
        #   to select the correct metadata folderpath anyways

        # Make sure the target_workspace_path exists
        G.check_folder_exists(target_workspace_path)

        # Set a default value for the workspace toml filename if the user did not define it
        if _target_workspace_toml_filename is None:
            _target_workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

        # We should be able to define the workspace toml filepath now
        target_workspace_toml_filepath = os.path.join(
            _target_workspace_metadata_path, _target_workspace_toml_filename
        )

        if link_mode == "link":
            MetaWorkspaceService.link(
                subject_workspace_toml_filepath=self._workspace_toml_filepath,
                target_workspace_toml_filepath=target_workspace_toml_filepath,
            )
        else:
            MetaWorkspaceService.unlink(
                subject_workspace_toml_filepath=self._workspace_toml_filepath,
                target_workspace_toml_filepath=target_workspace_toml_filepath,
            )
        return target_workspace_toml_filepath


WORKSPACE_CLASS_MAPPING_DICT: dict[
    ov_ws_type_t, type[MetaWorkspace | TemplatesWorkspace]
] = {
    meta_workspace_toml_type_value: MetaWorkspace,
    templates_workspace_toml_type_value: TemplatesWorkspace,
}
