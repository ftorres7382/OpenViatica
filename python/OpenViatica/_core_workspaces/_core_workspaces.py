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

    WORKSPACE_TYPE = MetaWorkspaceService.WORKSPACE_TYPE

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
        self._workspace_toml_filepath: str
        self._workspace_is_initialized: bool

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
        self.workspace_metadata_path = _workspace_metadata_path

        self.workspace_toml_filename = _workspace_toml_filename
        self._workspace_toml_filepath = os.path.join(
            self.workspace_metadata_path, self.workspace_toml_filename
        )

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
            # If the workspace has not been defined, use the foldername as the wrokspace name
            workspace_name = os.path.basename(self.workspace_path)

        # Any necessary checks are done in the service itself
        MetaWorkspaceService.initialize(
            folderpath=self.workspace_path,
            workspace_metadata_path=self.workspace_metadata_path,
            workspace_toml_filename=self.workspace_toml_filename,
            workspace_name=workspace_name,
            workspace_id=workspace_id,
        )

    @typechecked
    def link(
        self,
        target_workspace_path: str,
        target_workspace_type: ov_ws_type_t | None = None,
        _target_workspace_metadata_path: str | None = None,
        _target_workspace_toml_filename: str | None = None,
    ) -> None:
        """
        Links the meta workspace with another workspace
        """
        #  POSSIBLE IMPROVEMENT!
        #   WHAT IF THE LINKED WORKSPACE ID IS NOT UNIQUE!?
        #   THIS LINKING DOES NOT CHECK FOR THAT, SO MULTPLE WORKSPACE WITH THE SAME ID COULD BE ADDED...
        #   THIS COULD BE MITIGATED BY RAISING AN ERROR OR CREATING A UNIQUE ID ON THE META WORKSPACE SIDE
        #   NOT A PROBLEM FOR ME RIGHT NOW
        # ---------------------------------------------
        # Second comment on this improvement, the subject workspace could create a new id in his side,
        #   so that even if the target ids are repeated, we can use the subject link id as a tie breaker

        # Clean paths & set defaults
        target_workspace_path = G.get_posix_path(target_workspace_path)

        # If the workspace path is None, then we need to get what the workspace path should be
        # We need to take into account that a single workspace_path could contain multiple workspace types inside

        # Make sure the target_workspace_path exists
        G.check_folder_exists(target_workspace_path)
        # Check all the workspace types that are where
        breakpoint()

        if _target_workspace_metadata_path is not None:
            _target_workspace_metadata_path = G.get_posix_path(
                _target_workspace_metadata_path
            )
        else:
            # Else we should be able to define the workspace metadata path based on the type
            _target_workspace_metadata_path = os.path.join(
                target_workspace_path,
                DEFAULT_WORKSPACE_METADATA_INFO[target_workspace_type],
            )

        if _target_workspace_toml_filename is None:
            _target_workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

        # We should be able to define the workspace toml filepath now
        target_workspace_toml_filepath = os.path.join(
            _target_workspace_metadata_path, _target_workspace_toml_filename
        )

        MetaWorkspaceService.link(
            subject_workspace_toml_filepath=self._workspace_toml_filepath,
            target_workspace_toml_filepath=target_workspace_toml_filepath,
        )

    @typechecked
    def unlink(
        self,
        target_workspace_path: str,
        target_workspace_type: ov_ws_type_t,
        _target_workspace_metadata_path: str | None = None,
        _target_workspace_toml_filename: str | None = None,
    ) -> None:
        """
        Links the meta workspace with another workspace
        """

        # Clean paths & set defaults
        target_workspace_path = G.get_posix_path(target_workspace_path)

        if _target_workspace_metadata_path is not None:
            _target_workspace_metadata_path = G.get_posix_path(
                _target_workspace_metadata_path
            )
        else:
            # Else we should be able to define the workspace metadata path based on the type
            _target_workspace_metadata_path = os.path.join(
                target_workspace_path,
                DEFAULT_WORKSPACE_METADATA_INFO[target_workspace_type],
            )

        if _target_workspace_toml_filename is None:
            _target_workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

        # We should be able to define the workspace toml filepath now
        target_workspace_toml_filepath = os.path.join(
            _target_workspace_metadata_path, _target_workspace_toml_filename
        )

        MetaWorkspaceService.unlink(
            subject_workspace_toml_filepath=self._workspace_toml_filepath,
            target_workspace_toml_filepath=target_workspace_toml_filepath,
        )

    @t.overload
    def get_linked_workspace_object(
        self,
        identifier: str,
        identifier_type: t.Literal["id", "name"],
        expected_type_name: t.Literal["ov-meta"],
    ) -> "MetaWorkspace": ...

    # 2. Overload for "remote"
    @t.overload
    def get_linked_workspace_object(
        self,
        identifier: str,
        identifier_type: t.Literal["id", "name"],
        expected_type_name: t.Literal["ov-templates"],
    ) -> TemplatesWorkspace: ...

    # 3. Overload for None (returns the Base or a Union)
    @t.overload
    def get_linked_workspace_object(
        self,
        identifier: str,
        identifier_type: t.Literal["id", "name"],
        expected_type_name: None = None,
    ) -> "MetaWorkspace | TemplatesWorkspace": ...

    @typechecked
    def get_linked_workspace_object(
        self,
        identifier: str,
        identifier_type: t.Literal["id", "name"] | None = None,
        expected_type_name: ov_ws_type_t | None = None,
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
            filtered_values = [
                item for item in links_to_values if item[identifier_type] == identifier
            ]
        else:
            # Else we have to see what can find
            # For performance reasons we need to identify the information we need under a single for loop of the data
            # We will use other parts but ultimately determine the filtered_values that would pass scrutiny
            # Other parts of the code would be the ones responsible for cleaning it up
            breakpoint()
            pass

        # Check for any potential cases
        if len(filtered_values) == 0:
            raise ov_errors.LinkNotFoundError(
                f"Found no link with '{identifier_type}' equal to '{identifier}'"
            )
        elif len(filtered_values) > 1:
            raise ov_errors.DuplicatedLinksFoundError(
                f"Found multiple links where the '{identifier_type}' equals '{identifier}'"
            )
        result = filtered_values[0]

        return result

    # Private functions


WORKSPACE_CLASS_MAPPING_DICT: t.Dict[
    ov_ws_type_t, t.Type[MetaWorkspace | TemplatesWorkspace]
] = {
    meta_workspace_toml_type_value: MetaWorkspace,
    templates_workspace_toml_type_value: TemplatesWorkspace,
}
