''''''

# Standard
# Related
# Local


class MoopyError(Exception):
    '''The base Moopy error.
    '''
    pass

class ChannelsError(MoopyError):
    '''The base channels error.
    '''
    pass

class ImproperMatchType(ChannelsError):
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

class InvalidArgumentSupplied(MoopyError):
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

class ModoLibrariesNotFound(MoopyError):
    '''The libraries provided by an instance of modo were not found.
    '''
    pass
