
from OpenViatica._core_workspaces import ws_service
from pathlib import Path
import os
from typeguard import typechecked
class ws:
        '''
        # OpenViatica Workspace

        Provides a set of function for managing a Openviatica Workspace of other workspaces
        
        '''

        @typechecked
        def __init__(
            self,
            folderpath:str = "./",
            _workspace_relpath:str | None = None
            ) -> None:
            '''
            Initializes a configured transformer for an OpenViatica Workspace 
            '''
            self._base_folderpath  : str
            self._workspace_relpath : str
            self._workspace_path : str

            # If the user did not define a workspace relpath, use the program default
            if _workspace_relpath is None:
                _workspace_relpath = ws_service.DEFAULT_FOLDERPATH

            self._base_folderpath = Path(folderpath).as_posix()
            self._workspace_relpath = Path(_workspace_relpath).as_posix()
            self._workspace_path = os.path.join(self._base_folderpath, self._workspace_relpath)
        
        @typechecked
        def initialize(self)

            