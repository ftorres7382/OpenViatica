from OpenViatica._core_workspaces._core_workspaces import (
    MetaWorkspace,
    TemplatesWorkspace,
)
from typeguard import typechecked
from OpenViatica._general_core import General as G
import typing as t
import os


class ovutils:
    # No service is created for this one, because this class should use the tools already available to the user
    # It should mimic the user going in and manually creating all the necessary pre-config work

    DEFAULT_WORKSPACE_NAME: t.Final[str] = "openviatica"
    DEFAULT_METADATA_FOLDERPATH: t.Final[str] = "." + DEFAULT_WORKSPACE_NAME

    @typechecked
    def __init__(
        self,
        workspace_path: str = "./",
        _workspace_metadata_path: None | str = None,
        # Meta workspace arguments, they get passed directly to the Meta workspace class
        _meta_workspace_path: str | None = None,
        _meta_workspace_metadata_path: str | None = None,
        _meta_workspace_toml_filename: str | None = None,
        # Templates workspace arguments
        _templates_workspace_path: str | None = None,
        _templates_workspace_metadata_path: str | None = None,
        _templates_workspace_toml_filename: str | None = None,
    ) -> None:

        # Declaring the self variables of interest
        self.workspace_path: str
        self._workspace_metadata_path: str
        self._meta_ws: MetaWorkspace
        self._tmpl_ws: TemplatesWorkspace

        workspace_path = G.get_posix_path(workspace_path)

        # If the
        if _workspace_metadata_path is None:
            _workspace_metadata_path = os.path.join(
                workspace_path, self.DEFAULT_METADATA_FOLDERPATH
            )
        else:
            _workspace_metadata_path = G.get_posix_path(_workspace_metadata_path)

        # No need to clean, that is the job of the Meta class
        # Set the default path of the individual workspaces to be the metadata folder
        if _meta_workspace_path is None:
            _meta_workspace_path = _workspace_metadata_path

        if _templates_workspace_path is None:
            _templates_workspace_path = _workspace_metadata_path

        self.workspace_path = workspace_path

        self._workspace_metadata_path = _workspace_metadata_path

        self._meta_ws = MetaWorkspace(
            workspace_path=_meta_workspace_path,
            _workspace_metadata_path=_meta_workspace_metadata_path,
            _workspace_toml_filename=_meta_workspace_toml_filename,
        )

        self._tmpl_ws = TemplatesWorkspace(
            workspace_path=_templates_workspace_path,
            _workspace_metadata_path=_templates_workspace_metadata_path,
            _workspace_toml_filename=_templates_workspace_toml_filename,
        )

    @typechecked
    def initialize(
        self,
        workspace_id: str | None = None,
        workspace_name: str | None = None,
        # Workspace specific variables
        templates_workspace_id: str | None = None,
        templates_workspace_name: str | None = None,
    ) -> None:
        """Initializes a new OpenViatica Preconfigured workspace"""

        # A OpenViatica IS an instance of a MetaWorkspace, that just has other workspaces made by default

        if workspace_name is None:
            workspace_name = self.DEFAULT_WORKSPACE_NAME

        # Check if the workspace folder exists
        G.check_folder_exists(self.workspace_path)

        # Check that the workspace metadata does NOT exist
        G.check_folder_NOT_exists(self._workspace_metadata_path)

        # Create the metadata folder
        os.mkdir(self._workspace_metadata_path)

        # Initialize the meta workspace
        # It must hace the same workspace id & name since an openviatica workspace IS a meta workspace
        self._meta_ws.initialize(
            workspace_id=workspace_id, workspace_name=workspace_name
        )

        # Initialize a Templates Workspace
        self._tmpl_ws.initialize(
            workspace_id=templates_workspace_id, workspace_name=templates_workspace_name
        )

        # Link the meta workspace with all other workspaces
        self._meta_ws.link(
            target_workspace_path=self._tmpl_ws.workspace_path,
            target_workspace_type=self._tmpl_ws.WORKSPACE_TYPE,
        )

    class WorkspaceTools:
        MetaWorkspace: type["MetaWorkspace"]
        TemplatesWorkspace: type["TemplatesWorkspace"]


ovutils.WorkspaceTools.MetaWorkspace = MetaWorkspace
ovutils.WorkspaceTools.TemplatesWorkspace = TemplatesWorkspace
