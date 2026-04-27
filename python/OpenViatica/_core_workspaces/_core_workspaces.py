
from uuid import uuid4
from OpenViatica._core_workspaces._core_workspaces_services import \
    MetaWorkspaceService, TemplatesWorkspaceService, \
    DEFAULT_WORKSPACE_TOML_FILENAME, DEFAULT_WORKSPACE_METADATA_INFO
from OpenViatica._errors import ov_errors
from OpenViatica._types import ov_ws_types, ov_ws_type_t
from OpenViatica._general_core import General as G

from pathlib import Path
import os
from typeguard import typechecked

class MetaWorkspace:
        '''
        # Meta Workspace

        Provides a set of function for managing a Meta Workspace of other workspaces
        
        '''

        @typechecked
        def __init__(
            self,
            workspace_path:str = "./",
            _workspace_metadata_path:str | None = None,
            _workspace_toml_filename: str | None = None
            ) -> None:
            '''
            Initializes a configured transformer for an OpenViatica Workspace 
            '''
            self._workspace_path  : str
            self._workspace_metadata_path : str
            self._workspace_toml_filename:str
            self._workspace_toml_filepath : str 
            self._workspace_is_initialized: bool

            # Clean workspace path
            workspace_path = Path(workspace_path).as_posix()

            # If the user did not define a workspace relpath, use the program default
            if _workspace_metadata_path is None:
                _workspace_metadata_path = os.path.join(
                    workspace_path,
                    MetaWorkspaceService.DEFAULT_METADATA_FOLDERPATH
                )

            if _workspace_toml_filename is None:
                _workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

            self._workspace_path = workspace_path
            self._workspace_metadata_path = _workspace_metadata_path

            self._workspace_toml_filename = _workspace_toml_filename
            self._workspace_toml_filepath = os.path.join(self._workspace_metadata_path, self._workspace_toml_filename)


        @typechecked
        def initialize(
            self,
            workspace_id: str | None = None,
            workspace_name: str | None = None,
        ) -> None:
            '''Initializes a new OpenViatica meta workspace'''

            # Set default values
            if workspace_id is None:
                workspace_id = str(uuid4())

            if workspace_name is None:
                workspace_name = MetaWorkspaceService.DEFAULT_WORKSPACE_NAME
            
            # Any necessary checks are done in the service itself
            MetaWorkspaceService.initialize(
                folderpath = self._workspace_path,
                workspace_metadata_path=self._workspace_metadata_path,
                workspace_toml_filename = self._workspace_toml_filename,
                workspace_name=workspace_name,
                workspace_id=workspace_id
            )


        def link(self,
            target_workspace_path:str,
            target_workspace_type: ov_ws_type_t,
            _target_workspace_metadata_path:str | None = None,
            _target_workspace_toml_filename: str | None = None
            ) -> None:
            '''
            Links the meta workspace with another workspace
            '''            

            # Clean paths & set defaults
            target_workspace_path = G.get_posix_path(target_workspace_path)

            if _target_workspace_metadata_path is not None:
                _target_workspace_metadata_path = G.get_posix_path(_target_workspace_metadata_path)
            else:
                # Else we should be able to define the workspace metadata path based on the type
                _target_workspace_metadata_path = os.path.join(
                    target_workspace_path,
                    DEFAULT_WORKSPACE_METADATA_INFO[target_workspace_type]
                    )

            if _target_workspace_toml_filename is None:
                _target_workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME
            
            
            # We should be able to define the workspace toml filepath now
            target_workspace_toml_filepath = os.path.join(_target_workspace_metadata_path, _target_workspace_toml_filename)

            MetaWorkspaceService.link(
                subject_workspace_toml_filepath=self._workspace_toml_filepath,
                target_workspace_toml_filepath=target_workspace_toml_filepath
            )

        def is_initialized(self) -> bool:
            '''Returns True if the currently defined workspace has been initialized'''
            result = False
            try:
                self.check_initialized()
                result = True
            except Exception:
                pass
            return result


        def check_initialized(self) -> None: 
            '''Raises an error if the workspace has not been initialized'''
            
            # Check that the workspace path exists
            G.check_folder_exists(self._workspace_path)

            # Check that the workspace metadata folder exists
            G.check_folder_exists(self._workspace_path)

            # Check that the workspace toml exists
            G.check_file_exists(self._workspace_toml_filepath)

            # Check that it is of the correct format
            try:
                G.read_toml_dict(self._workspace_toml_filepath, expected_type=ov_ws_types.META_WORKSPACE_TOML_DICT_TYPE)
            except Exception as e:
                # If it failed that means it is of an incorrect format
                raise ov_errors.WorkspaceTomlFormatError(f"The format for the workspace toml '{self._workspace_toml_filepath}' is incorrect! Error found: {str(e)}")


        # Private functions










class TemplatesWorkspace:
        '''
        # Templates Workspace

        Provides a set of function for managing a Templates Workspace of template files and folders
        
        '''

        @typechecked
        def __init__(
            self,
            workspace_path:str = "./",
            _workspace_metadata_path:str | None = None,
            _workspace_toml_filename: str | None = None
            ) -> None:
            '''
            Initializes a configured transformer for an OpenViatica Workspace 
            '''
            self._workspace_path  : str
            self._workspace_metadata_path : str
            self._workspace_toml_filename:str

            # Clean workspace path
            workspace_path = Path(workspace_path).as_posix()

            # If the user did not define a workspace relpath, use the program default
            if _workspace_metadata_path is None:
                _workspace_metadata_path = os.path.join(
                    workspace_path,
                    TemplatesWorkspaceService.DEFAULT_METADATA_FOLDERPATH
                )

            if _workspace_toml_filename is None:
                _workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

            self._workspace_path = workspace_path
            self._workspace_metadata_path = _workspace_metadata_path

            self._workspace_toml_filename = _workspace_toml_filename

        @typechecked
        def initialize(
            self,
            workspace_id: str | None = None,
            workspace_name: str | None = None,
        ) -> None:
            '''Initializes a new OpenViatica meta workspace'''

            # Set default values
            if workspace_id is None:
                workspace_id = str(uuid4())

            if workspace_name is None:
                workspace_name = TemplatesWorkspaceService.DEFAULT_WORKSPACE_NAME
            
            # Any necessary checks are done in the service itself
            TemplatesWorkspaceService.initialize(
                folderpath = self._workspace_path,
                workspace_metadata_path=self._workspace_metadata_path,
                workspace_toml_filename = self._workspace_toml_filename,
                workspace_name=workspace_name,
                workspace_id=workspace_id
            )
            
        