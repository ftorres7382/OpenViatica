from OpenViatica._core_workspaces._core_workspaces import MetaWorkspace

class ovutils:

    class WorkpaceTools:
        MetaWorkspace: type["MetaWorkspace"]


ovutils.WorkpaceTools.MetaWorkspace = MetaWorkspace




