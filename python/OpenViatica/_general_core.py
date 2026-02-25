from typeguard import typechecked

class General:
    '''Used for general functions in the package itself'''
    @staticmethod
    @typechecked
    def vprint(value:object, verbose:bool = True) -> None:
        '''Verbose print, prints the value ONLY if verbose is True'''
        if verbose:
            print(value)
    