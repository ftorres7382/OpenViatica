import typing as t
from app.Custom_Types import Enums as E
from typing import Union
from pydantic import ConfigDict

from typing_extensions import TypedDict

# If we need to organize, use regions, if we need more, use a folder and divide by files

######################################
# Config min types
###################################### 
# region
class CONFIG_MIN_DICT(TypedDict):
    app_config_path: str
setattr(CONFIG_MIN_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid")) # Done this way so that pylance does not complain
# endregion


######################################
# App Config Types
###################################### 
# region

class APP_CONFIG_POSTGRES_DICT(TypedDict):
    host: str
    user: str
setattr(APP_CONFIG_POSTGRES_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))


class APP_CONFIG_SQLITE_DICT(TypedDict):
    path: str
setattr(APP_CONFIG_SQLITE_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))

class APP_CONFIG_APP_DATABASE_DICT(TypedDict):
    engine: E.ALLOWED_SQL_ENGINES
    database_name: str
    postgres: APP_CONFIG_POSTGRES_DICT
    sqlite: APP_CONFIG_SQLITE_DICT
setattr(APP_CONFIG_APP_DATABASE_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))


class APP_CONFIG_ADMIN_WORKSPACE_DICT(TypedDict):
    template_workspace_folder_path: str


    user_workspace_foldername: str


    internal_system_foldername: str
    sytem_config_foldername: str
    system_utilities_foldername: str
    setup_script_relpath: str


    base_folder_path: str
    admin_workspace_name: str
setattr(APP_CONFIG_ADMIN_WORKSPACE_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))


class APP_CONFIG_DICT(TypedDict):
    mode: str
    app_database: APP_CONFIG_APP_DATABASE_DICT
    workspace_settings: APP_CONFIG_ADMIN_WORKSPACE_DICT

setattr(APP_CONFIG_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))

# endregion


######################################
# Workspace Config Types
###################################### 
# region

# These settings are for all the settings that should be bundled into the workpsace itself

class WORKSPACE_SETUP_CONFIG_DICT(TypedDict):
    script_to_root_relpath:str
    user_workspace_foldername :str
    internal_system_foldername: str
    sytem_config_foldername: str
    setup_script_relpath: str
    system_utilities_foldername: str


setattr(WORKSPACE_SETUP_CONFIG_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))

# endregion


######################################
# SQLA Types
###################################### 
# region

class SQLA_CONNECTION_INFO_DICT(TypedDict):
    engine: E.ALLOWED_SQL_ENGINES
    connection_configuration: Union[APP_CONFIG_SQLITE_DICT, APP_CONFIG_POSTGRES_DICT]
    connection_string: str
setattr(SQLA_CONNECTION_INFO_DICT, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))


class SQLA_ENGINE_CONNECT_ARGS_DICT_TYPE(TypedDict):
    timeout: int
setattr(SQLA_ENGINE_CONNECT_ARGS_DICT_TYPE, "__pydantic_config__", ConfigDict(strict=True, extra="forbid"))
# endregion
