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

class InvalidArgumentSupplied(ModoPyWrapError):
    '''The arguments from modo given to a user script are formatted incorrectly.
    '''

    def __init__(self, message):
        '''
        '''
        
        self.message = message
    
    def __str__(self):
        '''
        '''
        return '\n%s' % self.message
