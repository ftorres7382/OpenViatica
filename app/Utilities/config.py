import typing as t
import os

from app import Custom_Types as T

class Config:
    
    def init(self)->None:
        pass
    
    @classmethod
    def get_clean_app_config(cls,app_config_raw: t.Dict[str, t.Any]) -> T.APP_CONFIG_DICT:
        '''
        This function takes in the raw app config and returns the app config.
        It will manaully set all the values so that mypy can check them
        '''
        

        app_config: T.APP_CONFIG_DICT = {
            "app_database": {
                "engine": app_config_raw["app_database"]["engine"],
                "database_name": app_config_raw["app_database"]["database_name"],
                "sqlite": {
                    "path": app_config_raw["app_database"]["sqlite"]["path"]
                },
                "postgres": {
                    "host": app_config_raw["app_database"]["postgres"]["host"],
                    "user": app_config_raw["app_database"]["postgres"]["user"]
                }
            }         
        }

        # Check if we did not miss anything
        if app_config_raw != app_config:
            import dictdiffer # type: ignore
            from pprint import pprint
            print("-"*30)
            print("app_config_raw:")
            pprint(app_config_raw)
            print("\napp_config:")
            pprint(app_config)
            
            diff = list(dictdiffer.diff(app_config_raw, app_config))
            
            print("-"*30)
            print("Differences:")
            pprint(diff)
            print("-"*30)
            raise ValueError(f"ERROR! There are values un 'app_config_raw' that were not set in 'app_config'!")
        
        # Standardize values
        app_config["app_database"]["sqlite"]["path"] = os.path.abspath(app_config["app_database"]["sqlite"]["path"])
        return app_config

