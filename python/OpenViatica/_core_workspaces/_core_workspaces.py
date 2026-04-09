
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
            folderpath:str = "./",
            _workspace_relpath:str | None = None,
            _workspace_toml_filename: str | None = None
            ) -> None:
            '''
            Initializes a configured transformer for an OpenViatica Workspace 
            '''
            self._root_folderpath  : str
            self._workspace_relpath : str
            self._workspace_path : str
            self._workspace_toml_filename:str

            # If the user did not define a workspace relpath, use the program default
            if _workspace_relpath is None:
                _workspace_relpath = MetaWorkspaceService.DEFAULT_FOLDERPATH

            if _workspace_toml_filename is None:
                _workspace_toml_filename = DEFAULT_WORKSPACE_TOML_FILENAME

            self._root_folderpath = Path(folderpath).as_posix()
            self._workspace_relpath = Path(_workspace_relpath).as_posix()
            self._workspace_path = os.path.join(self._root_folderpath, self._workspace_relpath)

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
            
            if os.path.exists(self._workspace_path):
                raise NotImplementedError("ERROR! IF the folder already exists, we need to validate that it is NOT already a meta workspace!")

            
            MetaWorkspaceService.initialize(
                folderpath = self._root_folderpath,
                workspace_relpath=self._workspace_relpath,
                workspace_toml_filename = self._workspace_toml_filename,
                workspace_name=workspace_name,
                workspace_id=workspace_id
            )
            