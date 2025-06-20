from app.Utilities import Setup



def main() -> None:
    '''
    This function will coordinate all of the apps functions
    '''

    # Database setup
    setup = Setup()
    setup.database_setup()

    
    



if __name__ == "__main__":
    main()