''''''

# Standard
import logging
# Related
# Local
import errors


def check_modo():
    '''Run through a series of tests to make sure ModoPyWrap is able to
    interact properly with modo.
    '''
    
    # First we import some modo libraries, and see if it raises any errors.
    try:
        import lx
    except ImportError:
        raise errors.ModoLibrariesNotFound()

if __name__ != '__main__':
    # If the package is being imported, run the check function.
    # The result of this, is that a check 'should' always occur
    check_modo()
