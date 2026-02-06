'''
# OpenViatica
The purpose of this module is to provide a CLI, Python importable OR API based way to create and manage a data analysis workspace.

A workspace is defined as a folder that is fully configured to do data analytics

# Methods
    1. ovutils
        The main tool in which the workspace objects will be managed.
        
        This includes creation & editing of workspace conmfiguration 
        
        Example: 
        ```python
        from OpenViatica import ovutils
        ovutils.fibonacci()
        ```
'''
# The documentation above will show up if the user runs help() on this module
from ._ovutils import ovutils

__all__ = [
    "ovutils"
]