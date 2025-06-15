import toml
import typing as t
import app.Utilities.Custom_Types as T

config_min_raw = toml.load("config_min.toml")
config_min = t.cast(T.CONFIG_MIN_DICT, config_min_raw)
del config_min_raw # No need for having the one without type hints


def main() -> None:
    print(config_min)



if __name__ == "__main__":
    main()