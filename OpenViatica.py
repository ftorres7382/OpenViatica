from app.Utilities import Setup



def main() -> None:
    '''
    This function will coordinate all of the apps functions
    '''

    # Database setup
    setup = Setup()
    setup.database_setup()

    # Setup the admin workspace if not already made
    
    



if __name__ == "__main__":
    main()