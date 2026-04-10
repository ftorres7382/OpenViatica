from OpenViatica._core_workspaces._core_workspaces import MetaWorkspace

class ovutils:

    class WorkpaceTools:
        MetaWorkspace: type["MetaWorkspace"]
    pass

ovutils.WorkpaceTools.MetaWorkspace = MetaWorkspace




