#
# Copyright 2026 ftorres7382
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.#
'''
# OpenViatica
The purpose of this module is to provide a CLI, Python importable OR API based way to create and manage a data analysis workspace.

A workspace is defined as a folder that is fully configured to do data analytics

ALL modules, methods & functions are made so that the help() is the primary way to get the documentation on how to use the tools

# Methods
    1. ovutils
        The main tool in which the workspace objects will be managed.
        
        This includes creation & editing of workspace configuration 
        
        Example: 
        ```python
        from OpenViatica import ovutils

        help(ovutils)
        ```
'''
# The documentation above will show up if the user runs help() on this module
from ._core import ovutils

__all__ = [
    "ovutils"
]