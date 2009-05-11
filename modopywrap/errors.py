''''''

# Standard
# Related
# Local


class ModoPyWrapError(Exception):
    '''The base Modo Wrapper error.
    '''
    pass

    
class ModoLibrariesNotFound(ModoPyWrapError):
    '''The libraries provided by an instance of modo were not found.
    '''
    pass

