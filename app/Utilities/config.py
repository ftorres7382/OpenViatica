import typing as t
from pydantic import TypeAdapter

from app import Custom_Types as T


class Config:
    
    def __init__(self)->None:
        from app.Custom_Types import Type_Helper
        self.type_helper = Type_Helper()
        
    
    def get_clean_app_config(self,app_config_raw: t.Dict[str, t.Any]) -> T.APP_CONFIG_DICT:
        '''
        This function takes in the raw app config and returns the app config.
        It will manaully set all the values so that mypy can check them
        '''

        # Check the dictionary
        adapter = TypeAdapter(T.APP_CONFIG_DICT)
        app_config = adapter.validate_python(app_config_raw)
        
        return app_config

