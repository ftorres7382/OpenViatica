import typing as t
from app.Custom_Types import Enums as E

# If we need to organize, use regions, if we need more, use a folder and divide by files

######################################
# Config min types
###################################### 
# region
CONFIG_MIN_DICT = t.TypedDict("CONFIG_MIN_DICT", {
    "app_config_path": str
})
# endregion


######################################
# App Config Types
###################################### 
# region

APP_CONFIG_POSTGRES_DICT = t.TypedDict("APP_CONFIG_POSTGRES_DICT", {
    "host": str,
    "user": str
})
APP_CONFIG_SQLITE_DICT = t.TypedDict("APP_CONFIG_SQLITE_DICT", {
    "path": str,
})

APP_CONFIG_APP_DATABASE_DICT = t.TypedDict("APP_CONFIG_APP_DATABASE_DICT", {
    "engine": E.ALLOWED_SQL_ENGINES,
    "database_name": str,
    "postgres": APP_CONFIG_POSTGRES_DICT,
    "sqlite" : APP_CONFIG_SQLITE_DICT
})

APP_CONFIG_ADMIN_WORKSPACE_DICT = t.TypedDict("APP_CONFIG_ADMIN_WORKSPACE_DICT", {
    "template_workspace_folder_path": str,
    "template_user_workspace_relpath": str,
    "template_venv_requirements_relpath": str,

    "base_folder_path": str,
    "admin_workspace_name": str
})

APP_CONFIG_DICT = t.TypedDict("APP_CONFIG_DICT", {
    "mode": str,
    "app_database": APP_CONFIG_APP_DATABASE_DICT,
    "workspace_settings": APP_CONFIG_ADMIN_WORKSPACE_DICT
    
})
# endregion

######################################
# SQLA Types
###################################### 
# region

SQLA_CONNECTION_INFO_DICT = t.TypedDict("SQLA_CONNECTION_INFO_DICT", {
    "engine": E.ALLOWED_SQL_ENGINES,
    "connection_configuration": t.Union[APP_CONFIG_SQLITE_DICT, APP_CONFIG_POSTGRES_DICT],
    "connection_string": str
})

SQLA_ENGINE_CONNECT_ARGS_DICT_TYPE = t.TypedDict("SQLA_ENGINE_CONNECT_ARGS_DICT_TYPE", {
    "timeout": int
})
# endregion