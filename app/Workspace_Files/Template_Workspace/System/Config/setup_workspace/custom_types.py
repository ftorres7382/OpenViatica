from typing_extensions import TypedDict
from pydantic import ConfigDict
class WORKSPACE_SETUP_CONFIG_DICT(TypedDict):

    script_to_root_relpath:str

    user_workspace_foldername :str

    internal_system_foldername: str

    sytem_config_foldername: str

    setup_script_relpath: str

    system_utilities_foldername: str





setattr(WORKSPACE_SETUP_CONFIG_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))



           





                                      

            

                                       

        



