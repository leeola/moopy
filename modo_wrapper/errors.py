''''''

# Standard
# Related
# Local


class ModoWrapperError(Exception):
    '''The base Modo Wrapper error.
    '''
    pass

    
class ModoLibrariesNotFound(ModoWrapperError):
    '''The libraries provided by an instance of modo were not found.
    '''
    pass

