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

class ModoLibrariesNotFound(MoopyError):
    '''The libraries provided by an instance of modo were not found.
    '''
    pass

class ScriptArgumentsError(MoopyError):
    '''The base script arguments error.'''

    def __init__(self, message):
        '''
        '''
        
        self.message = message
    
    def __str__(self):
        '''
        '''
        return '\n%s' % self.message

class ArgumentIsNotAnOption(ScriptArgumentsError):
    '''An argument supplied was found within the list of accepted arguments.
    '''
    pass

class DuplicateArgumentSupplied(ScriptArgumentsError):
    '''A keyword argument was given twice. This is thrown to prevent unintended
    behavior.
    '''
    pass

class InvalidArgumentFormatting(ScriptArgumentsError):
    '''The arguments from modo given to a user script are formatted incorrectly.
    '''
    pass

class InvalidArgumentType(ScriptArgumentsError):
    '''An argument supplied is not an accepted type for that argument.
    '''
    pass

class RequiredArgumentMissing(ScriptArgumentsError):
    '''A required argument was not supplied in any form by the user.
    '''
    pass
