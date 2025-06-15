import typing as t

import app.Utilities.Custom_Types as T

def get_app_config(app_config_raw: t.Dict[str, t.Any]) -> T.APP_CONFIG_DICT:
    '''
    This function takes in the raw app config and returns the app config.
    It will manaully set all the values so that mypy can check them
    '''
    

    app_config: T.APP_CONFIG_DICT = {
        "app_database": app_config_raw["app_database"],
        "sqlite": {
            "path": app_config_raw["app_database"]["sqlite"]["path"]
        },
        "postgres": {
            "host": app_config_raw["app_database"]["postgres"]["host"],
            "user": app_config_raw["app_database"]["postgres"]["user"]
        }
    }
    return app_config
