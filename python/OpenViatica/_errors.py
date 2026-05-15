class ov_errors:
    class OpenViaticaError(Exception):
        """Base class for ALL OpenViatica Errors"""

        pass

    class WorkspaceFoundError(OpenViaticaError):
        """Raised whenever the workspace is found"""

        pass

    class WorkspaceNotFoundError(OpenViaticaError):
        """Raised whenever the workspace was not found"""

        pass

    class FolderExistsError(OpenViaticaError):
        """Raised whenever a folder is found"""

        pass

    class FolderNotExistsError(OpenViaticaError):
        """Raised whenever a folder is found"""

        pass

    class WorkspaceMetadataExistsError(OpenViaticaError):
        """Raised whenever the workspace metadata folder has been identified and should not be there"""

        pass

    class WorkspaceMetadataNotFoundError(OpenViaticaError):
        """Raised whenever the workspace metadata folder could not be found"""

        pass

    class MultipleWorkspaceMetadataFoundError(OpenViaticaError):
        """Raised whenever multiple workspace metadata folders are found and its a problem for the logic"""

        pass

    class WorkspaceTomlFormatError(OpenViaticaError):
        """Raised whenever the workspace toml does not conform to format"""

        pass

    class LinkFoundError(OpenViaticaError):
        """Raised whenever the workspace has already been linked"""

        pass

    class LinkNotFoundError(OpenViaticaError):
        """Raised when a link value could not be found"""

        pass

    class DuplicatedLinksFoundError(OpenViaticaError):
        """Raised whenever we find multiple links when we expect only one link result"""

        pass

    class MultipleLinksFoundError(OpenViaticaError):
        """Raised whenever we find multiple link results when we expect only one to match"""

        pass

    class WorkspaceTypeNotFoundError(OpenViaticaError):
        """'Raised whenever the workspace type cannot be found and it required."""

        pass
