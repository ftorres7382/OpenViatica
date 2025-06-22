import typing as t
import os

from app import Custom_Types as T
from app.Utilities import Type_Helper

class Config:
    
    def init(self)->None:
        self.type_helper = Type_Helper()
        
    
    @classmethod
    def get_clean_app_config(cls,app_config_raw: t.Dict[str, t.Any]) -> T.APP_CONFIG_DICT:
        '''
        This function takes in the raw app config and returns the app config.
        It will manaully set all the values so that mypy can check them
        '''
        
        # Remind myself to automate having to do this...
        # The idea would be that by changing the type itself, it should change how this is set guess
        import pdb; pdb.set_trace()
        # app_config: T.APP_CONFIG_DICT = 

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

