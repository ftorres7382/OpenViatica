import typing as t
import argparse

from app.Utilities import Setup
from app.globals import APP_CONFIG


def main(cli_args: t.Any) -> None:
    '''
    This function will coordinate all of the apps functions
    '''
    

    # Database setup
    setup = Setup()
    setup.database_setup()

    # Setup the admin workspace
    setup.workspace_setup(APP_CONFIG["admin_workspace"]["folder_path"])
    
    
def parse_args() -> t.Any:
    '''
    This function sets up and parses the cli arguments
    '''
    parser = argparse.ArgumentParser(description="OpenViatica an open source data analysis framework.") 
    return parser.parse_args()



if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args)