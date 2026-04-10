
from uuid import uuid4
from OpenViatica._core_workspaces._core_workspaces_services import \
    MetaWorkspaceService, \
    DEFAULT_WORKSPACE_TOML_FILENAME
from pathlib import Path
import os
from typeguard import typechecked

class MetaWorkspace:
        '''
        # OpenViatica Workspace

        Provides a set of function for managing a Openviatica Workspace of other workspaces
        
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
            self._workspace_metadata_relpath : str
            self._workspace_metadata_path : str
            self._workspace_toml_filename:str

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
            