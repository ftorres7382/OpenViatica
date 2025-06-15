import typing as t
import app.Utilities.Custom_Types.Enums as E

# If we need to organize, use 

CONFIG_MIN_DICT = t.TypedDict("CONFIG_MIN_DICT", {
    "app_config_path": str
})


APP_CONFIG_POSTGRES_DICT = t.TypedDict("APP_CONFIG_POSTGRES_DICT", {
    "host": str,
    "user": str
})
APP_CONFIG_SQLITE_DICT = t.TypedDict("APP_CONFIG_SQLITE_DICT", {
    "path": str,
})

APP_CONFIG_DICT = t.TypedDict("APP_CONFIG_DICT", {
    "app_database": E.ALLOWED_SQL_ENGINES,
    "postgres": APP_CONFIG_POSTGRES_DICT,
    "sqlite" : APP_CONFIG_SQLITE_DICT
})