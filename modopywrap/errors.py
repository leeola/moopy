''''''

# Standard
# Related
# Local


class ModoPyWrapError(Exception):
    '''The base Modo Wrapper error.
    '''
    pass

class ChannelsError(ModoPyWrapError):
    '''The base channels error.
    '''
    pass

class ImproperMatchType(ModoChannelsError):
    '''
    '''
    
    def __init__(self, channel1, channel2, message=None):
        '''
        '''
        
        self.channel1 = channel1
        self.channel2 = channel2
        self.message = message
    
    def __str__(self):
        '''
        '''
        if self.message is not None:
            return '\n%s\nChannel #1: %s\nChannel #2: %s' % self.message

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

class ModoLibrariesNotFound(ModoPyWrapError):
    '''The libraries provided by an instance of modo were not found.
    '''
    pass
