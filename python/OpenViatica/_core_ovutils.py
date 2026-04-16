from OpenViatica._core_workspaces._core_workspaces import MetaWorkspace
from typeguard import typechecked
from OpenViatica._general_core import General as G
import os

class ovutils:

    # No service is created for this one, because this class should use the tools already available to the user
    # It should mimic the user going in and manually creating all the necessary pre-config work

    DEFAULT_WORKSPACE_NAME = "openviatica"
    DEFAULT_METADATA_FOLDERPATH = "." + DEFAULT_WORKSPACE_NAME

    @typechecked
    def __init__(
        self, 
        workspace_path:str = "./",
        _workspace_metadata_path: None | str = None,   

        # Meta workspace arguments, they get passed directly to the Meta workspace class
        _meta_workspace_path: str | None = None,
        _meta_workspace_metadata_path: str | None = None,
        _meta_workspace_toml_filename: str | None = None
        ) -> None:

        self._workspace_path: str
        self._workspace_metadata_path: str


        workspace_path = G.get_posix_path(workspace_path)

        if _workspace_metadata_path is None:
            _workspace_metadata_path = os.path.join(workspace_path, self.DEFAULT_METADATA_FOLDERPATH)
        else:
            _workspace_metadata_path = G.get_posix_path(_workspace_metadata_path)
        
        if _meta_workspace_path is None:
            _meta_workspace_path = _workspace_metadata_path
        
        

        self._workspace_path = workspace_path

        self._workspace_metadata_path = _workspace_metadata_path

        self._meta_ws = MetaWorkspace(
            workspace_path=_meta_workspace_path,
            _workspace_metadata_path = _meta_workspace_metadata_path,
            _workspace_toml_filename = _meta_workspace_toml_filename
        )

    @typechecked
    def initialize(
        self,
        workspace_id: str | None = None,
        workspace_name: str | None = None
    ) -> None:
        '''Initializes a new OpenViatica Preconfigured workspace'''

        # A OpenViatica IS an instance of a MetaWorkspace, that just has other workspaces made by default

        if workspace_name is None:
            workspace_name = self.DEFAULT_WORKSPACE_NAME

        # Check if the workspace folder exists
        G.check_folder_exists(self._workspace_path)

        # Check that the workspace metadata does NOT exist
        G.check_folder_NOT_exists(self._workspace_metadata_path)

        # Create the metadata folder
        os.mkdir(self._workspace_metadata_path)

        # Initialize the meta workspace
        self._meta_ws.initialize(
            workspace_id=workspace_id,
            workspace_name=workspace_name
        )


    class WorkpaceTools:
        MetaWorkspace: type["MetaWorkspace"]


ovutils.WorkpaceTools.MetaWorkspace = MetaWorkspace




