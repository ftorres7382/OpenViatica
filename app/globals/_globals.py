import toml

import app.Utilities.Custom_Types as T
import app.Utilities.Config as Config

config_min_raw = toml.load("config_min.toml")
CONFIG_MIN: T.CONFIG_MIN_DICT = {
    "app_config_path": config_min_raw["app_config_path"]
}


# Read the actual app config
app_config_raw = toml.load(CONFIG_MIN["app_config_path"])
APP_CONFIG: T.APP_CONFIG_DICT = Config.get_clean_app_config(app_config_raw)
