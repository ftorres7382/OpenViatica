import toml

import app.globals as globals
from app.Utilities import Setup



def main() -> None:
    '''
    This function will coordinate all of the apps functions
    '''

    # Database setup
    Setup.database_setup()

    
    

    print(globals.APP_CONFIG)



if __name__ == "__main__":
    main()