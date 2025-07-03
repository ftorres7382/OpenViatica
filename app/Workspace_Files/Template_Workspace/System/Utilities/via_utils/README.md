# via_utils

This module is made to be a python, CLI and API integrated module for handling anything having to do with workspace configurations.

Some examples of what this will encompass are the following:

1. Workspace configurations
   
   1. Changing whether the current workpsace sets a single directory as root as part of the .venv
   
   2. Changing the root path of the workspace

2. Permissions Management
   
   1. Adding/removing users from a workpsace
   
   2. Managing groups

3. etc.

The idea is that this can be automatically setup so that the user can use it in python code or in the CLI.

It should also know if how the workspace should be interacted with. So multiple versions of this will have to be configured.

It should check the user's permission to do a specific action before doing any action.


