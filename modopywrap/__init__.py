''''''

# Standard
# Related
# Local
import errors


def check_modo():
    '''Run through a series of tests to make sure ModoPyWrap is able to
    interact properly with modo.
    
    @note: This function is put here so that the rest of the library can
    '''
    
    # First we import some modo libraries, and see if it raises any errors.
    try:
        import lx
    except ImportError:
        raise errors.ModoLibrariesNotFound()

if __name__ != '__main__':
    # If the library is being imported, run the check function.
    check_modo()
