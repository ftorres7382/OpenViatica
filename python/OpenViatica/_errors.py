class ov_errors:
    class OpenViaticaError(Exception):
        '''Base class for ALL OpenViatica Errors'''
        pass

    class WorkspaceFoundError(OpenViaticaError):
        '''Raised whenever the workspace is found'''
        pass

    class FolderExistsError(OpenViaticaError):
        '''Raised whenever a folder is found'''
        pass
    
    class FolderNotFoundError(OpenViaticaError):
        '''Raised whenever a folder is found'''
        pass
