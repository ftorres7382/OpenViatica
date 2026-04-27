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
    
    class FolderNotExistsError(OpenViaticaError):
        '''Raised whenever a folder is found'''
        pass

    class WorkspaceMetadataExistsError(OpenViaticaError):
        '''Raised whenever the workspace metadata folder has been identified and should not be there'''
        pass

    class WorkspaceTomlFormatError(OpenViaticaError):
        '''Raised whenever the workspace toml does not conform to format'''
        pass

    class LinkFoundError(OpenViaticaError):
        '''Raised whenever the workspace has already been linked'''
        pass

