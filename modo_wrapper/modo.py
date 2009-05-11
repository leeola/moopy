''''''

# Standard
# Related
# Local
import errors


def check_modo():
    '''Run through a series of tests to make sure modo_wrapper is able to
    interact properly with modo.'''
    
    # First we import some modo libraries, and see if it raises any errors.
    try:
        import lx
    except ImportError:
        raise errors.ModoLibrariesNotFound()
