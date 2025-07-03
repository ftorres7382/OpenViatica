import typing as t
import argparse
import time

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
    setup.workspace_setup(APP_CONFIG["workspace_settings"]["base_folder_path"])

    print(f"\nSuccess! The Admin Workspace has been setup in the folder: '{APP_CONFIG['workspace_settings']['base_folder_path']}'")
    print(f"Feel free to open it in an IDE. VS Code is recommended, since it is natively supported.\n")
    
    
def parse_args() -> t.Any:
    '''
    This function sets up and parses the cli arguments
    '''
    parser = argparse.ArgumentParser(description="OpenViatica an open source data analysis framework.") 
    return parser.parse_args()



if __name__ == "__main__":
    cli_args = parse_args()
    main(cli_args)