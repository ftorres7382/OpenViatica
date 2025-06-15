import toml

import app.Utilities.Custom_Types as T
import app.Utilities.Config as Config

config_min_raw = toml.load("config_min.toml")
config_min: T.CONFIG_MIN_DICT = {
    "app_config_path": config_min_raw["app_config_path"]
}
del config_min_raw # No need for having the one without type hints

# Read the actual app config
app_config_raw = toml.load(config_min["app_config_path"])
app_config: T.APP_CONFIG_DICT = Config.get_app_config(app_config_raw)


def main() -> None:
    '''
    This function will coordinate all of the apps functions
    '''

    # Database setup

    print(config_min)



if __name__ == "__main__":
    main()